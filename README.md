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

The docker container currently runs Gunicorn and Nginx, ideally separating those into two containers eventually.
The public facing side of the container is the Nginx server handling static files, authentication, TLS and proxying the connection to Gunicorn.
Gunicorn is running the Flask code for the UI with diamond_loop.py and find_cameras.py treated as external binaries.
Configuration is mostly done by files being present or not in persistent storage, however there are variables defined at the top of the Dockerfile which can be overriden when building the image.


# Requirements
Docker needs to be install on the system.

# Deployment

1. Clone Repo
2. `docker-compose up -d`
- Login
  - default creds are admin:admin
  - you can update the logins file to change the credentials
  - install htpasswd
  - `htpasswd -c logins <user>`

- CSV File
  - csv file headers must be `name,url`
  - take a look at example_csv.csv

- After CSV is imported and the checks are successfully you can access the API Via this URL
  - http://<IP_OR_DOMAIN>/vvsapi
# Troubleshooting

Short of knowing what the problem is ahead of time, troubleshooting most likely involves tracing an error found in one of the below log files to bad data, bad code or both. Gunicorn logs will show errors from the Web backend, the analysis and search scripts have their own logs and Nginx will show errors with proxying, SSL and logins. For the frontend, it's a combination of figuring out where data in it was broken and looking at the broswer development tools (usually F12) for console logging.
  
The main log files can be found at:
  - diamond_loop.py: /opt/vvs/diamond.log
  - Gunicorn: /tmp/gunicorn.log
  - Nginx: /var/log/nginx/{access.log, error.log}
  
Currently, the logging level is hardcoded to DEBUG during development and can be defined in startup.sh for Gunicorn as well as inside the two Python scripts. From the Python logging documentation, the levels are as follows:
- CRITICAL: 50
- ERROR: 40
- WARNING: 30
- INFO: 20
- DEBUG: 10
- NOTSET: 0

The numerically lower levels will print more information.
