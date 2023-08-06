import configparser
import json
import os
import shutil
import signal
import subprocess
import sys
import traceback
from datetime import datetime

import requests
import virtualenv
from celery import exceptions
from celery.utils.log import get_task_logger

from api_client import NjinnAPI
from packinstall import PackInstallation
from postprocess import postproces_output
from utils import get_config_path, is_windows
from worker.__main__ import get_celery_app

app = get_celery_app()
log = get_task_logger(__name__)

config = None


def get_njinn_api():
    """
    Set the NjinnAPI class to make authenticated calls.
    """
    global config
    if not config:
        config = configparser.ConfigParser()
        config.read(get_config_path())

    api = config["DEFAULT"]["njinn_api"]
    secret = config["DEFAULT"]["secret"]
    worker_name = config["DEFAULT"]["name"]
    execution_id = context["njinn_execution_id"]

    njinn_api = NjinnAPI(api, secret, worker_name, execution_id)
    return njinn_api


def report_action_result(action_output):
    """
    Report action result of the task to the Njinn API.
    """

    action_output["context"] = context
    if not "state_info" in action_output:
        action_output["state_info"] = action_output["state"]

    action_output["worker"] = config["DEFAULT"]["name"]

    result_api = "/api/v1/workercom/results"
    log.info(f"Calling {result_api} with action output {json.dumps(action_output)}")

    r = njinn_api.put(result_api, json=action_output)
    if r.status_code == 413:
        if action_output["log"]:
            log.warning("Request too large, trying with a truncated log")
            first_lines = "\n".join(action_output["log"][:1000].split("\n")[:-1])
            last_lines = "\n".join(action_output["log"][-1000:].split("\n")[1:])
            truncated_log = (
                "Log too long - Truncated version: \n\n"
                + first_lines
                + "\n...(output omitted here)...\n"
                + last_lines
            )
            action_output["log"] = truncated_log
            r = njinn_api.put(result_api, json=action_output)

    log.info(f"Response: {r.status_code} {r.text}")


def report_picked(context):
    """
    Report action result of the task to the Njinn API.
    """

    data = {"context": context, "worker": config["DEFAULT"]["name"]}

    picked_api = "/api/v1/workercom/picked"
    log.info(f"Calling {picked_api} with data {json.dumps(data)}")

    r = njinn_api.put(picked_api, json=data)
    log.info(f"Response: {r.status_code} {r.text}")


def read_stdout(proc, lines):
    """ Reads all remaining stdout """
    if proc and proc.stdout:
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                return
            lines.append(line)
    return None


@app.task(name="njinn_execute")
def njinn_execute(action, pack, action_context):
    global context
    proc = None
    working_dir = None
    result = {
        "state": "ERROR",
        "output": {"error": f"Error during setup of pack {pack}"},
    }
    output_lines = []
    try:
        context = dict()
        context["action_execution_id"] = action_context.get("action_execution_id")
        context["task_name"] = action_context.get("task_name")
        context["execution_id"] = action_context.get("execution_id")
        context["njinn_execution_id"] = action_context.get("njinn_execution_id")

        global njinn_api
        njinn_api = get_njinn_api()
        report_picked(context)

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        log.info("Njinn task initiating")

        pack_installation = PackInstallation(pack, njinn_api)
        pack_installation.setup()

        action_execution_id = action_context.get("action_execution_id")
        working_dir = os.path.join("working", action_execution_id)
        log.debug("Creating working directory %s", working_dir)
        os.makedirs(working_dir)

        input_file = os.path.join(working_dir, "in.json")
        input_file_content = {
            "config_path": get_config_path(),
            "action": action,
            "pack": pack,
            "action_context": action_context,
        }

        with open(input_file, "w") as fp:
            json.dump(input_file_content, fp)
        if is_windows():
            py_cmd = "python.exe"
        else:
            py_cmd = "python"
        cmd = [py_cmd, "action.py", f"{input_file}"]

        if is_windows():
            # required so that PATH is observed
            shell = True
        else:
            # Facilitates killing the process tree on cancel, not yet implemented on Windows
            shell = False
        # Run detached, without a shell, and start a new group
        log.info("Running: %s", cmd)
        proc = subprocess.Popen(
            cmd,
            universal_newlines=True,
            cwd=dir_path,
            shell=shell,
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            start_new_session=True,
            env=pack_installation.virtualenv_env(),
        )
        log.debug("Subprocess started.")
        read_stdout(proc, output_lines)
        if proc.returncode != 0:
            log.warning("Return code %s", proc.returncode)
            raise Exception(f"Return code {proc.returncode}")

        with open(os.path.join(working_dir, "out.json")) as output_file:
            stdout = "".join(output_lines)
            stdout_variables = postproces_output(stdout or "")
            result = json.load(output_file)
            log.debug("Read output from file: %s", result)
            # precedence for results from script, but don't overwrite with None
            stdout_variables.update(result.get("output", {}) or {})
            result["output"] = stdout_variables
            result["log"] = f"{pack_installation.status}\n{stdout}"

    except exceptions.SoftTimeLimitExceeded:
        log.debug("Timeout")
        process_log = None
        stdout_variables = {}
        if proc:
            try:
                log.debug("Trying to terminate child proces %s", proc.pid)
                # Kill the whole process group, i.e. including child processes.
                os.killpg(proc.pid, signal.SIGKILL)
                log.debug("Kill signal sent to process %s", proc.pid)
                # read remaining lines
                read_stdout(proc, output_lines)
                process_log = "".join(output_lines)
                stdout_variables = postproces_output(process_log or "")
                log.info("Terminated process %s after timeout.", proc.pid)
                log.debug("Process stdout: %s", process_log)
            except Exception as e:
                log.warning("Problem terminating child process: %s", e)
        else:
            log.warning("No process found to terminate")
        error = "Time limit reached. This may be due to a timeout or a cancel request."
        process_log = process_log or error
        output = stdout_variables.update({"error": error})
        result = {
            "state": "ERROR",
            "output": output,
            "log": process_log,
            "state_info": error,
        }
        log.debug("Result after timeout: %s", result)
    except Exception as e:
        log.error("Error while running process: %s", e)
        # read remaining lines
        read_stdout(proc, output_lines)
        stdout = "".join(output_lines)
        output = postproces_output(stdout or "")
        error = stdout or traceback.format_exc()
        output.update({"error": error})
        result = {"state": "ERROR", "output": output, "log": error}
        log.debug("Result: %s", result)
    finally:
        report_action_result(result)
        if working_dir:
            shutil.rmtree(working_dir)

    return None
