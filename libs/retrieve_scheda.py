#!/bin/python
# -*- coding: utf-8 -*-
"""
class to download ocs schede
"""

import re
import time
import cgi

import yaml
import MySQLdb.cursors

import log
import db_connection
import local_variables
import html_and_archive


log_class = log.logging()
html = html_and_archive.html()


class scheda():
    def read_config_xml(self):
        try:
            f = open(local_variables.etc + "scheda.yaml")
            parse_f = yaml.safe_load(f)
            account = parse_f["Account"]
            components = parse_f["Components"]
            hardware = parse_f["Hardware"]
            softwares = parse_f["Softwares"]
            l_account = []
            l_components = []
            l_hardware = []
            l_softwares = []
            for i, j in dict.items(account):
                if j == 1:
                    l_account.append(i)
                else:
                    pass
            for i, j in dict.items(components):
                if j == 1:
                    l_components.append(i)
                else:
                    pass
            for i, j in dict.items(hardware):
                if j == 1:
                    l_hardware.append(i)
                else:
                    pass
            for i, j in dict.items(softwares):
                if j == 1:
                    l_softwares.append(i)
                else:
                    pass

        except IOError:
            log_class.error("Impossibile leggere il file scheda.yaml")

        return l_account, l_components, l_hardware, l_softwares

    def compone_section(self, section, id):
        """
        This function take as arguments the section and the id and return a text to insert in xml
        """
        #connect to db
        cur = db_connection.connect_db()
        cursore = cur.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursore.execute("SELECT * from " + section + " where HARDWARE_ID=" + id)
        text = ""
        popo = cursore.fetchall()
        #start_sc = time.time()
        text = text + "\t\t\t<" + str.upper(section) + ">\n"
        for i in popo:
            for tr, elem in i.items():
                strutf = str(elem)
                if str(tr) == ("HARDWARE_ID"):
                    pass
                elif str(tr) == ("ID"):
                    pass
                else:
                    #print str(s_elem)
                    #if the element is empty pass otherwise parse the elment in the form
                    if str(elem) == "":
                        pass
                    else:
                        text = text + "\t\t\t\t<" + str(tr) + ">" + cgi.escape(strutf) + "</" + str(tr) + ">\n"
                        #print text
                        #we close the stream of section and return all the text
        text = text + "\t\t\t</" + str.upper(section) + ">\n"
        # end_sc = time.time()
        # time_sc = end_sc - start_sc
        # print text
        # print section + " Execution time ciclo nuovo: " + str(time_sc)
        return text

    def compone_section_hardware(self, section, id):
        """
        This is equla to function before but insert some new tag only for hardware elements
        This function take as arguments the section and the id and return a text to insert in xml
        """
        cur = db_connection.connect_db()
        cursore = cur.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursore.execute("SELECT * from " + section + " where ID=" + id)
        text = ""
        popo = cursore.fetchall()
        #start_sc = time.time()
        text = text + "\t\t\t<" + str.upper(section) + ">\n"
        for i in popo:
            #print i
            data_elem = []
            for tr, elem in i.items():
                strutf = str(elem)
                data_elem.append(str(tr) + ":" + str(elem))
                if str(tr) == ("HARDWARE_ID"):
                    pass
                elif str(tr) == ("ID"):
                    pass
                else:
                    #print str(s_elem)
                    #if the element is empty pass otherwise parse the elment in the form
                    if str(elem) == "":
                        pass
                    else:
                        text = text + "\t\t\t\t<" + str(tr) + ">" + cgi.escape(strutf) + "</" + str(tr) + ">\n"
                        #print text
                        #we close the stream of section and return all the text
        text = text + "\t\t\t</" + str.upper(section) + ">\n"
        #end_sc = time.time()
        #time_sc = end_sc - start_sc
        #print section + " Execution time ciclo nuovo: " + str(time_sc)
        return text


    def retrieve(self, id):
        """
        This is the function that retrieve the tab from db
        """
        log_class.info("Inizio a creare la scheda per l'id " + id)
        elements = self.read_config_xml()
        l_account = elements[0]
        l_components = elements[1]
        l_hardware = elements[2]
        l_softwares = elements[3]
        cur = db_connection.connect_db()
        cursor = cur.cursor()
        cursor.execute("SELECT * from hardware where id=" + id)
        for record in cursor.fetchall():
            name_id = str(record[2])
            fop = open(local_variables.expfol + name_id + ".xml", "w")
            fop.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n")
            fop.write("<REQUEST>\n")
            fop.write("\t<DEVICEID>" + name_id + "</DEVICEID>\n")
            fop.write("\t<CONTENT>\n")
            for i in l_account:
                var = self.compone_section(i, id)
                fop.write(var)
            for q in l_components:
                var = self.compone_section(q, id)
                fop.write(var)
            for s in l_softwares:
                #print s
                var = self.compone_section(s, id)
                fop.write(var)
            for w in l_hardware:
                var = self.compone_section_hardware(w, id)
                fop.write(var)
            fop.write("\t</CONTENT>\n")
            fop.write("\t<QUERY>INVENTORY</QUERY>\n")
            fop.write("</REQUEST>\n")
            fop.close()
            filter = re.search(r'(sottorete*)', name_id)
            if name_id == "_SYSTEM":
                pass
            elif filter:
                pass
            else:
                html.xml_to_pdf(name_id + ".xml", local_variables.upfol+"ocs.xsl")
            log_class.info(time.asctime() + " - file " + name_id + ".xml creato.\n")
        cur.close()


if __name__ == "__main__":
    log_class.start()
    sched = scheda()
    sched.retrieve("275")
    #text=sched.compone_section("softwares","443")
    #text=sched.compone_section("storages","443")
    log_class.close()
