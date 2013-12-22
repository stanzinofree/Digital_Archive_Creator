#!/bin/python
# -*- coding: utf-8 -*-
"""
This is the utility to connect on db, it create the connection with database and return a vector with cursor and command with db

"""

import MySQLdb
import yaml
import local_variables
import log


log_class = log.logging()


def try_credentials():
    log_class.normal("Prova connession al DB")
    try:
        connect_db()
        log_class.normal("Connessione OK")
    except IOError:
        log_class.error("Impossibile connettersi al DB")


#db_name, db_pwd, db_user, db_server

def connect_db():
    host_temp = yaml.safe_load(local_variables.db_server)
    host = host_temp["SERVER_READ"]
    user_temp = yaml.safe_load(local_variables.db_user)
    user = user_temp["COMPTE_BASE"]
    passwd_temp = yaml.safe_load(local_variables.db_pwd)
    passwd = passwd_temp["PSWD_BASE"]
    db_temp = yaml.safe_load(local_variables.db_name)
    db = db_temp["DB_NAME"]
    db_con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    return db_con


if __name__ == "__main__":
    try_credentials()