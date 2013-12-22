#!/bin/python
# -*- coding: utf-8 -*-
"""
library to search through a ocs configuration file to extract credentials and translate in a Yaml compatible format

v. 0.1
"""
#expression='("(\w *)"),\s.'

import re


class parse():
    def extract_it(self, f_toparse):
        fop = open(f_toparse, "r")
        parsed_results = []
        for line in fop:
            match = re.search(r'"(\w*)".\s+"(\w*)"', line)
            if match:
                subs = re.sub(r',', r':', str(match.group()))
                parsed_results.append(subs)
            else:
                pass
        return parsed_results


if __name__ == "__main__":
    find = parse()
    parsed = find.extract_it("/usr/share/ocsinventory-reports/ocsreports/dbconfig.inc.php")
    for i in parsed:
        print i