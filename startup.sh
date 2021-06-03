#!/bin/sh

# change alias for download link (nginx) since it's not configured dynamically and i don't know a better way
sed -i "s#alias .*;#alias ${vvs_persistent_data}/${vvs_output_sheet};#" /etc/nginx/sites-available/default

# create skeleton of persistent storage, video parser won't do it but needs it
mkdir -p "$vvs_persistent_data"/;
mkdir -p "$vvs_persistent_data"/stream_results/;
mkdir -p "$vvs_persistent_data"/videofiles/;
mkdir -p "$vvs_persistent_data"/blacklog/;
mkdir -p "$vvs_persistent_data"/frozenlog/;
mkdir -p "$vvs_persistent_data"/staticlogs/;
mkdir -p "$vvs_persistent_data"/log/;
mkdir -p "$vvs_persistent_data"/ffmpeglog/;

# make sure both web UI & video parser can access persistent storage
chown -R www-data:www-data "$vvs_persistent_data"
chmod -R 0770 "$vvs_persistent_data"

# make the base executable
chmod 0755 /diamond_loop.py

# for correct placement of output spreadsheet

cd "$vvs_persistent_data"
sudo -Eu www-data python3 /diamond_loop.py >/opt/vvs/diamond_output.log 2>/opt/vvs/diamond_error.log &

sleep 2

# start nginx
service nginx start

# for file verification
sudo -Eu www-data /usr/local/bin/gunicorn -D --chdir /uploader  --workers 1 --bind unix:/tmp/uploader.sock -m 007 --log-file=/tmp/gunicorn.log wsgi:app

# default bash shell
cd /opt/vvs
/bin/bash
