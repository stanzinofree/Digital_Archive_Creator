#!/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'Alessandro'
__version__ = ''
__first_release__ = '20/08/13'

DESCRIPTION

"""
import subprocess
import os
from setuptools.command import easy_install
from color_shell import CODE, termcode, colorstr, formatter
forma= formatter() 

easy_pack = ["cherrypy", "simplejson", "pyyaml", "python-crontab", "redis"]

def easy(eas=easy_pack):
    color="BLUE"
    message = forma.line("Install i moduli di Python: ")
    print (colorstr(message, color))
    for i in eas:
        temp_message= "Installazione di "+i+" in corso: "
        message = forma.line(temp_message)
        print (colorstr(message, color))
        easy_install.main(["-U", i])
    message = forma.line("moduuli installati correttamente!!")
    print (colorstr(message, color))

if __name__ == '__main__':
    easy()