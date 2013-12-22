#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml
import os
import crontab

cron_file="/var/spool/cron/root"
crontab_file="etc/cronetab.tab"

def analyze_crontab_file():
	temp_open=open(crontab_file,'r')
	rows=[]
	for lines in temp_open:
		lines = lines.rstrip()
		rows.append(lines)
	return rows

def analyze_cron():
	temp_open=open(cron_file,'r')
	rows=[]
	for i in temp_open:
		i = i.rstrip()
		rows.append(i)
	return rows

def compare(crontab_rows=analyze_crontab_file(),cron_rows=analyze_cron()):
	full_row=[]
	print len(cron_rows)
	if len(cron_rows) == 0:
		for i in crontab_rows:
			full_row.append(i)
	else:
		list1=set(cron_rows)
		list2=set(crontab_rows)
		list_diff=list2-list1
		list_tot=cron_rows+list(list_diff)
		for element in list_tot:
			full_row.append(element)
	return full_row

def compose(flux=compare()):
	open(cron_file, 'w').close()
	cron_write=open(cron_file,"w")
	for i in flux:
		print i
		cron_write.write("%s\n" % i)
	cron_write.close()
	print "OK"

if __name__ == '__main__':
    compose()