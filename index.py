#!/usr/bin/python
# -*- encoding: UTF-8 -*-
#
#Import section
import os
import re
import time
import subprocess

import cherrypy
import simplejson
from cherrypy.lib.static import serve_file
from cherrypy.process.plugins import PIDFile
import redis

from base_config import html_header
from base_config import html_footer
from base_config import html_logged_header
import libs.local_variables
import libs.log_term
import libs.archive_rpc
import libs.retrieve_scheda
import libs.html_and_archive
from auth import AuthController, require, member_of



sch = libs.retrieve_scheda.scheda()
versione = libs.local_variables.versione()
html_r = libs.html_and_archive.html()

r = redis.StrictRedis(host='localhost', port=6379, db=3)
s = redis.StrictRedis(host='localhost', port=6379, db=0)
q = redis.StrictRedis(host='localhost', port=6379, db=2)
v = redis.StrictRedis(host='localhost', port=6379, db=1)
l = redis.StrictRedis(host='localhost', port=6379, db=6)
w = redis.StrictRedis(host='localhost', port=6379, db=5)

p = PIDFile(cherrypy.engine, libs.local_variables.pid_file)
p.subscribe()

#Function to list all file in html folder
def list_htm():
    list = os.listdir(libs.local_variables.exportweb)
    for elem in list:
        q.set(elem, elem)

