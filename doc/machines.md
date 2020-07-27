# Overview

Nimbix allows resources to be specified as machine types, using a standardized nomenclature.

# System Architectures

In the Nimbix Cloud the following architectures are supported:

* `n` - x86
* `nx` - Xilinx FPGA (x86)

# Complete Machine Type Examples

Machine Type ID | Platform | XRT | Mark
--------------- | -------- | --- | ----
n2 | N/A | N/A | 8 core, 64GB RAM (CPU only)
n3 | N/A | N/A | 16 core, 128GB RAM (CPU only)
n4 | N/A | N/A | 16 core, 256GB RAM (CPU only)
n5 | N/A | N/A | 16 core, 512GB RAM (CPU only)
n9 | N/A | N/A | 20 core Intel Skylake, 192GB RAM (CPU only)
nx5u_xdma_201830_1 | xilinx_u200_xdma_201830_1 | 2018.3 | 16 core, 128GB RAM, Xilinx Alveo U200 FPGA
nx5u_xdma_201830_2 | xilinx_u200_xdma_201830_2 | 2019.1 | 16 core, 128GB RAM, Xilinx Alveo U200 FPGA
nx5u_xdma_201830_2_2_3 | xilinx_u200_xdma_201830_2 | 2019.2|  16 core, 128GB RAM, Xilinx Alveo U200 FPGA
nx6u_xdma_201830_1 | xilinx_u250_xdma_201830_1 | 2018.3 | 16 core, 128GB RAM, Xilinx Alveo U250 FPGA
nx6u_xdma_201830_2 | xilinx_u250_xdma_201830_2 | 2019.1 | 16 core, 128GB RAM, Xilinx Alveo U250 FPGA
nx6u_xdma_201830_2_2_3 | xilinx_u250_xdma_201830_2 | 2019.2 | 16 core, 128GB RAM, Xilinx Alveo U250 FPGA
nx7u_xdma_201920_1 | xilinx_u280_xdma_201920_1 | 2019.2 | 16 core, 128GB RAM, Xilinx Alveo U280 FPGA
nx_u50_gen3x16_xdma_201920_3 | xilinx_u50_gen3x16_xdma_201920_3 | 2019.2 | 16 core, 128GB RAM, Xilinx Alveo U50 FPGA
nx_u200_202010 | xilinx_u200_xdma_201830_2 | 2020.1 | 16 Core, 128GB RAM, Xilinx U200, xdma-201830.2-2580015 SHELL, 202010.2.6 XRT
nx_u250_202010 | xilinx_u250_xdma_201830_2 | 2020.1 | 16 Core, 128GB RAM, Xilinx U250, xdma-201830.2-2580015 SHELL, 202010.2.6 XRT
nx_u280_202010 | xilinx_u280_xdma_201920_3 | 2020.1 | 16 Core, 128GB RAM, Xilinx U280, xdma-201920.3-2789161 SHELL, 202010.2.6 XRT
nx_u50_202010 | xilinx_u50_gen3x16_xdma_201920_3 | 2020.1 | 16 Core, 128GB, Xilinx U50, xilinx-u50-gen3x16-xdma-201920-3 SHELL, 202010.2.6.665 XRT