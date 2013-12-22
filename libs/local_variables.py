#!/bin/python
# -*- coding: utf-8 -*-
"""
 This  file is distributed only with pyc to evitate that user modify this settings
This contain all the declaration of variables and export "as variables" the internal path for the application library
"""

# ###Import Section
import yaml
import log
import redis
import ocs_config_parse
"""
We import yaml to parse configuration file, log to interact with logging function and
ocs_config_parse because is our regular expression interpreter for yaml files
"""
log_class = log.logging()

#db5 Informations for home_page
w = redis.StrictRedis(host='localhost', port=6379, db=5)
# ###Version file reading
def versione():
    """
    This function parse the version.yaml file to read the actual version and export the result for all the
    library in sofware that using it

    ### Input

    ### Output
     * **temp_string** (str) : this is a text string with version 

    ### Variable List

     * **conf_read** : this contain stream of yaml file etc/version.yaml
     * **conf** : this contain the yaml load of stream_file
     * **main** : intercept the main section of file
     * **release** : intercept the release section
     * **patch** : intercept the patch section
     * **repo** : intercept the repo section
     * **temp_string** : create the string to export with all version information
    """
    try:
        conf_read = open("etc/version.yaml")
    except IOError:
        try:
            conf_read = open("../etc/version.yaml")
        except IOError:
            print "Impossibile trovare il file di configurazione, riprovare a lanciare l'eseguibile dalla root dell'applicazione"
    conf = yaml.safe_load(conf_read)
    main = conf["Version"]
    release = main["release"]
    subversion = main["subversion"]
    patch = main["patch"]
    repo = main["repo"]
    temp_string=release+"."+subversion+"."+patch+"-"+repo
    return temp_string

def read_conf_file():
    try:
        conf_read = open("etc/config.yaml")
    except IOError:
        try:
            conf_read = open("../etc/config.yaml")
        except IOError:
            print "Impossibile trovare il file di configurazione, riprovare a lanciare l'eseguibile dalla root dell'applicazione"
    conf = yaml.safe_load(conf_read)
    path = conf["Path"]
    root = path["root_folder"]
    server = conf["Server"]
    cf_file = server["conf_file"]
    srv = server["server"]
    administrators= conf["Administrators"]
    user= administrators["user"]
    serv_web = conf["Server_Config"]
    ip = serv_web["ip"]
    port = serv_web["port"]
    ssl = serv_web["ssl"]
    ssl_cert_path = serv_web["ssl_cert_path"]
    ssl_key_path = serv_web["ssl_key_path"]
    pid= conf["PID"]
    pid_file = pid["file"]
    return root, cf_file, srv, user, ip, port, ssl, ssl_cert_path, ssl_key_path, pid_file

def retrieve_credentials():
    find = ocs_config_parse.parse()
    conf_file_temp = read_conf_file()
    config_files = conf_file_temp[1]
    parsed = find.extract_it(config_files)
    db_name = parsed[0]
    db_pwd = parsed[4]
    db_user = parsed[3]
    db_server = parsed[1]

    return db_name, db_pwd, db_user, db_server

version=versione()
retr_dbcon = retrieve_credentials()
db_name = retr_dbcon[0]
db_pwd = retr_dbcon[1]
db_user = retr_dbcon[2]
db_server = retr_dbcon[3]
temp_read=read_conf_file()
admin_user=temp_read[3]

#This section of files define all the internal variables that we use in our project
#We parse the config.yaml files so we know the custom parameters and then we valorize all the local variables
parse_cf = read_conf_file()
root_folder = parse_cf[0]
conf_file = parse_cf[1]
server = parse_cf[2]
ip = parse_cf[4]
port = parse_cf[5]
ssl = parse_cf[6]
ssl_cert_path = parse_cf[7]
ssl_key_path = parse_cf[8]
pid_file = parse_cf[9]

etc = root_folder + "etc/"

var = root_folder + "var/"

css_directory = root_folder + "uploads/"
expfol = root_folder + "temp/"
#export_web
exportweb = root_folder + "share/"
#export_web_one_time
export_customweb = root_folder + "custom_report/share/"
export_customtemp = root_folder + "custom_report/temp/"
#archive
archive = root_folder + "archive/"
archive_web = root_folder + "archive_html/"
#dump log
dump = root_folder + "dump/"
#upload folder
upfol = root_folder + "uploads/"
#version files
version_file="etc/version.yaml"

if __name__ == "__main__":
    print temp_read
    print admin_user
    for i in admin_user:
        print i