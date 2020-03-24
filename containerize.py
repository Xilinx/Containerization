#!/usr/bin/env python

import json
import subprocess
import os
import sys
import shutil, errno

def print_help():
    print("usage: ./nimbixlize.py [-h] [-q]")
    print("")
    print("optional arguments:")
    print("  -h, --help            show this help message and exit")
    print("  -q, --quiet           only print error messages on stdout")

support_vendors = ['nimbix']

argvs = sys.argv[1:]
isQuiet = False

for argv in argvs:
    if argv == "-q" or argv == "--quiet":
        isQuiet = True
    elif argv == "-h" or argv == "--help":
        print_help()
        exit(0)

with open('config.json') as d:
    repos = json.load(d)

vendor = repos['vendor']

if vendor not in support_vendors:
    sys.exit("Vendor is NOT supported! ")

if isQuiet: 
    subprocess.check_output("./" + vendor + ".py", stderr=subprocess.STDOUT, shell=True)
else: 
    subprocess.call("./" + vendor + ".py", stderr=subprocess.STDOUT, shell=True)