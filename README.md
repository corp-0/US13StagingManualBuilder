# US13 Staging Manual Builder

A script for this times of need

This script will attempt to build and publish a new version to Staging server and our CDN.
Just check everything is alright in ``config.json`` and set these environmental variables:

- ``SSH_PRIVATE_KEY``
- ``HUB_USERNAME`` 
- ``SSH_USER`` 
- ``SSH_KNOWN_HOSTS`` 
- ``HUB_PASSWORD`` 
- ``ERROR_WEBHOOK`` 
- ``CDN_HOST`` 
- ``CDN_USER`` 
- ``DOCKER_USERNAME`` 
- ``DOCKER_PASSWORD`` 

You could also set these in your ``config.json`` but it is kinda unsecure.

## Features
- [x] Config file to set all the shiet
- [x] Error handling
- [x] Basic logs
- [x] Builds to all 3 supported platforms
- [ ] Makes the docker image and updates it
- [ ] Uploads to CDN 

## Dependencies:
- Python >3.6
- Internet connection
- Docker
- Unity
- Unitystation repo with latest develop at the moment of build
