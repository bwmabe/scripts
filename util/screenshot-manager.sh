#!/usr/bin/env bash

image_regex=".*\.png$"

inotifywait -m ~ -e create -e moved_to | 
	while read -r dir _ filename
	do
		if [[ $filename =~ $image_regex ]]
		then
			sleep 1.5s
			width=$(identify -format "%w" "$dir$filename")
			# height=$(identify -format "%h" "$dir$filename")
			if [[ $width -eq 3840 ]]
			then
				mkdir -p Screenshots
				newfname=Screenshots/$(date +"ss_%Y_%m_%d_%H_%M_%S").png
				convert -crop 1920x1080+1920+0 "$dir$filename" "$dir$newfname"
				rm "$dir$filename"
			fi
		fi
	done
