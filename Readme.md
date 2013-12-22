# Digital Archive Creator for OCS Inventory NG #
===========================

This Python software was written to give a better report function to **OCS Inventory NG: http://www.ocsinventory-ng.org/en/** 

It is a web application that read a OCS Database and export data in a fancy and customizable HTML and PDF reports.

## Menu
- [Prerequisites](#prerequisites)
- [Setup](#Setup)
- [Additional Configuration](#additional_configuration)
- [Chngelog](#changelog)
- [TODO](#todo)
- [License](#license)
- [Credits](#credits)
- [Author](#author)



<a name="prerequisites"/>
## Prerequisites

At the actual revision D.A.C. working on a machine with this requisites:
- Centos as OS Distribution (I've tested on 5.X and 6.X)
- Python 2.6
- MySQL DB installed from Centos Repos
- OCS Inventory NG v.2.0

In the next releases I test even Debian and Ubuntu OS

<a name="Setup"/>

## Installation

### Introduction
There are some softwares dependencies that DAC requires to work and you can install with launching setup routines.
Read the above Warning about dependencies that setup try to install and workaround to bypass overwriting of your installed version of these softwares.

:heavy_exclamation_mark: **setup_check.py** TRY TO INSTALL THE FOLLOWING DEPENDECIES:
     -wget
     -python-setuptools
     -make
     -gcc
     -MySQL-python
     -libxslt
     -python-devel
     -pyOpenSSL

If you have special customization of this softwares you can exclude from installation some packages changing following line:

    package = ["wget", "python-setuptools", "make", "gcc", "MySQL-python", "libxslt", "python-devel","pyOpenSSL"]

In the next release I planning to implement launching switch to bypass part of installation routine (redis or wkhtml or some packages too) to save personal configuration of installed software.

The setup_check.py also try to install this python modules trough easy_install software:
    -cherrypy
    -simplejson
    -pyyaml
    -python-crontab
    -redis

After this installation the software prompt you to write the following informations:
    -OCS absolute installation path
    -IP on which application listen to (0.0.0.0  for all ip)
    -Port on which application listen to
    -SSL Cert Path absolute path(blank if you want disable SSL)
    -SSL Cert Key absolute path(blank if you want disable SSL)

### First Step

The first step to create directory in which you want put your installation of DAC.
After you have created the directory, you enter in it and clone the repository:

    git clone https://github.com/stanzinofree/Digital_Archive_Creator

After you have cloned source you can launch the setup with the command:

    python setup_check.py
This launch the setup procedure that check your system for DAC dependencies and if did not found them it provide to install it.

<a name="additional_configuration" />
## Additional Configuration
- [Config](#config)
- [Cronetab](#cronetab)
- [Scheda](#scheda)

<a name="config" />
### Config
In file config.yaml there are some voices to configure, usually if you run setup good you don't have to touch it, if you don't want edit manually you can launch from DAC folder:

    python libs/setup_config.py

If you want edit manually this is the voices in files:
- Path:
 - root_folder : This is the absolute path of DAC folder, root of the software
- Server:
 - server : web address on which ocs respond
 - conf_file : is the absolute path of dbconfig.inc.php file that is the configuration file of ocs 
- Server_Config:
 - ip : ip on which web application listen for connection (ip of server or 0.0.0.0)
 - port : port on which web application listen for connection (if you have iptables turned on you must add an entry for this port)
 - ssl : in this release this field is unused
 - ssl_cert_path : if you want ssl you must insert the absolute path of certification in form of file.crt
 - ssl_key_path : if you want ssl you must insert the absolute path of key file in form of file.key
- Administrators:
 - user : this field contain the username of ocs users that you want promoted administrators of DAC, the form is ["user1", "user2"]
- PID:
 - file : This is the pid file (inside DAC) in which DAC save his state

<a name="cronteab" />
### Cronetab
The cronetab component is divided in two parts, one for system's tasks and the other one for application's tasks.
The System's Tasks are written in system_cron.yaml file and it contains one task to check if website is up and if the site is down it try to start up the site.
I put this task in separate file to put in read only mode because this task is core part of the software and in the next release I want to give the possibility to admin to edit others task in a web way.
The other file cronetab.yaml contains the system routine jobs like search for new computer and you can edit the frequency modifying its value.
The syntax for both files is under the cron leaf.
- description: description of task (it is facultative but I encourage you to write in it to maintain better the tasks).
- command : is the python file that you want launch, now there is only one python check to control, if you write some python plugin to extend check you can call it in this field writing the relative path starting from root dac folder.
- schedule: is the cron syntax schedule, in the next release I want to try to implement English natural language syntax support but for now you have to edit in cron syntax way.

<a name="scheda" />
### Scheda
In scheda.yaml you can find sections defined in OCS report engine and you can decide which of them you want report in your fancy reports.
You can enable the view setting the value to 1 and disabled with 0.
In the next releases I want introduce web editing choise instead of file manually editing and control to normalize file when value differ from 1 or 0.
The voices are:
- Account
 - accountinfo
- Components
 - controllers
 - drives
 - inputs
 - memories
 - monitors
 - networks
 - ports
 - printers
 - slots
 - sounds
 - storages
- Softwares
 - softwares
 - bios
- Hardware
 - hardware

<a name="changelog">
## Changelog

v 1.0
- Release software

<a name="todo" />
## TODO
- English human language in cron system
- Web edit of Cron Task
- Web edit of Scheda section
- Better in code documentation
- Screenshot


<a name="license" />
## License
This software is released under [LGPL](http://www.gnu.org/licenses/lgpl-2.1.txt "LGPL")

<a name="credits" />
## Credits

Thanks to the author of the module I use in my software and the author of templates

- [HTML Kickstart Template](http://www.99lime.com/ "HTML Kickstart")
- [Redis](http://redis.io/ "Redis")
- [Redis-py](https://github.com/andymccurdy/redis-py "Redis-py")
- [PyYAML](http://pyyaml.org/ "PyYAML")
- [Cherrypy](http://www.cherrypy.org/ "CherryPy")
- [Unutbu](http://stackoverflow.com/users/190597/unutbu) from stackoverflow for [this solution](http://stackoverflow.com/questions/3696430/print-colorful-string-out-to-console-with-python) on colored term

<a name="author" />
## Author
**Author**: Middei Alessandro
**Contact**: alessandro.middei@gmail.com
**Website**: www.stanzinofree.net
**Skype**:alessandro.middei
