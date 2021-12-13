#!/bin/sh
set -o xtrace

# change alias for download link (nginx) since it's not configured dynamically and i don't know a better way
nginx_config="/etc/nginx/sites-available/default"
sed -i "s#alias analysis.*;#alias ${vvs_persistent_data}/${vvs_analyzer_output};#" "$nginx_config"
sed -i "s#alias search.*;#alias ${vvs_persistent_data}/${vvs_explorer_output};#" "$nginx_config"
if [ -n "$domain_name" ]; then
	sed -i "s#server_name .*;#server_name ${domain_name};#" "$nginx_config"
fi
if [ -e "$vvs_persistent_data/ssl/certificate" ] && [ -e "$vvs_persistent_data/ssl/key" ]; then
	chown www-data:www-data "$vvs_persistent_data/ssl/certificate" "$vvs_persistent_data/ssl/key"
	chmod 400 "$vvs_persistent_data/ssl/certificate" "$vvs_persistent_data/ssl/key"
	sed -i "s#listen 80 default_server;#listen 443 ssl;#" "$nginx_config"
	sed -i "/server_name /a \    ssl_certificate_key $vvs_persistent_data/ssl/key;" "$nginx_config"
	sed -i "/server_name /a \    ssl_certificate $vvs_persistent_data/ssl/certificate;" "$nginx_config"
	#
	printf '
server {
    listen 80 default_server;

    server_name _;

    return 307 https://$host$request_uri;
}
' >>"$nginx_config"
fi

# create skeleton of persistent storage, video parser won't do it but needs it
mkdir -p "$vvs_persistent_data"/;
mkdir -p "$vvs_persistent_data"/stream_results/;
mkdir -p "$vvs_persistent_data"/videofiles/;
mkdir -p "$vvs_persistent_data"/imagefiles/;
mkdir -p "$vvs_persistent_data"/blacklog/;
mkdir -p "$vvs_persistent_data"/frozenlog/;
mkdir -p "$vvs_persistent_data"/staticlogs/;
mkdir -p "$vvs_persistent_data"/log/;
mkdir -p "$vvs_persistent_data"/ffmpeglog/;
mkdir -p "$vvs_persistent_data"/camerafinder/logs;
mkdir -p "$vvs_persistent_data"/camerafinder/nmaplog;

# make sure both web UI & video parser can access persistent storage
chown -R www-data:www-data "$vvs_persistent_data"
chmod -R 0770 "$vvs_persistent_data"

# make the base executable
chmod 0755 /analysis/diamond_loop.py
chmod 0755 /analysis/finding_cameras.py
chmod 0755 /analysis/vvs_api.py

# for correct placement of output spreadsheet

#cd "$vvs_persistent_data"
#sudo -Eu www-data python3 /ui/diamond_loop.py >/opt/vvs/diamond_output.log 2>/opt/vvs/diamond_error.log &

#sleep 2

# start nginx
service nginx start

# for file verification
sudo -Eu www-data /usr/local/bin/gunicorn -D --chdir /ui  --workers 1 --bind unix:/tmp/ui.sock -m 007 --log-file=/tmp/gunicorn.log --log-level DEBUG --enable-stdio-inheritance wsgi:app

# start API service
python3 /analysis/vvs_api.py &

# default bash shell
cd /opt/vvs
/bin/bash
