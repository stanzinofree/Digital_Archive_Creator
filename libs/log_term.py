#!/bin/python
# -*- coding: utf-8 -*-
#Author: Middei Alessandro
#Date of first relase: 25_07_2013
#Version: 0.1
"""
This function is a rpc for Ajax functionality of log page of OCS_DAC
"""

import re
import os

import redis

import local_variables


r = redis.StrictRedis(host='localhost', port=6379, db=3)
s = redis.StrictRedis(host='localhost', port=6379, db=0)
q = redis.StrictRedis(host='localhost', port=6379, db=2)
v = redis.StrictRedis(host='localhost', port=6379, db=1)
l = redis.StrictRedis(host='localhost', port=6379, db=6)


def prompt_parse(term_cmd, log, calc):
    text = ""
    elements = term_cmd.split(" ")
    print elements
    if elements[0] == "tail":
        try:
            if elements[1]:
                try:
                    index = l.lrange(log, (int(elements[1]) * -1), -1)
                    for i in index:
                        text += i + "<br>"
                except:
                    text += "comando non riconosciuto<br>ES: tail 10"
        except:
            index = l.lrange(log, -10, -1)
            for i in index:
                text += i + "<br>"
    elif elements[0] == "head":
        try:
            if elements[1]:
                try:
                    index = l.lrange(log, 0, (int(elements[1])) - 1)
                    for i in index:
                        text += i + "<br>"
                except:
                    text += "comando non riconosciuto<br>ES: tail 10"
        except:
            index = l.lrange(log, 0, 9)
            for i in index:
                text += i + "<br>"
    elif elements[0] == "cat":
        index = l.lrange(log, 0, -1)
        for i in index:
            text += i + "<br>"
    elif elements[0] == "grep":
        try:
            if elements[1]:
                try:
                    index = l.lrange(log, 0, -1)
                    for i in index:
                        result = re.search(elements[1], i)
                        if result:
                            text += i + "<br>"
                        else:
                            pass
                except:
                    text += "comando non riconosciuto<br>ES: tail 10"
            else:
                text += "Comando non riconosciuto<br>"
        except:
            text += "comando non riconosciuto<br>ES: tail 10"
    elif elements[0] == "igrep":
        try:
            if elements[1]:
                try:
                    index = l.lrange(log, 0, -1)
                    for i in index:
                        result = re.search(elements[1], i, re.IGNORECASE)
                        if result:
                            text += i + "<br>"
                        else:
                            pass
                except:
                    text += "comando non riconosciuto<br>ES: tail 10"
            else:
                text += "Comando non riconosciuto<br>"
        except:
            text += "comando non riconosciuto<br>ES: tail 10"
    elif elements[0] == "dump":
        index = l.lrange(log, 0, -1)
        l_file = open(local_variables.dump + log + ".log", "wr")
        for i in index:
            l_file.write(i)
        absPath = os.path.abspath(local_variables.dump + log)
        text += "<a href='/Download/?filepath=" + absPath + ".log'>Download LOG</a><br>"
        print text
    elif elements[0] == "help":
        try:
            if elements[1] == "cat":
                text += """Questo comando mostra tutto il log selezionato dall'inizio alla fine."""
            elif elements[1] == "head":
                text += """Questo comando mostra le prime N righe del file di log selezionato.
                                Nel caso non si indicasse un valore dopo head, N sara' uguale a 10.<br>
                                Esempio: <code>head 5</code> mostra le prime 5 righe del log"""
            elif elements[1] == "tail":
                text += """Questo comando mostra le ultime N righe del file di log selezionato.
                                Nel caso non si indicasse un valore dopo tail, N sara' uguale a 10.<br>
                                Esempio: <code>tail 5</code> mostra le ultime 5 righe del log"""
            elif elements[1] == "grep":
                text += """Questo comando cerca il termine successivo nei log, se si vuole usare la versione
                                case insensitive si deve usare il comando igrep seguito dalla parola da cercare<br>
                                Esempio: <code>grep Avvio</code> trova tutte le righe che contengono Avvio ma non avvio<br>
                                Esempio: <code>igrep Avvio</code> trova tutte le righe che contengono Avvio o avvio"""
            elif elements[1] == "dump":
                text += """Questo comando genera un link nella shell che permette il download del file di Log
                                in modo da poter essere salvato od analizzato in maniera piu' approfondita"""
        except:
            text += """cat<br>head<br>tail<br>grep<br>dump<br>
                """
        print text
    else:
        text += "Comando non riconosciuto<br>"

    return text