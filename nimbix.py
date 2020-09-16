#!/usr/bin/env python

import json
import subprocess
import os
import sys
import datetime
import shutil, errno
import argparse

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

def list_tags() :
    sys.exit("XRT and platform do NOT match! \
    Available platform and XRT combination:\
    \
    Platform       XRT Version                          OS Version\
    alveo-u200     2018.3 /2019.1 / 2019.2 / 2020.1     Ubuntu 16.04 / Ubuntu 18.04 / CentOS\
    alveo-u250     2018.3 /2019.1 / 2019.2 / 2020.1     Ubuntu 16.04 / Ubuntu 18.04 / CentOS\
    alveo-u280     2019.2 / 2020.1                      Ubuntu 16.04 / Ubuntu 18.04 / CentOS\
    alveo-u50      2019.2 / 2020.1                      Ubuntu 16.04 / Ubuntu 18.04 / CentOS")

if args.path:
    with open(args.path) as d:
        repos = json.load(d)
else:
    with open('config.json') as d:
        repos = json.load(d)

vendor = repos['vendor']
metadata = repos['metadata']
provisioners = repos['provisioners']
app_info = repos['app_info']
post_processors = repos['post_processors']
example_path = "examples/nimbix/"

if vendor != "nimbix":
    sys.exit("Vendor is NOT supported! ")

with open(example_path+'AppDef.json.example') as d:
    appdef = json.load(d)

if not metadata['app_name']:
    sys.exit("Application name can NOT be empty!")

if not app_info['os_version']:
    sys.exit("OS version can NOT be empty!")

if not app_info['xrt_version']:
    sys.exit("XRT version can NOT be empty!")

if not app_info['platform']:
    sys.exit("Platform can NOT be empty!")

if not post_processors['repository']:
    sys.exit("Repository can NOT be empty!")
if not post_processors['tag']:
    sys.exit("Tag can NOT be empty!")

internal = False
if "internal" in metadata and metadata['internal']:
    internal = True


with open('spec.json') as d:
    spec = json.load(d)

commands = []
labels = {}

# Xilinx Base Runtim Image Url

image_url = "" 
target_platforms = []

if internal:
    image_url = "xdock.xilinx.com/base_runtime:" + post_processors['tag'] + "-" + app_info['os_version']
else:
    if app_info['os_version'] in spec['os_version']:
        if app_info['xrt_version'] in spec['os_version'][app_info['os_version']]['xrt_version']:
            image_url = "xilinx/xilinx_runtime_base:" + "alveo" + "-" + app_info['xrt_version'] + "-" + app_info['os_version']
            for platform in app_info['platform']:
                if platform in spec['os_version'][app_info['os_version']]['xrt_version'][app_info['xrt_version']]['platform']:
                    target_platforms.append(spec['os_version'][app_info['os_version']]['xrt_version'][app_info['xrt_version']]['platform'][platform])
                    if platform == "alveo-u50" and app_info['xrt_version'] == "2019.2":
                        image_url += "-u50"
                        commands.append("ENV INTERNAL_BUILD=1")
                else:
                    print(" [Warning] Invalide platform: " + platform)

    if not image_url:
        list_tags()

dockerfile_example = example_path + ("Dockerfile_Centos.example" if app_info['os_version'] == "centos" else "Dockerfile_Ubuntu.example")
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
path = "build_history/" + timestamp

try:
    os.mkdir(path)
    shutil.copy(example_path+'help.html.example', path + "/help.html")
    shutil.copy(example_path+'xilinx_runtime.sh.example', path + "/xilinx_runtime.sh")
except OSError:
    sys.exit("[Error]: Can NOT create folder " + path)

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

if "app_cover_image" in metadata:
    app_cover_image = metadata["app_cover_image"]
    if not os.path.exists(app_cover_image):
        print("[Warning]: " + app_cover_image + " is not exists! ")
    elif not app_cover_image.lower().endswith('.png'):
        print("[Warning]: Cover image must be PNG image! Skip adding cover image! ")
    else:
        copyanything(app_cover_image, path + "/" + "screenshot.png")
        commands.append("COPY screenshot.png /etc/NAE/screenshot.png")
        commands.append("RUN chmod 644 /etc/NAE/screenshot.png")

if "app_license" in metadata:
    app_license = metadata["app_license"]
    if not os.path.exists(app_license):
        print("[Warning]: " + app_license + " is not exists! ")
    elif not app_license.lower().endswith('.txt'):
        print("[Warning]: License file must be txt file! Skip adding license file! ")
    else:
        copyanything(app_license, path + "/" + "license.txt")
        commands.append("COPY license.txt /etc/NAE/license.txt")

with open(dockerfile_example, "r") as f:
    s = f.read()
    s = s.replace("__from_image__", image_url)
    with open(path + "/Dockerfile", "w") as d:
        d.write(s)
        for command in commands:
            d.write(command + "\n")
        if labels:
            label_str = 'LABEL '
            for key in labels:
                label_str += key + '="' + labels[key] + '" '
            d.write(label_str + "\n")

appdef['name'] = metadata['app_name']
appdef['description'] = metadata['app_description']
if not metadata['desktop_mode']:
    del appdef['commands']['server']
if not metadata['batch_mode']:
    del appdef['commands']['batch']
appdef["machines"] = metadata["machines"]
for target_platform in target_platforms:
    if target_platform not in appdef['machines']:
        appdef['machines'].append(target_platform)


with open(path + '/AppDef.json', "w") as d:
    json.dump(appdef, d, indent=4)

#Build application

print("Build docker image: " + post_processors['repository'] + ":" + post_processors["tag"])
subprocess.check_call(
    "docker build -t " + post_processors['repository'] + ":" + post_processors["tag"] + " " + path,
    stderr=subprocess.STDOUT, shell=True)

if post_processors['push_after_build']:
    print("docker push " + post_processors['repository'] + ":" + post_processors["tag"])
    subprocess.check_call("docker push " + post_processors['repository'] + ":" + post_processors["tag"],
    stderr=subprocess.STDOUT, shell=True)
else:
    print("Push docker image by running:")
    print("    docker push " + post_processors['repository'] + ":" + post_processors["tag"])

print("Build history: " + path)
print("Build successfully!")
exit(0)
