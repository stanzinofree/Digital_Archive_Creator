#!/bin/python
# -*- coding: utf-8 -*-
"""
class to generate html from xml and archive old schedes
"""

import time
import re
import os
import subprocess

import redis

import log
import local_variables


log_class = log.logging()
r = redis.StrictRedis(host='localhost', port=6379, db=1)


class html():
    def list_files_xml(self, name="ocs.xsl"):
        css = local_variables.upfol+name
        list = os.listdir(local_variables.expfol)
        for item in list:
            filter = re.search(r'(sottorete*)', item)
            #print item
            if item == "_SYSTEM.xml":
                pass
            elif filter:
                pass
            else:
                self.xml_to_pdf(item, css)
        print "conversione avvenuta"

    def xml_to_pdf(self, filename, style):
        comando = "xsltproc -o " + local_variables.exportweb + filename[:-4] + ".htm " + style + " " + local_variables.expfol + filename
        subprocess.call(comando, shell=True)
        comando2 = "wkhtml " + local_variables.root_folder + "share/" + filename[:-4] + ".htm " + local_variables.root_folder + "img/" + filename[:-4] + ".png"
        subprocess.call(comando2, shell=True)

        log_class.normal("Conversione del file: " + filename + " in html avvenuta con successo")

    def xml_to_pdf_custom(self, filename, style):
        comando = "xsltproc -o " + local_variables.export_customweb + filename + ".htm " + local_variables.root_folder+ "uploads/" +style + " " + local_variables.expfol + filename +".xml"
        subprocess.call(comando, shell=True)
        comando2 = "wkhtml " + local_variables.export_customweb + filename + ".htm " + local_variables.root_folder + "custom_report/img/" + style[:-4] + ".png"
        subprocess.call(comando2, shell=True)

        # log_class.normal("Conversione del file: " + file + " in html avvenuta con successo")

    def check_archive(self, name):
        leng = r.llen(name)
        if leng == 3:
            elem = r.lindex(name, 0)
            os.remove(elem)
            r.lpop(name)


    def archive(self, name):
        #print "archive for "+name
        source = local_variables.expfol + name + ".xml"
        source_web = local_variables.exportweb + name + ".htm"
        destination = local_variables.archive + name + time.strftime("_%d_%b_%Y_%H:%M") + ".xml"
        destination_web = local_variables.archive + name + time.strftime("_%d_%b_%Y_%H:%M") + ".htm"
        try:
            self.check_archive(name)
            open(source)
            os.renames(source, destination)
            os.renames(source_web, destination_web)
            r.rpush(name, destination)
        except IOError:
            print "errore nell'apertura del file"
        log_class.normal("Archiviato il file: " + name + ".xml come " + destination + " con successo")


if __name__ == "__main__":
    log_class.start()
    html = html()
    #html.archive("01060-A")
    css=local_variables.upfol+"test.xsl"
    item="00194-A.xml"
    html.xml_to_pdf_custom(item, css)
    log_class.close()
    #check.set_checksum_0("252")


