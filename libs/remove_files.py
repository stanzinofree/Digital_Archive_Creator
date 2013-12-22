#!/bin/python
# -*- coding: utf-8 -*-
"""
utility to remove file in a folder

future improvements: add extension filter

"""

import os
import log
from local_variables import root_folder


log_class = log.logging(local_variables.log_file)


class remove():
    def all(self, dir):
        list = os.listdir(dir)
        log_class.normal("Inizio la rimozione dei file dalla cartella " + dir + " ")
        for file in list:
            try:
                os.unlink(dir + file)
                log_class.normal("Rimosso " + file + " ")
            except:
                log_class.error("Impossibile rimouovere" + file + " ")

    def this_file(self, file):
        try:
            os.unlink(file)
            log_class.normal("Rimosso " + file + " ")

        except:
            log_class.error("Impossibile rimouovere" + file + " ")


if __name__ == "__main__":
    log_class.start()
    rem = remove()
    rem.all(root_folder + "temp/temp/")
    log_class.close()