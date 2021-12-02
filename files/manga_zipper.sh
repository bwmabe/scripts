#!/usr/bin/env bash

for I in $(fd --type d --max-depth 1); do cd $I; for J in $(fd --type d --max-depth 1 "Vol"); do zip $J.zip $J/*/* > /dev/null; mv $J.zip $J.cbz; done; cd ..; done
