# US13 Staging Manual Builder

A script for this times of need

This script will attempt to build and publish a new version to Staging server and our CDN.
Just check everything is alright in ``config.json`` and set these environmental variables for FTP credentials:

- ``CDN_HOST`` 
- ``CDN_USER`` 
- ``CDN_PASSWORD``

You could also set these in your ``config.json`` but it is kinda unsecure.

## Features
- [x] Config file to set all the shiet
- [x] Error handling
- [x] Basic logs
- [x] Builds to all 3 supported platforms
- [x] Makes the docker image and updates it
- [x] Uploads to CDN 

## Dependencies:
- Python >3.6
- Requests (Pyhon package)
- Internet connection
- Docker
- Unity
- Unitystation repo with latest develop at the moment of build


## Usage:
1. Install required software.
2. Install the required python package with ``pip install requests``.
3. Fill in config.json with your directories and desired behavior.
4. Set your environmental variables (or declare them in the same config.json).
5. Run ``python main.py``


### Config explanation:
- ``unity_executable`` where in your machine is the Unity editor executable.
- ``project_path`` where in your machine is the UnityProject folder (Remember to fetch and rebase from upstream before
building).
- ``target_platform`` which platforms do you want to build.
- ``license_file`` where in your machine is the .ulf file generated by Unity. You can get from from Unity Hub, in the
License manage and Manual Activation option.
- ``CDN_DOWNLOAD_URL`` how should the download link look. This is required for the Station Hub to actually download 
the build in the clients without crashing.
- ``forkName`` also needed for Hub. This is the name that identifies Forks.
- ``build_auto_increment`` If your local cashed build number is equal or less than the last successful run number from
github, this will simply auto increment the build number. Defaults to false if not set explicitly to true. Aborts the
build if your local number is less than or equal to last successful run number and this is false.
- ``abort_on_build_fail`` If any of the requested builds fail, aborts the entire process. Defaults to false if not 
explicitly declared.

### Missing features:
Deploying is not yet done. Once the docker image is pushed, one must manually deploy. You can use Portainer to do it.