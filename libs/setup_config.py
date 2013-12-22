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
import time
import yaml
from color_shell import CODE, termcode, colorstr, formatter
forma= formatter() 

def rewrite_config():
    color="BLUE"
    message = forma.line("Ora modifichiamo il file di configurazione: ")
    print (colorstr(message, color))
    print os.getcwd()
    config_file="./etc/config.yaml"
    open_file=open(config_file,"r")
    conf=yaml.safe_load(open_file)
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
    open_file.close()
    writer=open(config_file,"w")     
    path["root_folder"] = os.getcwd()
    server["conf_file"]=raw_input(colorstr("Inserisci il path completo del file di configurazione di ocs: (esempio: /usr/share/ocsinventory-reports/ocsreports/dbconfig.inc.php) ", color))
    serv_web["ip"]=raw_input(colorstr("Inserisci l'ip su cui il server deve rispondere: (esempio: 0.0.0.0 per ascoltare su tutti gli ip) ", color))
    port = serv_web["port"]=raw_input(colorstr("Inserisci la porta su cui ascoltera' OCS_DAC: (esempio: 8086 - ricordati di aprirla su iptables) ", color))
    serv_web["ssl_cert_path"]=raw_input(colorstr("Inserisci il path completo del file cert per l'ssl: (esempio: /etc/pki/tls/certs/server.crt) ", color))
    serv_web["ssl_key_path"]=raw_input(colorstr("Inserisci il path completo del file key per l'ssl: (esempio: /etc/pki/tls/private/server.key) ", color))
    yaml.safe_dump(conf,writer,default_flow_style=False)
    writer.close()

def install_routine():
    tmp_file="/tmp/nohup.out"
    try:
        open(tmp_file,"w")
    except IOError:
        color="RED"
        message = forma.line("Errore nel creare il file nohup.out")
        print (colorstr(message, color))


def close_install():
    os.system('cls' if os.name=='nt' else 'clear')
    message = forma.banner()
    message += forma.line("L'installazione e' finita")
    message += forma.line("si consiglia il riavvio del server prima di avviare il login web")
    message += forma.banner()
    message += forma.empty()
    message += forma.empty()
    color="BLUE"
    print (colorstr(message, color))
    time.sleep( 1 )

if __name__ == '__main__':
    rewrite_config()
    close_install()