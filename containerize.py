#!/usr/bin/env python

import json
import subprocess
import os
import sys
import shutil, errno
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-path', help = 'the config file path, default as config.json')
args = parser.parse_args()

def print_help():
    print("usage: ./containerize.py [-path] [-h] [-q]")
    print("")
    print("optional arguments:")
    print("  -path,                the config file path, default as config.json")
    print("  -h, --help            show this help message and exit")
    print("  -q, --quiet           only print error messages on stdout")

support_vendors = ['nimbix', 'on_premise', 'aws']

argvs = sys.argv[1:]
isQuiet = False

for argv in argvs:
    if argv == "-q" or argv == "--quiet":
        isQuiet = True
    elif argv == "-h" or argv == "--help":
        print_help()
        exit(0)

if args.path:
    with open(args.path) as d:
        repos = json.load(d)
else:
    with open('config.json') as d:
        repos = json.load(d)

vendor = repos['vendor']

if vendor not in support_vendors:
    sys.exit("Vendor is NOT supported! Support Vendors: " + ", ".join(support_vendors))

if args.path:
    if isQuiet: 
        subprocess.check_output("./" + vendor + ".py " + "-path " + args.path , stderr=subprocess.STDOUT, shell=True)
    else: 
        subprocess.call("./" + vendor + ".py " + "-path " + args.path , stderr=subprocess.STDOUT, shell=True)
else:
    if isQuiet:
        subprocess.check_output("./" + vendor + ".py ", stderr=subprocess.STDOUT, shell=True)
    else:
        subprocess.call("./" + vendor + ".py " , stderr=subprocess.STDOUT, shell=True)
