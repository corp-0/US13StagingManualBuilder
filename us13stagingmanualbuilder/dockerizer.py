from . import CONFIG, logger
import shutil
import os
from subprocess import Popen, PIPE, STDOUT


def copy_server_build():
    if os.path.isdir("Docker/server"):
        shutil.rmtree("Docker/server")

    build_path = os.path.join(CONFIG["output_dir"], "StandaloneLinux64")
    shutil.copytree(build_path, "Docker/server")


def make_image():
    logger.log("Creating image")
    cmd = Popen("docker build -t unitystation/unitystation:develop Docker",
                stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    for line in cmd.stdout:
        logger.log(line)

    cmd.wait()
    rc = cmd.returncode
    logger.log(f"process says: {rc}")


def push_image():
    logger.log("Pushing docker image (Needs to be logged in before running this!)")
    cmd = Popen("docker push unitystation/unitystation:develop", stdout=PIPE, stderr=STDOUT, universal_newlines=True)

    for line in cmd.stdout:
        logger.log(line)
    cmd.wait()
    rc = cmd.returncode
    logger.log(f"process says: {rc}")


def start_dockering():
    logger.log("Starting docker process...")

    copy_server_build()
    make_image()
    push_image()
