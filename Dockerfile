FROM mc587/vvs-ubuntu

#ARG ${VOLUME_NAME}=/opt/vvs
#ENV vvs_persistent_data=$persistent_data
#ARG analyzer_input=streams.csv
#ENV vvs_analyzer_input=$analyzer_input
##ARG analyzer_output=diamond_sheet.xlsx
#ENV vvs_analyzer_output=$analyzer_output
#ARG explorer_output=search.xlsx
#ENV vvs_explorer_output=$explorer_output

RUN apt update
RUN apt install -y nginx python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools sudo iputils-ping nmap
RUN python3 -m pip install wheel gunicorn flask python-nmap pandas requests aniso8601==8.0.0 Flask-RESTful==0.3.8 itsdangerous==1.1.0
#RUN npm -g install imgclip

# web UI
COPY ui /ui
COPY nginx/ui /etc/nginx/sites-available/default
# analysis scripts
COPY analysis /analysis

# COPY htpasswd file to /opt/vvs folder
COPY logins /opt/vvs/
COPY startup.sh /startup.sh

#VOLUME ${vvs_persistent_data}/
ENTRYPOINT /startup.sh
