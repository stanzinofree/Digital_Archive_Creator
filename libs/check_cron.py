#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml
import os
import crontab
from local_variables import root_folder

open('etc/cronetab.tab', 'w').close()
system_cron = crontab.CronTab(tabfile='etc/cronetab.tab')
users_cron = crontab.CronTab(user='root')
cron_file=("etc/crontab.yaml")
system_crontab=("etc/system_cron.yaml")

def cron_string(runner,time_cycle,comment):
	job = system_cron.new(command=runner,comment=comment)
	job.setall(time_cycle)
	for elem in system_cron:
		if True == job.is_valid():
			job.enable()

def read_yaml_file(crontab_file):
	conf_open=open(crontab_file,"r")
	yaml_load=yaml.safe_load(conf_open)
	cron_tab=yaml_load["cron"]
	for i in cron_tab:
		runner_tmp=i["command"]
		runner="cd "+ root_folder +";python "+runner_tmp
		time_cycle=i["schedule"]
		comment=i["description"]
		cron_string(runner,time_cycle,comment)


if __name__ == '__main__':
    read_yaml_file(cron_file)
    read_yaml_file(system_crontab)
    system_cron.write('etc/cronetab.tab')