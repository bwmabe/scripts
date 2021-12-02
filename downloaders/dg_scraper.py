#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup


if not sys.argv[1:]:
    raise RuntimeError('usage: dg_scraper.py URI')

r = requests.get(sys.argv[1])
s = BeautifulSoup(r.content, "html.parser")
arr = []

for i in s.find_all("a", class_="download-button"):
    arr.append(i["href"])

for i in arr:
    n = i.split("/")[-1]
    line = i[:24] + "/dl" + i[24:]
    print(line)

for i in arr:
    n = i.split("/")[-1]
    line = i[:24] + "/dl" + i[24:]
    f = requests.get(line)
    open(n, "wb").write(f.content)
