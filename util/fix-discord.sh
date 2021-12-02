#!/bin/sh

# Fixes discord by changing all xdg-mime type handlers to firefox instead of 
# Chromium like they are by default sometimes
#
# From https://old.reddit.com/r/discordapp/comments/89c881/default_web_browser_setting_not_respected_by/

xdg-mime default firefox.desktop x-scheme-handler/http
xdg-mime default firefox.desktop scheme-handler/http
xdg-mime default firefox.desktop x-scheme-handler/https
xdg-mime default firefox.desktop scheme-handler/https
