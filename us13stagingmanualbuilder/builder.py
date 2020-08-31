from . import CONFIG, logger
import os
from subprocess import Popen, PIPE, STDOUT
import json
import requests
import shutil

exec_name = {
    "StandaloneWindows64": "Unitystation.exe",
    "StandaloneOSX": "Unitystation.app",
    "StandaloneLinux64": "Unitystation"
}


def make_command(target: str):
    return f"\"{CONFIG['unity_executable']}\"-quit " \
           f" -batchmode -nographics -logfile - " \
           f"-buildTarget {target} " \
           f"-projectPath \"{CONFIG['project_path']}\" " \
           f"-executeMethod BuildScript.BuildProject " \
           f"-customBuildPath \"{os.path.join(CONFIG['output_dir'], target, exec_name[target])}\" " \
           f"-customBuildName Unitysation "


def build(command: str, target: str):
    try:
        logger.log(command)
        cmd = Popen(command, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
        for line in cmd.stdout:
            if line.strip():
                logger.log(line)
            if "Build succeeded!" in line:
                CONFIG[f"{target}_build_status"] = "success"
        cmd.wait()
        exit_code = cmd.returncode

    except Exception as e:
        logger.log(str(e))
        raise e

    CONFIG[f"{target}_build_status"] = "success" if exit_code == 0 else "fail"

    if CONFIG["abort_on_build_fail"] and CONFIG[f"{target}_build_status"] == "fail":
        logger.log(f"build for {target} failed and config is set to abort process on fail, aborting")
        raise Exception("A build failed and config is set to abort on fail")


def get_build_number():
    logger.log("Getting build number from last sucessfull push from Github")
    url = "https://api.github.com/repos/unitystation/unitystation/actions/runs"
    response = json.loads(requests.get(url).text)
    build_number = 0

    if response is None:
        logger.log("GitHub API is not responding. Can't continue.")
        raise Exception("GitHub API unresponsive.")

    for run in response["workflow_runs"]:
        try:
            if run["event"] == "push" and run["conclusion"] == "success":
                build_number = run["run_number"]
                break
        except KeyError:
            if run == response["workflow_runs"][-1]:
                logger.log("No sucessfull push events found in gh api response, aborting.")
                raise Exception("Be sucessful or die")

    local = get_local_build_number()
    if local is not None:
        if build_number <= local:
            logger.log("Build number is less than or equal to last cached number")
            logger.log(f"Last run: {build_number} Last local build: {local}")

            if CONFIG["build_number_autoincrement"]:
                build_number = local + 1
                logger.log(f"Making a new build number {build_number}")
            else:
                logger.log("Local auto increment is disabled. Can't continue!")
                raise Exception("Found newer build number on local but autoincrement was disabled.")
    else:
        logger.log("There is no previous local build number")

    CONFIG["build_number"] = build_number
    write_local_build_number(build_number)
    logger.log(f"Setting {build_number} as the build number...")


def get_local_build_number():
    try:
        with open("build_number.txt") as bn:
            buil_number = bn.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.log(str(e))
        raise e

    return int(buil_number.strip())


def write_local_build_number(number: int):
    with open("build_number.txt", "w") as bn:
        bn.write(str(number))


def create_builds_folder():
    for target in CONFIG["target_platform"]:
        try:
            os.makedirs(
                os.path.join(CONFIG["output_dir"], target), exist_ok=True)
        except Exception as e:
            logger.log(str(e))


def set_jsons_data():
    build_info = os.path.join(CONFIG["project_path"], "Assets", "StreamingAssets", "buildinfo.json")
    config_json = os.path.join(CONFIG["project_path"], "Assets", "StreamingAssets", "config", "config.json")

    with open(build_info) as read:
        p_build_info = json.loads(read.read())

    with open(config_json) as read:
        p_config_json = json.loads(read.read())

    with open(build_info, "w") as json_data:
        p_build_info["BuildNumber"] = CONFIG["build_number"]
        p_build_info["ForkName"] = CONFIG["forkName"]
        json.dump(p_build_info, json_data, indent=4)

    with open(config_json, "w") as json_data:
        url = CONFIG["CDN_DOWNLOAD_URL"]
        p_config_json["WinDownload"] = url.format(CONFIG["forkName"], "StandaloneWindows64", CONFIG["build_number"])
        p_config_json["OSXDownload"] = url.format(CONFIG["forkName"], "StandaloneOSX", CONFIG["build_number"])
        p_config_json["LinuxDownload"] = url.format(CONFIG["forkName"], "StandaloneLinux64", CONFIG["build_number"])
        json.dump(p_config_json, json_data, indent=4)


def clean_builds_folder():
    for target in CONFIG['target_platform']:
        folder = os.path.join(CONFIG["output_dir"], target)

        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                logger.log((str(e)))


def start_building():
    logger.log("Starting build process...")
    get_build_number()
    clean_builds_folder()
    create_builds_folder()
    set_jsons_data()

    for target in CONFIG["target_platform"]:
        logger.log(f"\n****************\nStarting build of {target}...\n****************\n")
        build(make_command(target), target)

    logger.log("\n\n*************************************************\n\n")
    for target in CONFIG["target_platform"]:
        logger.log(f"Build for {target} was a {CONFIG[target + '_build_status']}")
    logger.log("\n\n*************************************************\n\n")
