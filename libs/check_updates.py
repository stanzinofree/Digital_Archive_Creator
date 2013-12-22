#!/bin/python
# -*- coding: utf-8 -*-
"""
*Version* : *0.1.0*

Questo modulo si occupa di creare i pdf per le schede quando trova i checksum modificati nel db

i db usati sono:
0 - Retrieve ID: (scheda_id : (nome_pc : checksum)) e (nome_pc : scheda_id) e ((nome_pc : checksum) : scheda_id)
5 - information for home_page

Classi:
CheckUpdate

Le funzioni:
retrieve_id
check_cheksum
check_exist_check0
check_exist_check_not0
set_checksum_0
prepare_result

Routine se lanciato da solo:
check = CheckUpdate()
check.retrieve_id()
check.prepare_result()

"""

import re
import redis
import time
import log
import db_connection
import retrieve_scheda
import html_and_archive
import os
import local_variables

#db0 Retrieve ID: (scheda_id : (nome_pc : checksum)) e (nome_pc : scheda_id) e ((nome_pc : checksum) : scheda_id)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
#db5 Informations for home_page
w = redis.StrictRedis(host='localhost', port=6379, db=5)
#Inizialization for log class
log_class = log.logging()
#Inizialization for retrieve_scheda class
sch = retrieve_scheda.scheda()
#Inizialization for html class
html = html_and_archive.html()

#start our main class
class CheckUpdate:
    """
    Called Functions:
    -retrieve_id
    -check_cheksum
    -check_exist_check0
    -check_exist_check_not0
    -set_checksum_0
    -prepare_result
    """
    #when Inizializate do nothing
    def __init__(self):
        pass
    #
    def retrieve_id(self):
        """
        This function set the last update check in db 5,
        Connect to OCS_Mysql DB and select valid id and theri checksum,
        after this set the information collected in a redis db0
        close the db connection and log the operations on db_log  
        """
        last_check=time.strftime("%H:%M - %d/%m/%Y")
        w.set("last_check",last_check)
        log_class.normal("Inizio retrieve degli id validi dal db")
        connectdb = db_connection.connect_db()
        cursor = connectdb.cursor()
        cursor.execute("SELECT ID,NAME,CHECKSUM FROM hardware")
        valid_id = []
        for record in cursor.fetchall():
            scheda_id = str(record[0])
            nome_id = str(record[1])
            check_id = str(record[2])
            valid_id.append(scheda_id)
            vector_temp = nome_id + ":" + check_id
            r.set(scheda_id, vector_temp)
            r.set(nome_id, scheda_id)
        connectdb.close()
        log_class.normal("Fine raccolta id validi dal db")
        for i in valid_id:
            self.check_cheksum(i)

    def check_cheksum(self, id):
        """
        id -> int
        
        This function take in input the ID(int),
        get the value from db0 using id as key,
        parse the result as yaml syntax and then check if 
        checksum is 0 or not.
        If checksum is 0 call check_exist_check0 function
        otherwise call check_exist_check_not0

        """
        tem = r.get(id)
        tem_yaml = re.search(r'(.+):(.+)', tem)
        tem_check = tem_yaml.group(2)
        #print tem_yaml.group(1)
        tem_name=tem_yaml.group(1)
        if tem_check == "0":
            self.check_exist_check0(id, tem_name)
            #print tem_check+" e' uguale a 0"
        else:
            #print tem_check+" non e' 0"
            self.check_exist_check_not0(id, tem_name)

    def check_exist_check0(self, id, tem_name):
        """
        id -> int
        tem_name -> string
        
        This function take in input the ID(int), and tem_name(str)
        try to open the xml file generated from past execution otherwise call
        sch.retrieve(id) and set checksum to 0
        """
        try:
            open(local_variables.expfol + tem_name + ".xml", "r")
        except IOError:
            sch.retrieve(id)
            self.set_checksum_0(id)


    def check_exist_check_not0(self, id, tem_name):
        #print "inizio ciclo per lid "+id
        #print tem_name
        try:
            open(local_variables.expfol + tem_name + ".xml", "r")
            #print tem_name
            html.archive(tem_name)
            sch.retrieve(id)
            self.set_checksum_0(id)
        except IOError:
            sch.retrieve(id)
            self.set_checksum_0(id)

    def set_checksum_0(self, id):
        connectdb = db_connection.connect_db()
        cursor = connectdb.cursor()
        check_zero = str(0)
        cursor.execute("SELECT ID,CHECKSUM FROM hardware where ID=" + id)
        for i in cursor.fetchall():
            cursor.execute("UPDATE hardware SET CHECKSUM=" + check_zero + " where ID=" + str(id))
            connectdb.commit()
        connectdb.close()
        log_class.normal("Reset del checksum a 0 per l'id: " + id)

    def prepare_result(self):
        path, dirs, files=os.walk(local_variables.exportweb).next()
        filecount=len(files)
        old_filecount=w.get("filecount")
        if old_filecount == None:
            new_filecount = filecount
        else:
            new_filecount=int(filecount)-int(old_filecount)
        w.set("filecount", filecount)
        w.set("new_files", str(new_filecount))

if __name__ == "__main__":
    log_class.start()
    check = CheckUpdate()
    check.retrieve_id()
    check.prepare_result()
    log_class.close()