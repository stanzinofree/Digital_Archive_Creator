#!/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'Alessandro'
__version__ = ''
__first_release__ = '20/08/13'

DESCRIPTION

"""
import yum
import platform
import subprocess
import tempfile
import shutil
import os
from sys import exit
import time
import subprocess
from libs.color_shell import CODE, termcode, colorstr, formatter

forma= formatter() 
yp = yum.YumBase()

#Remove package if you have custom installation of follow softwares
package = ["wget", "python-setuptools", "make", "gcc", "MySQL-python", "libxslt", "python-devel","pyOpenSSL"]

cmds_redis = ["tar xvf redis-2.6.14.tar.gz",
        "make -C ./redis-2.6.14/",
        "mkdir /etc/redis /var/lib/redis",
        "cp ./redis-2.6.14/src/redis-server ./redis-2.6.14/src/redis-cli /usr/local/bin",
        "cp ./redis-2.6.14/redis.conf /etc/redis",
        "mv redis-server /etc/init.d/",
        "chmod 755 /etc/init.d/redis-server",
        "chkconfig --add redis-server",
        "chkconfig --level 345 redis-server on",
        "echo 'vm.overcommit_memory = 1' >> /etc/sysctl.conf",
        "sysctl vm.overcommit_memory=1",
        "service redis-server start"
        ]
cmds_wkhtml_64 = ["tar xvf wkhtmltopdf-0.11.0_rc1-static-amd64.tar.bz2",
                 "mv wkhtmltopdf-amd64 /usr/bin/wkhtmltopdf"
                 ]
cmds_wkhtml_32 = ["tar xvf wkhtmltopdf-0.11.0_rc1-static-i386.tar.bz2",
                 "mv wkhtmltopdf-amd64 /usr/bin/wkhtmltopdf"
                 ]

def welcome():
    os.system('cls' if os.name=='nt' else 'clear')
    message = forma.banner()
    message += forma.line("Welcome to installer for OCS_DAC v.3")
    message += forma.line("Author: Middei Alessandro")
    message += forma.line("Info: www.stanzinofree.net/ocs_dac/")
    message += forma.banner()
    message += forma.empty()
    message += forma.line("The first step is checking the dependency for OCS DAC v.3")
    message += forma.line("If some library or system package will missing this script provides in it's installation")
    message += forma.line("The author of this software is not legally responsable for damage occured in authomatic installation")
    message += forma.line("of the missing package, to know the package requirements read the readme.md file")
    message += forma.empty()
    color="BLUE"
    print (colorstr(message, color))
    time.sleep( 1 )

def check_root():
    color="BLUE"
    message = forma.line("Check if user is root: ")
    print (colorstr(message, color))
    time.sleep( 1 )
    if os.geteuid() != 0:
        color="RED"
        message = forma.line("WARNING: you have launched this script with user different from root")
        message += forma.line("now this script stop his operationes so you can launch it as root")
        print (colorstr(message, color))
        exit()
    else:
        color = "GREEN"
        message = forma.line("TEST PASSED!!!!")
        print (colorstr(message, color))

def check_package(pck=package):
    color="RED_BG"
    #choise=raw_input(colorstr("Installare i software non presenti sul sistema? (Y/n): ", color))
    choise="Y"
    color="BLUE"
    message = forma.line("Check for system package dependecies: ")
    print (colorstr(message, color))
    count = 0
    for i in pck:
        color="YELLOW"
        count += 1
        temp_message= "Check if "+i+" is installed: "
        message = forma.line(temp_message)
        print (colorstr(message, color))
        time.sleep( 1 )
        if yp.rpmdb.searchNevra(name=i):
            color="GREEN"
            temp_message = "TEST PASSED: "+i+" is installed"
            message = forma.line(temp_message)
            print (colorstr(message, color))
        else:
            color="RED"
            temp_message = "TEST FAILED: "+i+" is not installed"
            message = forma.line(temp_message)
            print (colorstr(message, color))
            if choise == "Y" or "y":
                yp.install(pattern=i)
    yp.buildTransaction()
    yp.processTransaction()

def runCommands():
    tmp_dir="./tmp_install"
    os.chdir(tmp_dir)
    cpu_info=platform.processor()
    #Iterates over list, running statements for each item in the list
    color="YELLOW"
    temp_message= "Start operation for Redis installation:"
    print (colorstr(temp_message, color))
    for cmd in cmds_redis:
        subprocess.call(cmd, shell=True)
    temp_message= "I found this CPU class: "+cpu_info
    print (colorstr(temp_message, color))
    if cpu_info == "x86_64":
        temp_message= "Starting 64Bit installation of WkhtmlToPdf:"
        print (colorstr(temp_message, color))
        for cmd in cmds_wkhtml_64:
            subprocess.call(cmd, shell=True)
    else:
        temp_message= "Starting installation of 32Bit version of WkhtmlToPdf:"
        print (colorstr(temp_message, color))
        for cmd in cmds_wkhtml_32:
            subprocess.call(cmd, shell=True)
    os.chdir("../")
    try:
        shutil.rmtree(tmp_dir)  # delete directory
    except OSError as exc:
        if exc.errno != 2:  # code 2 - no such file or directory
            raise  # re-raise exception

def launch_setup():
    command=" echo \"* */2 * * * echo ' '>/dev/null\" > /var/spool/cron/root"
    color="BLUE"
    temp_message= "Start remain operations:"
    print (colorstr(temp_message, color))
    subprocess.call(command,shell=True) 
    subprocess.call("python ./libs/setup_modules.py", shell=True)
    subprocess.call("python ./libs/setup_config.py", shell=True)

if __name__ == '__main__':
    welcome()
    check_root()
    check_package()
    runCommands()
    launch_setup()