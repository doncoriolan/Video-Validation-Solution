#!/bin/bash

clear
STATICLOGS=/opt/vvs/staticlogs/*
VIDEOFILES=/opt/vvs/videofiles/*

for video in $VIDEOFILES
do
clear
	convert "$video" -colorspace HSL -channel S -separate -format '%M avg sat=%[fx:int(mean*100)]\n' info: > "$video".log
sed '1,200d' "$video".log
done

mv /opt/vvs/videofiles/*.log /opt/vvs/staticlogs/

for logs in $STATICLOGS
do
	sed -i '$!d' "$logs"
done
