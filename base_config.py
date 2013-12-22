#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 This file contain all the header (logged and not logged user) and footer for all html files.
If you made a modfiy here you can change header for all html pages.
"""


# ##Import Section
import yaml
import libs.local_variables
"""
 We import the yaml module to read version file
"""

# ##Software and Title variables

vers_file=open(libs.local_variables.version_file)
init_ver=yaml.safe_load(vers_file)
main_ver=init_ver["Version"]
softver = "v. "+main_ver["release"]+"."+main_ver["subversion"]
title = "DAC"
"""
 In this section we valorized the **softver** and **title** variables.
 We open the yaml file that contain version information to compose the softver string

 ### Variable List

 * **vers_file** : this contain yaml file etc/version.yaml
 * **init_ver** : this contain the yaml loading of *version_file* variable
 * **main_ver** : this search in *init_ver* the _Version_ section
 * **softver** : this is the variable we export and it's valorized by _release_ and _subversion_ updated on every release
 * **title** : this is the variable we export and contain the _Title of the software_
"""

# ## Header Base

html_head_base = (
    "<!DOCTYPE html>"
        "<html lang='en'>"
        "<head>"
            "<meta charset='utf-8' />"
            "<title>" + title + " " + softver + "</title>"
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'/>"
            "<meta name='description' content='OCS_DAC di Middei Alessandro' />"
            "<meta name='copyright' content='Middei Alessandro' />"
            "<link rel='stylesheet' href='/css/jquery.fancybox-1.3.4.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/jquery.terminal.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/jquery-ui-1.10.3.custom.min.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/style.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/kickstart.css' type='text/css' media='all'/>"
            "<link rel='stylesheet' href='/css/kickstart-grid.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/prettify.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/kickstart-forms.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/tiptip.css' type='text/css' />"
            "<link rel='stylesheet' href='/css/kickstart-buttons.css' type='text/css' />"
            "<script src='/js/jquery-1.9.1.min.js' type='text/javascript' charset='utf-8'></script>"
            "<script src='/js/kickstart.js' type='text/javascript' ></script>"
            #"<script src='/js/pyterm2.js' type='text/javascript' ></script>"
            "<script src='/js/jquery.terminal-0.7.8.js' type='text/javascript' ></script>"
            "<script src='/js/jquery-ui-1.10.3.custom.min.js' type='text/javascript' charset='utf-8'></script>"
            "<script src='/js/live_search.js' type='text/javascript' charset='utf-8'></script>"
            "</head>"
            "<body class='elements'>")
"""
 Whit this variable **html_head_base** we define a skeleton to use for all html pages, we call all css and javascript and we recall
 **softver** and **title** variables
"""


#IStart to coding the skel of every page
html_header = html_head_base + (
                "<!-- HR.alt1 -->"
                "<!-- Menu Horizontal -->"
                "<nav class='navbar'>"
                    "<a id='logo' href='/auth/login'><i class='icon-angle-right'></i> L<span>ogin</span></a>"
                    "<ul>"
                	    "<li class='current'><a href=''><span>H</span>ome</a></li>"
                    "</ul>"
                "</nav>"
                "<div class='callout callout-top clearfix  hide-phone'>"
                "<div class='grid  hide-phone'>"
                        "<h1>" + title + " " + softver + "</h1>"
                    "</div>"
                    "<div class='clear'> </div>"
                "</div>"
                "</div>"
                "<div class='grid'>")

html_logged_header = html_head_base + (
                "<!-- HR.alt1 -->"
                "<!-- Menu Horizontal -->"
                "<nav class='navbar'>"
                    "<a id='logo' href='/auth/logout'><i class='icon-angle-right'></i> L<span>ogout</span></a>"
                    "<ul>"
                        "<li><a href='/search_schede'><span>D</span>ownload Scheda</a></li>"
                        "<li><a href='/test'><span>L</span>og</a>"
                        "<li><a href='/admin/admin'><span>A</span>dministrator</a>"
                    "</ul>"
                "</ul>"
                "</nav>"
                "<div class='callout callout-top clearfix  hide-phone'>"
                "<div class='grid  hide-phone'>"
                        "<h1>" + title + " " + softver + "</h1>"
                    "</div>"
                    "<div class='clear'> </div>"
                "</div>"
                "</div>"
                "<div class='grid'>")

#And now coding our Footer
def html_footer(nome):
    if nome == None:
        footer = (
                "</div><div class='clear'></div>"
              "<div id='footer'>"
              "<div class='grid flex'>"
              "<div class='col_10'>&copy; Copyright 2012–2013 All Rights Reserved.</div>"
              "<div class='col_2'>Utente: Anonimo</div>"
              "</div></div></body></html>")
    else:
        footer = (
                "</div><div class='clear'></div>"
                "<div id='footer'>"
                "<div class='grid flex'>"
                "<div class='col_10'>&copy; Copyright 2012–2013 All Rights Reserved.</div>"
                "<div class='col_2'>Utente: " + nome + "</div>"
                "</div></div></body></html>")
    return footer