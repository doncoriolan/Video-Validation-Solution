# Video-Validation-Solution
VVS is intended for analysing camera streams for inactivity, lack of/broken output and similar in an automated fashion.

It is based on ffmpeg and uses RTSP for media transport, written in Python.

# Input
Input is handled by a CSV formatted with 2 columns (arbitrary name, URL of RTSP stream)

# Deployment
Currently, Docker containers are used to deploy the script. The base image is mc587/vvs-ubuntu and a Dockerfile is present to add the necessary files for the web UI and the analysis script with a startup script that handles starting all services. The created image can be used on its own as a self hosted analysis tool, with persistent storage that can be used to keep the working directory of the vvs script. 
