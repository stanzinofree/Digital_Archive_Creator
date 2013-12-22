#!/bin/python
# -*- coding: utf-8 -*-
"""
class to check hash for all files for file integrity
"""

import simplejson
import redis
import hashlib
import os
import yaml
from local_variables import root_folder

f= redis.StrictRedis(host='localhost', port=6379, db=7)
c_files=["auth.py","base_config.py"]
c_dir=["etc"]

def versione():
    conf_read = open(root_folder + "etc/version.yaml")
    conf = yaml.safe_load(conf_read)
    main = conf["Version"]
    release = main["release"]
    subversion = main["subversion"]
    patch = main["patch"]
    repo = main["repo"]
    temp_string=release+"."+subversion+"."+patch+"-"+repo
    f.set("version",temp_string)

def check_files(directory):
    for elem in directory:
        try:
            filename=os.listdir(elem)
            for eme in filename:
                try:
                    test=os.listdir(eme)
                    pass
                except:
                    old_hash=f.get(eme)
                    hash_file=hashlib.md5(eme).hexdigest()
                    if old_hash == hash_file:
                        pass
                    else:
                        print "ALERT!!!! File : "+eme+ " - Hash : "+hash_file
                        f.set(eme,hash_file)
        except:
            old_hash=f.get(elem)
            hash_file=hashlib.md5(elem).hexdigest()
            if old_hash == hash_file:
                pass
            else:
                print "ALERT!!!! File : "+elem+ " - Hash : "+hash_file
                f.set(elem,hash_file)

def generate_file():
    chiavi=f.keys()
    text=simplejson.dumps([(elem,f.get(elem)) for elem in chiavi])
    print text
    f.set("files_list_hashing",text)


def expose_update_file():
    text=f.get("files_list_hashing")
    string=f.get("version")
    print text
    print string
    version=simplejson.dumps([string,["files",text]]).replace('\\"',"\"")
    return version

if __name__ == "__main__":
    check_files(c_files)
    check_files(c_dir)
    generate_file()
    versione()