#This section describe the RestricteArea for ocs_dac
class RestrictedArea:
    _cp_config = {
        'auth.require': [member_of('admin')]
    }

    @cherrypy.expose
    def index(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = """
                    """
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html


class Root:
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()

    restricted = RestrictedArea()

    #Index Page, we inert directly login form
    def index(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        filecount = w.get("filecount")
        new_pc = w.get("new_files")
        last_check = w.get("last_check")
        versione = libs.local_variables.versione()
        print filecount
        print versione

        html_body = ("<div class='col_12'><div class='tab-content clearfix'><div class='col_3'></div><div class='col_6'>"
                            "<table cellspacing='0' cellpadding='0' class='striped'>"
                            "<tbody><tr><td>Computer Censiti</td>"
                                "<td>" + filecount + "</td></tr>"
                            "<tr><td>Computer Nuovi</td>"
                                "<td>" + new_pc + "</td></tr>"
                            "<tr><td>Last Check:</td>"
                                "<td>" + last_check + "</td></tr>"
                            #"<tr><td>OCS_DAC Version:</td>"
                            #    "<td>" + versione + "</td></tr>"
                            "</tbody></table></div><div class='col_3'></div>"
                        "</div></div></div>")
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    index.exposed = True


    @require(member_of('admin'))
    def start(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = "BENVENUTO " + str(nome)
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    start.exposed = True

    @require(member_of('admin'))
    def test(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        # NElla form è stato tolto il seguente bottone e attivato come javascript <input type="submit" value="Invio" class="small blue" style="display:hide"/>
        html_body = """
                            <div class="col_12">
                                <div class="col_8">
                                <div class="terminal">
                                <form id="command" action="#" method="post">
                                <span />
                                <div id=pyterm></div>
                                <label for="log_list" class="col_2 column">Scegli il log: </label>
                                <input type="text" id="log_list" class="col_6 column"/><br>
                                <label for="promptt" class="col_2 column">Digita il comando: </span>
                                <input type="text" id="prompt" class="col_6 column" autocomplete="off"/><br>
                                <input id="submit_log" type="submit" value="Invio" class="small blue"/>
                                <input id="calc" type="text" value="0">
                                </span />
                                </form>
                                <div id="terminal" class="terminal" style="height: 400px; overflow-y: scroll;"></div>
                                </div></div>
                                <div class="col_4">
                                <div id="help">
                                <h5>Guida ad OCS DAC terminal</h5>
                                <p>
                                Fare click sulla funzione per vedere l'help
                                oppure digitare <code>help</code> nella shell
                                </p>
                                <blockquote class="small">
                                <code id="cathide">cat</code>
                                <div class="catshow" style="display:none">
                                <p>
                                Questo comando mostra tutto il log selezionato dall'inizio alla fine.
                                </p></div>
                                </blockquote>
                                <blockquote class="small">
                                <code id="headhide">head</code><br>
                                <code>head N</code>
                                <div class="headshow" style="display:none">
                                <p>
                                Questo comando mostra le prime N righe del file di log selezionato.
                                Nel caso non si indicasse un valore dopo head, N sara' uguale a 10.<br>
                                Esempio: <code>head 5</code> mostra le prime 5 righe del log
                                </p></div>
                                </blockquote>
                                <blockquote class="small">
                                <code id="tailhide">tail</code><br>
                                <code>tail N</code>
                                <div class="tailshow" style="display:none">
                                <p>
                                Questo comando mostra le ultime N righe del file di log selezionato.
                                Nel caso non si indicasse un valore dopo tail, N sara' uguale a 10.<br>
                                Esempio: <code>tail 5</code> mostra le ultime 5 righe del log
                                </p></div>
                                </blockquote>
                                <blockquote class="small">
                                <code id="grephide">grep</code><br>
                                <code>igrep</code>
                                <div class="grepshow" style="display:none">
                                <p>
                                Questo comando cerca il termine successivo nei log, se si vuole usare la versione
                                case insensitive si deve usare il comando igrep seguito dalla parola da cercare<br>
                                Esempio: <code>grep Avvio</code> trova tutte le righe che contengono Avvio ma non avvio<br>
                                Esempio: <code>igrep Avvio</code> trova tutte le righe che contengono Avvio o avvio
                                </p></div>
                                </blockquote>
                                </blockquote>
                                <blockquote class="small">
                                <code id="dumphide">dump</code><br>
                                <div class="dumpshow" style="display:none">
                                <p>
                                Questo comando genera un link nella shell che permette il download del file di Log
                                in modo da poter essere salvato od analizzato in maniera piu' approfondita
                                </p></div>
                                </blockquote>
                                </div>
                                </div>
                            </div>

                                """
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    test.exposed = True

    @require()
    def search_schede(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = """
                            <div class="col_12">
                                <div class="col_3">

                                <form id="testform" action="#" method="post">
                                                <p>
                                                <input type="text" id="search" /><br>
                                                <input type="submit" value="Scegli" />
                                                </p>

                                </form>
                                <div id="title"></div>
                                <div id="archive"></div>
                                </div>
                                <div class="col_9">
                                <div id="preview"></div>
                                </div>
                            </div>

                                """
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    search_schede.exposed = True

    @require()
    def gallery(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = """
                            <div class="col_12">
                                <div class="col_3">

                                <form id="testform" action="#" method="post">
                                                <p>
                                                <input type="text" id="search" /><br>
                                                <input type="submit" value="Scegli" />
                                                </p>

                                </form>
                                <div id="title"></div>
                                <div id="archive"></div>
                                </div>
                                <div class="col_9">
                                <div id="preview"></div>
                                </div>
                            </div>

                                """
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    gallery.exposed = True

    @require()
    @cherrypy.expose
    def submit(self, name):
        list_htm()
        cherrypy.response.headers['Content-Type'] = 'application/json'
        var = q.keys(name)
        return simplejson.dumps(dict(title=var))

    @require()
    @cherrypy.expose
    def log_sub(self, term, log, calc):
        text = libs.log_term.prompt_parse(term, log, calc)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps([text])

    @require()
    @cherrypy.expose
    def sub_temp(self, term):
        list = q.keys(term + "*")
        #print simplejson.dumps([(pn) for pn in list])
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps([(pn[:-4]) for pn in list])

    @require()
    @cherrypy.expose
    def log_list(self, term):
        list = l.keys(term + "*")
        print simplejson.dumps([(pn) for pn in list])
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps([(pn) for pn in list])

    @require()
    @cherrypy.expose
    def sub_calc(self, term):
        absPath = os.path.abspath(libs.local_variables.root_folder + "share/" + term)
        title = """<hr class="alt1" /><h5>Scarica la scheda</h5><br><button class="medium blue pill" onclick="location.href='/Download/?filepath=""" + absPath + """.htm'">Download</button>"""
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps([title])

    @require()
    @cherrypy.expose
    def archive(self, term):
        text = libs.archive_rpc.archive_consult(term)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps([text])

    @require()
    @cherrypy.expose
    def test2(self, command):
        titolo = command
        return simplejson.dumps([titolo])

    @require()
    @cherrypy.expose
    def preview(self, term):
        thu = os.path.abspath(libs.local_variables.root_folder + "img/" + term)
        prev = """<h5>Anteprima della scheda: """ + term + """ </h5>
        <p>Puoi eseguire il download dal bottone a sinistra</p><img class="caption" title="Preview della Scheda" src=\"/View?filepath=/""" + thu + """.png\"/>
</div>"""
        # title="<a href='/Download/?filepath="+absPath+".htm'>"+term+"</a>"
        #print simplejson.dumps([(pn) for pn in list])
        cherrypy.response.headers['Content-Type'] = 'application/json'
        #print simplejson.dumps([title])
        return simplejson.dumps([prev])

    @require()
    @cherrypy.expose
    def Download(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")

    Download.exposed = True

    @require()
    def View(self, filepath):
        return serve_file(filepath, "image/png")

    View.exposed = True

class AdminArea(object):
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    @require()
    @cherrypy.expose
    def View(self, filepath):
        return serve_file(filepath, "image/png")
    View.exposed = True

    @require()
    @cherrypy.expose
    def admin(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = ("<div class='col_12'>"
                        "<div class='col_4'></div>"
                        "<div class='col_4'><h3 class='center'>AREA AMMINISTRATIVA</h3></div>"
                        "<div class='col_4'></div>"
                        "<div class='tab-content clearfix'>"
                        "<div class='col_4'></div>"
                        "<div class='col_4'><ul>"
                        "<li><a href='/admin/upload_form'>Upload CSS</a></li>"
                        "<li><a href='/admin/xsl_view'>Visualizza CSS</a></li>"
                        "<li><a href='/admin/remove_form'>Rimuovi CSS</a></li></ul></div>"
                        "<div class='col_4'></div>"
                        "</div></div>")
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    admin.exposed = True

    """
    Sezione per il form di upload del file xls
    """
    @require()
    def upload_form(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = (
            "<div class='col_12'>"
            "<div class='col_4'></div>"
            "<div class='col_4'><h3 class='center'>CARICA UN FOGLIO DI STILE</h3></div>"
            "<div class='col_4'></div>"
            "<div class='tab-content clearfix'>"
            "<form class='vertical' method='post' action='/admin/upload' enctype='multipart/form-data'>"
            "<div class='col_4'></div>"
            "<div class='col_4'><input type='file' name='myCSS' id='myCSS' /><button class='blue center' id='px-submit' type='submit'>CARICA</button></div></div>"
            "<div class='col_4'></div>"
            "</form>"
            "<script type='text/javascript'>jQuery(function($){$('.fileUpload').fileUploader();});</script>"
            "</div></div>")
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    upload_form.exposed = True

    """
    Funzione di upload vera e propria richiamata dal form di upload
    """
    @require()
    def upload(self, myCSS):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = (
            "<div class='col_12'>"
            "<div class='col_4'></div>"
            "<div class='col_4'><h3 class='center'>CSS CARICATI:</h3></div>"
            "<div class='col_4'></div>"
            "<div class='tab-content clearfix'>"
        )
        cherrypy.response.timeout = 3600
        file_name = myCSS.filename
        size = 0
        allData = ''
        while True:
            data = myCSS.file.read(8192)
            allData += data
            if not data:
                break
            size += len(data)
        savedFile = open(libs.local_variables.css_directory + myCSS.filename, 'wb')
        savedFile.write(allData)
        savedFile.close()
        tem=s.get(10)
        tem_yaml = re.search(r'(.+):(.+)', tem)
        tem_name=tem_yaml.group(1)
        print tem_name, file_name
        html_r.xml_to_pdf_custom(tem_name, file_name)
        comando3="convert "+libs.local_variables.root_folder+"custom_report/img/"+myCSS.filename[:-4]+".png -crop 600x300+0+0 "+libs.local_variables.root_folder+"custom_report/thumb/"+myCSS.filename[:-4]+".png"
        subprocess.call(comando3, shell=True)
        html_body += (
        "<table cellspacing='0' cellpadding='0' class='striped'>"
                "<thead><tr>"
                        "<th>Foglio di Stile</th><th>Data ultima modifica</th><th>Preview Scheda</th>"
                    "</tr></thead>")
        list = os.listdir(libs.local_variables.css_directory)
        if not list:
            html_body += '<p>Errore</p>'
        else:
            for i in list:
                thu=i[:-4]+".png"
                html_body += "<tr><td>" + i + "</td><td>" + time.ctime(os.path.getmtime(libs.local_variables.css_directory + i)) + "</td><td><a href='/admin/View?filepath="+libs.local_variables.root_folder+"custom_report/img/"+thu+"' title='Anteprima foglio di stile: "+thu+"'><img src='image/"+thu+"' alt='' width='200' height='100' /></a></td></tr>"
        html_body += "</table></div></div>"
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html

    upload.exposed = True

    """
    Tabella che mostra i fogli di stile caricati e le anteprime
    """
    @require()
    def xsl_view(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = (
            "<div class='col_12'>"
            "<div class='col_4'></div>"
            "<div class='col_4'><h3 class='center'>CSS CARICATI:</h3></div>"
            "<div class='col_4'></div>"
            "<div class='tab-content clearfix'>"
        )
        html_body += (
        "<table cellspacing='0' cellpadding='0' class='striped'>"
                "<thead><tr>"
                        "<th>Foglio di Stile</th><th>Data ultima modifica</th><th>Preview Scheda</th>"
                    "</tr></thead>")
        list = os.listdir(libs.local_variables.css_directory)
        if not list:
            html_body += '<p>Errore</p>'
        else:
            for i in list:
                thu=i[:-4]+".png"
                html_body += "<tr><td>" + i + "</td><td>" + time.ctime(os.path.getmtime(libs.local_variables.css_directory + i)) + "</td><td><a href='/admin/View?filepath="+libs.local_variables.root_folder+"custom_report/img/"+thu+"' title='Anteprima foglio di stile: "+thu+"'><img src='image/"+thu+"' alt='' width='200' height='100' /></a></td></tr>"
        html_body += "</table></div></div>"
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html
    xsl_view.exposed=True

    @require()
    def remove_form(self):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = (
            "<div class='col_12'>"
            "<div class='col_4'></div>"
            "<div class='col_4'><h3 class='center'>CSS CARICATI:</h3></div>"
            "<div class='col_4'></div>"
            "<div class='tab-content clearfix'>"
            "<form action='/admin/remove' method='post' enctype='multipart/form-data'>"
            "<div class='col_4'></div>"
            "<div class='col_4'>"
            "<fieldset><legend>CSS</legend>"
        )
        list = os.listdir(libs.local_variables.css_directory)
        for i in list:
            html_body += "<input type='radio' name='myCSS' value='"+i+"'/><label for='"+i+"' class='inline'>"+i+"</label><br>"
        html_body += ("<button class='blue center' id='css-submit' type='submit'>RIMUOVI</button></fieldset></div>"
                        "<div class='col_4'></div>"
                        "</form></div></div>")
        if nome == None:
            html = html_header + html_body + footer
        else:
            html = html_logged_header + html_body + footer
        return html
    remove_form.exposed = True


    @require()
    def remove(self, myCSS):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = html_footer(nome)
        html_body = (
            "<div class='col_12'>"
            "<div class='col_4'></div>"
            "<div class='col_4'><h3 class='center'>CSS CARICATI:</h3></div>"
            "<div class='col_4'></div>"
            "<div class='tab-content clearfix'>"
            "<div class='col_4'></div>"
            "<div class='col_4'>"
        )
        if myCSS == "ocs.xsl":
            html_body += ("<div class='notice error'><i class='icon-remove-sign icon-large'></i> ERRORE: Questo CSS non puo' essere rimosso <a href='#close' class='icon-remove'></a></div>"
                        "<ul>"
                        "<li><a href='/admin/upload_form'>Upload CSS</a></li>"
                        "<li><a href='/admin/xsl_view'>Visualizza CSS</a></li>"
                        "<li><a href='/admin/remove_form'>Rimuovi CSS</a></li></ul>"
                        "</div><div class='col_4'></div></div></div>"
                )
            if nome == None:
                html = html_header + html_body + footer
            else:
                html = html_logged_header + html_body + footer
        else:
            comando = "rm -f "+libs.local_variables.css_directory+myCSS
            subprocess.call(comando, shell=True)
            html_body += ("<div class='notice success'><i class='icon-ok icon-large'></i> CSS rimosso con successo <a href='#close' class='icon-remove'></a></div>"
                        "<ul>"
                        "<li><a href='/admin/upload_form'>Upload CSS</a></li>"
                        "<li><a href='/admin/xsl_view'>Visualizza CSS</a></li>"
                        "<li><a href='/admin/remove_form'>Rimuovi CSS</a></li></ul>"
                        "</div><div class='col_4'></div></div></div>"
                )
            if nome == None:
                html = html_header + html_body + footer
            else:
                html = html_logged_header + html_body + footer
        return html
    remove.exposed = True

if __name__ == '__main__':
    root = Root()
    admin = AdminArea()
    
    cherrypy.config.update({'server.socket_host': libs.local_variables.ip,
                            'server.socket_port': int(libs.local_variables.port),
                            'server.ssl_module': "pyopenssl",
                            'server.ssl_certificate': libs.local_variables.ssl_cert_path,
                            'server.ssl_private_key': libs.local_variables.ssl_key_path,
                            'tools.staticdir.debug': True,
                            'log.screen': True,
                            'engine.timeout_monitor.on': False,
                        })
    config = {'/':
    {
        'tools.staticdir.root': libs.local_variables.root_folder,
    },
    '/favicon.ico':
    {
        'tools.staticdir.root': libs.local_variables.root_folder,
    },
    '/css':
    {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'css',
    },
    '/js':
    {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'js',
    },
    }
    config_admin = {'/':
    {
        'tools.staticdir.root': libs.local_variables.root_folder,
    },
    '/image':
    {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'custom_report/thumb',
    },
    }
    cherrypy.tree.mount(root, "/", config=config)
    cherrypy.tree.mount(admin, "/admin", config=config_admin)
    
    if hasattr(cherrypy.engine, 'block'):
        # 3.1 syntax
        cherrypy.engine.start()
        cherrypy.engine.block()
    else:
        # 3.0 syntax
        cherrypy.server.quickstart()
        cherrypy.engine.start()