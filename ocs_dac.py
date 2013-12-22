#!/bin/python
# -*- coding: utf-8 -*-
"""
core library to query OCS and extract pdf or html data

"""

import libs.log
import libs.local_variables
import libs.db_connection
import libs.ocs_config_parse
import libs.remove_files
import libs.retrieve_scheda

#Come prima cosa dobbiamo pulire le cartelle temporanee
#remove_files

#Iniziamo a connetterci al db e tirare fuori le schede
#Pulisco il db sqlite,





#We use this python standard modules: filecmp, os, subprocess, optparse, time, xml.dom
#And this custom module written for the software: send_mail and backup
#echo "http://localhost/ocsreports/index.php?function=export_ocs&no_header=1&systemid=46" | awk '{split($0,a,"="); print a[4]}'

#The firse routine that we have to write is the check of db credentials, if they exist we write in a vector the data, if they don't exist we create the file and read it
#This will be place in main but now we need it

#The first part of our program





# def check_file(config):
#     try:
#         test = open(config, 'r')
#     except IOError:
#         command = "bash " + local_variables.config_sh + " " + local_variables.conf_file + "db.inc.php"
#         subprocess.call(command, shell=True)

if __name__ == "__main__":
    logger = libs.log.logging(libs.local_variables.log_file)
    logger.start()
    sched = libs.retrieve_scheda.scheda("/opt/ocs3/uploads/ocs.xsl")
    connectdb = libs.db_connection.connect_db()
    cursor = connectdb.cursor()
    cursor.execute("SELECT ID,DEVICEID,NAME FROM hardware")
    valid_id = []
    for record in cursor.fetchall():
        scheda_id = str(record[0])
        name_id = str(record[2])
        valid_id.append(scheda_id)
    connectdb.close()
    for i in valid_id:
        sched.retrieve(i)
    logger.close()