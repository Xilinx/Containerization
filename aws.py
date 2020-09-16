#!/usr/bin/env python

import json
import subprocess
import os
import sys
import datetime
import shutil, errnoimport argparse

parser = argparse.ArgumentParser()
parser.add_argument('-path', help = 'the config file path, default as config.json')
args = parser.parse_args()

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise


if args.path:
    with open(args.path) as d:
        repos = json.load(d)
else:
    with open('config.json') as d:
        repos = json.load(d)

vendor = repos['vendor']
metadata = repos['metadata']
provisioners = repos['provisioners']
post_processors = repos['post_processors']

if vendor != "aws":
    sys.exit("Vendor is NOT supported! ")

if not metadata['os_version']:
    sys.exit("OS version can NOT be empty!")
elif metadata['os_version'] != "centos":
    sys.exit("AWS only supports CentOS! ")

if not metadata['xrt_version']:
    sys.exit("XRT version can NOT be empty!")

if not post_processors['repository']:
    sys.exit("Repository can NOT be empty!")
if not post_processors['tag']:
    sys.exit("Tag can NOT be empty!")

with open('spec.json') as d:
    spec = json.load(d)
    spec = spec["aws"]

# XRT Packages
if metadata['xrt_version'] in spec:
    xrt_package = spec[metadata['xrt_version']]['xrt']
    aws_package = spec[metadata['xrt_version']]['xrt-aws']
else:
    sys.exit("AWS supports XRT version: " + ", ".join(spec.keys()))

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
path = "build_history/" + timestamp

try:
    os.mkdir(path)
except OSError:
    sys.exit("[Error]: Can NOT create folder " + path)

commands = ["RUN curl -s "+xrt_package+" -o xrt.rpm; curl -s "+aws_package+" -o xrt_aws.rpm; yum install -y epel-release; yum install -y xrt*.rpm"]
labels = {}

for pro in provisioners:
    ctype = pro['type']
    if ctype == 'shell':
        commands.append("RUN " + " && ".join(pro['inline']))
    elif ctype == 'file':
        if not os.path.exists(pro['source']):
            sys.exit(pro['source'] + "  does NOT exists!")
        filename = os.path.basename(os.path.normpath(pro['destination']))
        copyanything(pro['source'], path + "/" + filename)
        commands.append("COPY " + filename + " " + pro['destination'])
    elif ctype == 'label':
        labels[pro['key']] = pro['value']
    else:
        print("Warning: Unknown type: " + ctype + "! ")

with open(path + "/Dockerfile", "w") as d:
    d.write("From centos:7 \n")
    for command in commands:
        d.write(command + "\n")
    if labels:
        label_str = 'LABEL '
        for key in labels:
            label_str += key + '="' + labels[key] + '" '
        d.write(label_str + "\n")
    if metadata and "entrypoint" in metadata:
        d.write("ENTRYPOINT " + metadata['entrypoint'])

#Build application

print("Build docker image: " + post_processors['repository'] + ":" + post_processors["tag"])
subprocess.check_call(
    "docker build -t " + post_processors['repository'] + ":" + post_processors["tag"] + " " + path,
    stderr=subprocess.STDOUT, shell=True)

if post_processors['push_after_build']:
    print("docker push " + post_processors['repository'] + ":" + post_processors["tag"])
    subprocess.check_call("docker push " + post_processors['repository'] + ":" + post_processors["tag"],
    stderr=subprocess.STDOUT, shell=True)

print("Build history: " + path)
print("Build successfully!")
exit(0)