import json
import os
import shutil
from . import logger

with open("config.json") as f:
    CONFIG = json.load(f)

envs = ["SSH_PRIVATE_KEY",
        "HUB_USERNAME",
        "SSH_USER",
        "SSH_KNOWN_HOSTS",
        "HUB_PASSWORD",
        "ERROR_WEBHOOK",
        "CDN_HOST",
        "CDN_USER",
        "DOCKER_USERNAME",
        "DOCKER_PASSWORD"]

req_configs = ["unity_executable",
               "project_path",
               "target_platform",
               "license_file",
               "CDN_DOWNLOAD_URL",
               "forkName",
               "output_dir"]

optional_configs = ["abort_on_build_fail",
                    "build_number_autoincrement"]


def load_envs_from_json():
    logger.log("Reading config from json file...")
    for env in envs:
        try:
            os.environ[env] = CONFIG[env]
        except KeyError:
            pass
        except Exception as e:
            logger.log(str(e))


def check_envs():
    logger.log("Checking required environmental variables...")
    for env in envs:
        try:
            _env = os.environ[env]
        except KeyError:
            logger.log(f"Required environmental variable not set: {env}")
            raise KeyError
        except Exception as e:
            logger.log(str(e))


def check_config_file():
    for config in req_configs:
        if config not in CONFIG.keys():
            logger.log(f"Missing required value in config file! {config}")
            raise Exception("Missing required config value")


def check_optionals():
    for config in optional_configs:
        if config not in CONFIG.keys():
            logger.log(f"Optional config {config} was not found in config file and defaulted to false")
            CONFIG[config] = False


def check_dirs():
    for folder in ["unity_executable", "project_path"]:
        if not os.path.isdir(CONFIG[folder]) and not os.path.isfile(CONFIG[folder]):
            logger.log(f"{folder} was declared in config.json, but the folder doesn't exists!")
            logger.log(f"Non existant folder: {CONFIG[folder]}")
            raise Exception("Non existant required folder")


def check_license_file():
    if not os.path.isfile(CONFIG["license_file"]):
        logger.log("Couldn't find the declared unity_license! Try creating a new one if you havem't yet.")
        raise Exception("Missing license file")


def clean_builds_folder():
    if os.path.isdir(CONFIG['output_dir']):
        try:
            logger.log("Cleaning builds folder...")
            shutil.rmtree(CONFIG["output_dir"])
        except Exception as e:
            logger.log(str(e))


##########
load_envs_from_json()
check_envs()
check_config_file()
check_dirs()
check_license_file()
clean_builds_folder()
