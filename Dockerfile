FROM mc587/vvs-ubuntu

ARG persistent_data=/opt/vvs
ENV vvs_persistent_data=$persistent_data
ARG input_csv=streams.csv
ENV vvs_input_csv=$input_csv
ARG output_sheet=diamond_sheet.xlsx
ENV vvs_output_sheet=$output_sheet

RUN apt update
RUN apt install -y nginx python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools sudo
RUN python3 -m pip install wheel gunicorn flask

COPY uploader /uploader
COPY nginx/uploader /etc/nginx/sites-available/default
COPY startup.sh /startup.sh
COPY diamond_loop.py /diamond_loop.py
COPY static_check.sh /static_check.sh

VOLUME ${vvs_persistent_data}/
ENTRYPOINT /startup.sh
