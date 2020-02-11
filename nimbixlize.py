#!/usr/bin/env python

import json
import subprocess
import os
import datetime
import shutil 

def list_tags() :
    print ("Available platform and XRT combination:")
    print ("")
    print ("Platform       XRT Version                  OS Version")
    print ("alveo-u200     2018.3 /2019.1 / 2019.2      Ubuntu 16.04 / Ubuntu 18.04 / CentOS")
    print ("alveo-u250     2018.3 /2019.1 / 2019.2      Ubuntu 16.04 / Ubuntu 18.04 / CentOS")
    print ("alveo-u280     2019.2                       Ubuntu 16.04 / Ubuntu 18.04 / CentOS")

with open('config.json') as d:
    repos = json.load(d)

metadata = repos['nimbix_metadata']
provisioners = repos['provisioners']
app_info = repos['app_info']
post_processors = repos['post_processors']

with open('AppDef.json.example') as d:
    appdef = json.load(d)

if not metadata['app_name']:
    print("Application name can NOT be empty!")
    exit(1)

if not app_info['os_version']:
    print("OS version can NOT be empty!")
    exit(1)

if not app_info['xrt_version']:
    print("XRT version can NOT be empty!")
    exit(1)

if not app_info['platform']:
    print("Platform can NOT be empty!")
    exit(1)

if not post_processors['repository']:
    print("Repository can NOT be empty!")
    exit(1)
if not post_processors['tag']:
    print("Tag can NOT be empty!")
    exit(1)

with open('spec.json') as d:
    spec = json.load(d)

# Xilinx Base Runtim Image Url
image_url = "" 
target_platform = ""
if app_info['os_version'] in spec['os_version']:
    if app_info['xrt_version'] in spec['os_version'][app_info['os_version']]['xrt_version']:
        if app_info['platform'] in spec['os_version'][app_info['os_version']]['xrt_version'][app_info['xrt_version']]['platform']:
            image_url = "xilinx/xilinx_runtime_base:" + "alveo" + "-" + app_info['xrt_version'] + "-" + app_info['os_version']
            target_platform = spec['os_version'][app_info['os_version']]['xrt_version'][app_info['xrt_version']]['platform'][app_info['platform']]

if not image_url:
    print("XRT and platform do NOT match! ")
    list_tags()
    exit(1)

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
path = "build_history/" + timestamp

try:
    os.mkdir(path)
    shutil.copy('help.html.example', path + "/help.html")
except OSError:
    print (path)
    exit(1)

commands = []

for pro in provisioners:
    ctype = pro['type']
    if ctype == 'shell':
        commands.append("RUN " + " & ".join(pro['inline']))
    elif ctype == 'file':
        if not os.path.exists(pro['source']):
            print(pro['source'] + "  does NOT exists!")
            exit(1)
        shutil.copy(pro['source'], path + "/")
        filename = os.path.basename(pro['source'])
        commands.append("COPY " + filename + " " + pro['destination'])
    else:
        print("Warning: Unknown type: " + ctype + "! ")

with open("Dockerfile.example", "r") as f:
    s = f.read()
    s = s.replace("__from_image__", image_url)
    with open(path + "/Dockerfile", "w") as d:
        d.write(s)
        for command in commands:
            d.write(command + "\n")

appdef['name'] = metadata['app_name']
appdef['description'] = metadata['app_description']
if not metadata['desktop_mode']:
    del appdef['commands']['server']
if not metadata['batch_mode']:
    del appdef['commands']['batch']
appdef["machines"] = metadata["machines"]
if target_platform not in appdef['machines']:
    appdef['machines'].append(target_platform)


with open(path + '/AppDef.json', "w") as d:
    json.dump(appdef, d, indent=4)

#Build application
subprocess.check_output(
    "docker build -t " + post_processors['repository'] + ":" + post_processors["tag"] + " " + path,
    stderr=subprocess.STDOUT, shell=True)

if post_processors['push_after_build']:
    print("docker push " + post_processors['repository'] + ":" + post_processors["tag"])
    subprocess.check_output("docker push " + post_processors['repository'] + ":" + post_processors["tag"],
    stderr=subprocess.STDOUT, shell=True)

print("Build successfully!")
exit(0)