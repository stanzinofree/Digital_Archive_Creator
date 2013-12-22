#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from os import kill
import subprocess
try:
    code=urllib.urlopen("https://localhost:8086").getcode()
    if code == 200:
        print "Il sito e' su"
    elif code == 400:
        print "Sito non raggiungibile"
except IOError:
    command="nohup python index.py &"
    subprocess.call(command, shell="True")

if __name__ == "__main__":
    print "CHECKING WEBSITE"