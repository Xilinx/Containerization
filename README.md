# Nimbix Container Flow for Library and Application

This project provides script to build Docker Application for Nimbix Jarvice platform based on docker image. 

## Usage

1. Clone nimbixlize repository

`git clone https://gitenterprise.xilinx.com/FaaSApps/nimbixlize.git`

2. Go to nimbixlize repository

`cd nimbixlize`

3. Modify file `AppDef.json.example`. Update attribute `machines` on line 10. Replace `__update machine types here__` with machine type id list below. 

Machine Type ID | Platform | Mark
------------- | -------- | -------
n2 | N/A | 8 core, 64GB RAM (CPU only)
n3 | N/A | 16 core, 128GB RAM (CPU only)
n4 | N/A | 16 core, 256GB RAM (CPU only)
n5 | N/A | 16 core, 512GB RAM (CPU only)
n9 | N/A | 20 core Intel Skylake, 192GB RAM (CPU only)
nx5u | xilinx_u200_xdma_201820_1 | 16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2018.2 XDF 
nx5u_xdma_201830_1 | xilinx_u200_xdma_201830_1 | 16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2018.3
nx5u_xdma_201830_2 | xilinx_u200_xdma_201830_2 | 16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2019.1
nx5u_xdma_201830_2_2_3 | xilinx_u200_xdma_201830_2 | 16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2019.2
nx6u | xilinx_u250_xdma_201820_1 | 16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2018.2 XDF 
nx6u_xdma_201830_1 | xilinx_u250_xdma_201830_1 | 16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2018.3
nx6u_xdma_201830_2 | xilinx_u250_xdma_201830_2 | 16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2019.1
nx6u_xdma_201830_2_2_3 | xilinx_u250_xdma_201830_2 | 16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2019.2
nx7u_xdma_201920_1 | xilinx_u280_xdma_201920_1 | 16 core, 128GB RAM, Xilinx Alveo U280 FPGA 2019.2

For example:
```
	"machines": [
        "n2",
        "n3",
        "nx7u_xdma_201920_1"
    ],
```

4. Build Nimbix image

	4.1 `./utility.sh`

	4.2 Enter your origin docker image id: 

	4.3 Enter your building Nimbix docker image id : 

	4.4 Enter your building Nimbix application name: 

	4.5 Enter your buiilding Nimbix application description (optional):

5. Push built docker image

`docker push $(IMAGE ID)`