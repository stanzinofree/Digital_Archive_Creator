#!/bin/python
# -*- coding: utf-8 -*-
"""
library to implement log function to my software

v. 0.1

"""

import time
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=6)
suffix = time.strftime("%Y_%m_%d")
name = suffix


class logging():
    def start(self):
        r.rpush(name, time.asctime() + " - Avvio scrittura LOG\n")

    def warning(self, message):
        r.rpush(name, time.asctime() + " - WARN: " + message + "\n")

    def error(self, message):
        r.rpush(name, time.asctime() + " - ERROR: " + message + "\n")

    def info(self, message):
        r.rpush(name, time.asctime() + " - INFO: " + message + "\n")

    def normal(self, message):
        r.rpush(name, time.asctime() + " - " + message + "\n")

    def close(self):
        r.rpush(name, time.asctime() + " - Operazione di scrittura LOG Terminata.\n")


if __name__ == "__main__":
    log_class = logging()
    log_class.start()
    log_class.normal("test ciclo scrittura log")
    log_class.warning("Problema sui files")
    log_class.close()