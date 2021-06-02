#!/bin/bash

STATICLOGS="$vvs_persistent_data/staticlogs/"
VIDEOFILES="$vvs_persistent_data/videofiles/"

ls -1 "$VIDEOFILES" | while read video; do
	convert "$VIDEOFILES/$video" -colorspace HSL -channel S -separate -format '%M avg sat=%[fx:int(mean*100)]\n' info: > "$STATICLOGS/$video".log
	#TODO: verify this line is supposed to have a -i
	sed -i '1,200d' "$STATICLOGS/$video".log
done

ls -1 "$STATICLOGS" | while read logs; do
	sed -i '$!d' "$STATICLOGS/$logs"
done
