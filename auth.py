# -*- encoding: UTF-8 -*-
"""
*Version* : *0.1.4*

This lib give the api for the autentication and consultation of user



"""

import hashlib
import string
import random
import cherrypy
import redis
import libs.db_connection
import libs.local_variables
from base_config import html_header


r = redis.StrictRedis(host='localhost', port=6379, db=3)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


SESSION_KEY = '_cp_username'


def check_credentials(username, password):
    """
    Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure
    """
    
    cur = libs.db_connection.connect_db()
    cursor = cur.cursor()
    quer = "SELECT * FROM operators WHERE ID='" + username + "'"
    cursor.execute(quer)
    passwords = []
    for record in cursor.fetchall():
        pwd = str(record[3])
        nome = str(record[1] + " " + record[2])
        passwords.append(pwd)
        r.set(username, nome)
    cursor.close()

    pwd = hashlib.md5(password).hexdigest()
    try:
        passwords[0]
    except IndexError:
        msg = "Username does not exist".encode('utf-8')
        username = None
        return msg, username
    if pwd == passwords[0]:
        return None
    else:
        msg = "Incorrect username or password.".encode('utf-8')
        return msg


def check_auth(*args, **kwargs):
    """
    A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill
    """
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/auth/login")
        else:
            raise cherrypy.HTTPRedirect("/auth/login")


cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)


def require(*conditions):
    """
    A decorator that appends conditions to the auth.require config
    variable.
    """

    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f

    return decorate


def member_of(groupname):
    def check():
        # replace with actual check if <username> is in <groupname>
        admin = libs.local_variables.admin_user
        print admin
        print cherrypy.request.login
        if groupname == "admin":
            for i in admin:
                try:
                    return cherrypy.request.login in admin
                except:
                    pass
        else:
            return cherrypy.request.login in groupname
    return check


def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login

# These might be handy

def any_of(*conditions):
    """Returns True if any of the conditions match"""

    def check():
        for c in conditions:
            if c():
                return True
        return False

    return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""

    def check():
        for c in conditions:
            if not c():
                return False
        return True

    return check


# Controller to provide login and logout actions

class AuthController(object):
    def on_login(self, username):
        """Called on successful login"""

    def on_logout(self, username):
        """Called on logout"""

    def get_loginform(self, username, msg="", from_page="/"):
        key = cherrypy.session.get('_cp_username')
        nome = r.get(key)
        footer = u"""
                </div><div class="clear"></div>
              <div id="footer">
              <div class="grid flex">
              <div class="col_10">&copy; Copyright 2012–2013 All Rights Reserved.</div>
              <div class="col_2">Utente: Anonimo</div>
              </div></div></body></html>"""

        html_body = ""
        if msg == "":
            html_body += """
                     <div class="col_12">
                        <div class="col_4"></div>
                        <div class="col_4"><h3 class="center">ACCESSO</h3></div>
                        <div class="col_4"></div>
                        <div class="tab-content clearfix">
                            <form class="vertical" method="post" action="/auth/login">
                            <div class="col_4"></div>
                            <div class="col_4"><input type="hidden" name="from_page" value="%(from_page)s " />%(msg)s<br />
                                <input type="text" name="username" placeholder="USERNAME" value="%(username)s" />
                                <input type="password" name="password" placeholder="PASSWORD" id="password" />
                                <button class="blue center" type="submit">Submit</button></div>
                            <div class="col_4"></div>
                            </form>
                        </div>
                    </div>""" % locals()
        else:
            html_body += """
            <h1>ACCESSO</h1>
            <form class="vertical" method="post" action="/auth/login">
            <input type="hidden" name="from_page" value="%(from_page)s " />
            <div class="notice error"><i class="icon-remove-sign icon-large"></i>Wrong Username or Password <a href="#close" class="icon-remove"></a></div>
            <input class="error" type="text" name="username" placeholder="USERNAME" value="%(username)s" />
            <input class="error" type="password" name="password" placeholder="PASSWORD" id="password"/><br/><button type="submit">Submit</button></form><br/>""" % locals()
        html = html_header + html_body + footer
        return html

    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):

        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)

        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_loginform(username, error_msg, from_page)
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")