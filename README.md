# Video-Validation-Solution
VVS is intended for analysing camera streams for camera defects in an automated fashion.

It is based on ffmpeg and uses RTSP for media transport, with a HTML UI using Nginx and a backend written with Flask/Python.

The backend has two main features being able to consume CSV sheets to run analysis on or to search for cameras on a given subnet.

# Camera Analysis

Input is handled by uploading a CSV listing the names and addresses of cameras. The output can be either viewed through the Web UI or downloaded as an Excel sheet.

# Camera Search

Input is in the form of a subnet directly in the Web UI. Results can also be viewed through the web or downloaded as an Excel sheet.

# Overview
Currently, Docker containers are used to deploy the script. The base image is mc587/vvs-ubuntu and a Dockerfile is present to add the necessary files for the web UI and the analysis script with a startup script that handles starting all services. The created image can be used on its own as a self hosted analysis tool, with persistent storage that can be used to keep the working directory of the vvs script. 

There is a Github action for generating Docker images which can be pulled with a PAT.

The docker container currently runs Gunicorn and Nginx, ideally separating those into two containers eventually.
The public facing side of the container is the Nginx server handling static files, authentication, TLS and proxying the connection to Gunicorn.
Gunicorn is running the Flask code for the UI with diamond_loop.py and find_cameras.py treated as external binaries.
Configuration is mostly done by files being present or not in persistent storage, however there are variables defined at the top of the Dockerfile which can be overriden when building the image.

# Deployment

1. Obtain a VPS connected to the internet, allow inbound TCP 80 & TCP 443, get a [PAT](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) and [configure](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) it
1. Pull docker image can be found on the registry [page](https://github.com/mc587/Video-Validation-Solution/pkgs/container/vvs-container)
1. Create persistent storage with the command `docker volume create persistent_data`, the name of the volume can be changed but needs to be kept consistent in later steps
1. Create a logins file with the command `htpasswd -c logins <user>` defining a username in the command and putting the password in the interactive prompts. The file needs to be placed in the persistent storage from the host, by default under /var/lib/docker/volumes/<name>/_data/logins
1. If necessary, place ssl certificates in <persistent>/ssl/certificate and <persistent>/ssl/key for the certificate and key respectively
1. Image can now be tested using `sudo docker run -p80:80 -p443:443 --mount source=persistent_data,target=/opt/vvs -it <image id>`, an `--rm` can be used to automatically destroy the container after it's shutdown to limit changes only to persistent storage
1. Once successfully tested the container can be started headless
