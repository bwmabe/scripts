#!/usr/bin/env bash

readarray -d '' books < <(find -type f -name "*.epub" -print0)

readarray -d '' titles < <(find -type f -name "*.epub" | sed 's/..Books.//g;s/ (.*//g;s/$/.epub/g' | tr '\n' '\0')

for ((i=0;i<=${#books[@]}-1;i++))
do
	ebook-convert "${books[$i]}" "${titles[$i]}"
done
