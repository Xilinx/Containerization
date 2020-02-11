#!/usr/bin/env python

import json
import subprocess
import os
import datetime
import shutil 

def list_machines() :
    print "Available Machines Types on Nimbix:"
    print ("")
    print ("Machine Type ID         Platform                      Mark")
    print ("n2                      N/A                           8 core, 64GB RAM (CPU only)")
    print ("n3                      N/A                           16 core, 128GB RAM (CPU only)")
    print ("n4                      N/A                           16 core, 256GB RAM (CPU only)")
    print ("n5                      N/A                           16 core, 512GB RAM (CPU only)")
    print ("n9                      N/A                           20 core Intel Skylake, 192GB RAM (CPU only)")
    print ("nx5u                    xilinx_u200_xdma_201820_1     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2018.2 XDF")
    print ("nx5u_xdma_201830_1      xilinx_u200_xdma_201830_1     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2018.3")
    print ("nx5u_xdma_201830_2      xilinx_u200_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2019.1")
    print ("nx5u_xdma_201830_2_2_3  xilinx_u200_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2019.2")
    print ("nx6u                    xilinx_u250_xdma_201820_1     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2018.2 XDF")
    print ("nx6u_xdma_201830_1      xilinx_u250_xdma_201830_1     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2018.3")
    print ("nx6u_xdma_201830_2      xilinx_u250_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2019.1")
    print ("nx6u_xdma_201830_2_2_3  xilinx_u250_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2019.2")
    print ("nx7u_xdma_201920_1      xilinx_u280_xdma_201920_1     16 core, 128GB RAM, Xilinx Alveo U280 FPGA 2019.2")

def list_tags() :
    print ("Available platform and XRT combination:")
    print ("")
    print ("Platform                                  XRT Version    OS Version")
    print ("alveo-u200 / alveo-u250                   2018.3         CentOS")
    print ("alveo-u200 / alveo-u250                   2018.3         Ubuntu 16.04")
    print ("alveo-u200 / alveo-u250                   2018.3         Ubuntu 18.04")
    print ("alveo-u200 / alveo-u250 / alveo-u280      2019.1         CentOS")
    print ("alveo-u200 / alveo-u250 / alveo-u280      2019.1         Ubuntu 16.04")
    print ("alveo-u200 / alveo-u250 / alveo-u280      2019.1         Ubuntu 18.04")
    print ("alveo-u200 / alveo-u250 / alveo-u280      2019.2         CentOS")
    print ("alveo-u200 / alveo-u250 / alveo-u280      2019.2         Ubuntu 16.04")
    print ("alveo-u200 / alveo-u250 / alveo-u280      2019.2         Ubuntu 18.04")

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

if post_processors['push_after_build']:
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
copies = []
for pro in provisioners:
    ctype = pro['type']
    if ctype == 'cmd':
        commands.append("RUN " + " & ".join(pro['inline']))
    elif ctype == 'file':
        if not os.path.exists(pro['source']):
            print(pro['source'] + "  does NOT exists!")
            exit(1)
        shutil.copy(pro['source'], path + "/")
        filename = os.path.basename(pro['source'])
        copies.append("COPY " + filename + " " + pro['destination'])

with open("Dockerfile.example", "r") as f:
    s = f.read()
    s = s.replace("__from_image__", image_url)
    with open(path + "/Dockerfile", "w") as d:
        d.write(s)
        for copy in copies:
            d.write(copy+"\n")
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
    json.dump(appdef, d)

#Build application
subprocess.check_output(
    "docker build -t " + post_processors['repository'] + ":" + post_processors["tag"] + " -f " + path + "/Dockerfile",
    stderr=subprocess.STDOUT)

if post_processors['push_after_build']:
    subprocess.check_output("docekr push " + post_processors['repository'] + ":" + post_processors["tag"],
    stderr=subprocess.STDOUT)