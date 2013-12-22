#!/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Alessandro'
__version__ = '1.0'
__first_release__ = '25/07/13'

"""
This module was built to work as rpc damon to serve json answer to ocs_dac web request
"""

#We import redis module
import redis
#Inizialitze v as redis instance for db1
v = redis.StrictRedis(host='localhost', port=6379, db=1)


def archive_consult(term):
    """
    :param term
    """
    v_len = v.llen(term)
    title = """<hr /><h5>Archivio Storico</h5><br>"""
    print v_len
    if v_len != 0:
        for i in v.lrange(term, 0, 3):
            #link="""<button class="tooltip medium blue pill" onclick="location.href='/Download/?filepath="""+ term[:-4] +""".htm'">Download</button>"""
            data = i[26:-4]
            convert = data.split("_")
            day = convert[0]
            month = convert[1]
            year = convert[2]
            hour = convert[3]
            form_data = day + " " + month
            title += """
                    <blockquote class="small">
                    <p>
                    Data: """ + form_data + """
                    Anno: """ + year + """
                    Ora: """ + hour + """
                    <span><button class="medium orange pill" onclick="location.href='/Download/?filepath=""" + i[:-4] + """.htm'">Download</button></span>
                    </p>
                    </blockquote>"""
    else:
        title += """
                <blockquote class="small">
                <p>Non ci sono schede archiviate per questo computer
                </p>
                </blockquote>"""
    return title