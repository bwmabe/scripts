#!/usr/bin/env bash

fd --type f | rg -e "mp4$" | xargs -n1 -d'\n' -i{} adb push -z any {} $1
