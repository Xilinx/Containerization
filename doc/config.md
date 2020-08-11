# Introducing the config file

The config file describes the application interface for Xilinx FPGA applications that are deployed on multiple cloud vendors.

The config file is a simple JSON object which is used to define:

* Vendor
* Metadata (metadata required by cloud vendors)
* Application information (XRT version, OS version and target platform. Except for AWS. )
* Provisioners (support two functions: inline command and copy files)
* Post processor (build repository and tag)

# Reference

## Vendor
Key | Type | Required/Optional | Description | Example
----| ---- | ----------------- | ----------- | -------
vendor | string | required | Application target cloud vendor. | "nimbix" / "on_premise" / "aws"


## Metadata

### On Premise
Key | Type | Required/Optional | Description | Example
----| ---- | ----------------- | ----------- | -------
entrypoint | string | optional | An ENTRYPOINT allows you to configure a container that will run as an executable. | '["executable", "param1", "param2"]'

### Nimbix metadata

Key | Type | Required/Optional | Description | Example
----| ---- | ----------------- | ----------- | -------
app_name | string | required | Defines the human-readable name of the application. | "Xilinx Vitis Application 2019.2"
app_description | string | optional | Description of the application used in the application market place icon. | "The Vitis unified software platform enables..."
app_cover_image | string | optional | The path of cover image of the application. The image must be PNG image. | "/home/user/cover_image.png"
app_license | string | optional | The path of license of the application. The image must be txt file. | "/home/user/license.txt"
machines | list of strings | required | Target platforms of application on Nimbix. See [Machines](machines.md) for more information. | ["n2", "n3", "nx7u_xdma_201920_1"]
desktop_mode | boolean | required | Enable desktop mode. Default `true` | true
batch_mode | boolean | required | Enable batch mode. Default `true` | true 

### AWS

Key | Type | Required/Optional | Description | Example
----| ---- | ----------------- | ----------- | -------
xrt_version | string | required | Xilinx Runtime versions match with the tool that you created your AFI with. | "2019.2"
os_version | string | required | AWS only supports CentOS for now | "centos"

## Application information

Only for Nimbix and on premise. AWS supports its own version and platform. Configure in section Metadata. 

Key | Type | Required/Optional | Description | Available values
----| ---- | ----------------- | ----------- | -------
xrt_version | string | required | XRT version of application | 2018.3 / 2019.1 / 2019.2
os_version | string | required | OS version application running on | ubuntu-16.04 / ubuntu-18.04 / centos
platform | list of strings | required | Target platforms of application | alveo-u200 / alveo-u250 / alveo-u280

## Provisioners

### Inline command

Inline command provides any commands you want to run when building your applications.

Key | Type | Required/Optional | Description | Example
----| ---- | ----------------- | ----------- | -------
type | string | required | Type of provisioner. Must be `shell` | "shell"
inline | list of strings (commands) | required | List of commands | `[ "mkdir -p /tmp/deploy" , "apt-get update"]`

### Copy files

Copy local files to your Nimbix applications. 

Key | Type | Required/Optional | Description | Example
----| ---- | ----------------- | ----------- | -------
type | string | required | Type of provisioner. Must be `file` | "file"
source | path | required | Source path of your local file or directory | `/opt/xilinx/xsa/xilinx_u280_xdma_201920_1/test/validate.exe`
destination | path | required | Destination path of file or directory located in application | `/opt/xilinx/test/validate.exe`

## Post processor

Key | Type | Required/Optional | Description | Example
----| ---- | ----------------- | ----------- | -------
repository | string | required | Repository of application (docker image) | xilinx/xilinx_nimbix_application*
tag | string | required | Tag of application (docker image) | vitis-2019.2
push_after_build | boolean | required | Determine application (docker image) push after build or not. Default `true` | true

>The `repository` can be a DockerHub repository or a private repository. Learn more on [docker tag](https://docs.docker.com/engine/reference/commandline/tag/). 

# Config file example

## Nimbix

```
{
    "vendor": "nimbix",
    "metadata":{
        "app_name": "nx7u test",
        "app_description": "nx7u test",
        "app_cover_image": "/home/user/cover_image.png",
        "app_license": "/home/user/license.txt",
        "machines":["n2", "n3", "nx7u_xdma_201920_1"],
        "desktop_mode": true,
        "batch_mode": true
    },
    "provisioners":[
        {
            "type": "shell",
            "inline": ["mkdir -p /opt/xilinx/test", "apt-get update"]
        },
        {
            "type": "file",
            "source": "/opt/xilinx/xsa/xilinx_u280_xdma_201920_1/test/validate.exe",
            "destination": "/opt/xilinx/test/validate.exe"
        },
        {
            "type": "file",
            "source": "/opt/xilinx/xsa/xilinx_u280_xdma_201920_1/test/verify.xclbin",
            "destination": "/opt/xilinx/test/verify.xclbin"
        }
    ],
    "post_processors": {
        "repository": "xilinx/test",
        "tag": "nimbix-test",
        "push_after_build": true
    },
    "app_info":{
        "xrt_version": "2019.2",
        "os_version": "ubuntu-16.04",
        "platform": ["alveo-u280"]
    }
}
```

## On Premise

```
{
    "vendor": "on_premise",
    "metadata": {
        "entrypoint": '["executable", "param1", "param2"]'
    },
    "provisioners":[
        {
            "type": "shell",
            "inline": ["mkdir -p /opt/xilinx/test", "apt-get update"]
        },
        {
            "type": "file",
            "source": "/opt/xilinx/xsa/xilinx_u280_xdma_201920_1/test/validate.exe",
            "destination": "/opt/xilinx/test/validate.exe"
        },
        {
            "type": "file",
            "source": "/opt/xilinx/xsa/xilinx_u280_xdma_201920_1/test/verify.xclbin",
            "destination": "/opt/xilinx/test/verify.xclbin"
        }
    ],
    "post_processors": {
        "repository": "xilinx/test",
        "tag": "on-premise-test",
        "push_after_build": true
    },
    "app_info":{
        "xrt_version": "2019.2",
        "os_version": "ubuntu-16.04",
        "platform": ["alveo-u280"]
    }
}
```

## AWS

```
{
    "vendor": "on_premise",
    "metadata": {
        "xrt_version": "2019.2",
        "os_version": "centos"
    },
    "provisioners":[
        {
            "type": "shell",
            "inline": ["mkdir -p /opt/xilinx/test", "yum update"]
        },
        {
            "type": "file",
            "source": "/opt/xilinx/xsa/xilinx_u280_xdma_201920_1/test/validate.exe",
            "destination": "/opt/xilinx/test/validate.exe"
        },
        {
            "type": "file",
            "source": "/opt/xilinx/xsa/xilinx_u280_xdma_201920_1/test/verify.awsxclbin",
            "destination": "/opt/xilinx/test/verify.aws`xclbin"
        }
    ],
    "post_processors": {
        "repository": "xilinx/test",
        "tag": "aws-test",
        "push_after_build": true
    }
}
```