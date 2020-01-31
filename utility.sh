#!/usr/bin/env bash
#
# (C) Copyright 2020, Xilinx, Inc.
#
#!/usr/bin/env bash

usage() {
    echo "Run utility.sh for building docker application for Nimbix. "
    echo ""
    echo "./utility.sh "
    echo "   -i --image        [Image ID] (required)"
    echo "   -t --tag          [New Image ID] (required)"
    echo "   -n --name         [App name] (required)"
    echo "   -d --description  [App Description] (not required)"
    echo "   -p --push         [push after build] (not required)"

}


list() {
    echo "Available Machines Types on Nimbix:"
    echo ""
    echo "Machine Type ID         Platform                      Mark"
    echo "n2                      N/A                           8 core, 64GB RAM (CPU only)"
    echo "n3                      N/A                           16 core, 128GB RAM (CPU only)"
    echo "n4                      N/A                           16 core, 256GB RAM (CPU only)"
    echo "n5                      N/A                           16 core, 512GB RAM (CPU only)"
    echo "n9                      N/A                           20 core Intel Skylake, 192GB RAM (CPU only)"
    echo "nx5u                    xilinx_u200_xdma_201820_1     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2018.2 XDF"
    echo "nx5u_xdma_201830_1      xilinx_u200_xdma_201830_1     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2018.3"
    echo "nx5u_xdma_201830_2      xilinx_u200_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2019.1"
    echo "nx5u_xdma_201830_2_2_3  xilinx_u200_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U200 FPGA 2019.2"
    echo "nx6u                    xilinx_u250_xdma_201820_1     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2018.2 XDF"
    echo "nx6u_xdma_201830_1      xilinx_u250_xdma_201830_1     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2018.3"
    echo "nx6u_xdma_201830_2      xilinx_u250_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2019.1"
    echo "nx6u_xdma_201830_2_2_3  xilinx_u250_xdma_201830_2     16 core, 128GB RAM, Xilinx Alveo U250 FPGA 2019.2"
    echo "nx7u_xdma_201920_1      xilinx_u280_xdma_201920_1     16 core, 128GB RAM, Xilinx Alveo U280 FPGA 2019.2"
}

notice_disclaimer() {
    cat doc/notice_disclaimer.txt
}

confirm() {
    # call with a prompt string or use a default
    read -r -p "${1:-Are you sure you wish to proceed? [y/n]:} " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            true
            ;;
        *)
            exit 1
            ;;
    esac
}


docker info > /dev/null
if [ $? != 0 ] ; then
    docker info
    exit 1
fi


while true
do
case "$1" in
    -i | --image           ) IMAGE="$2"    ; shift 2 ;;
    -t | --tag             ) TAG="$2"      ; shift 2 ;;
    -n | --name            ) NAME="$2"     ; shift 2 ;;
    -d | --description     ) DESC="$2"     ; shift 2 ;;
    -p | --push            ) PUSH="1"      ; shift 1 ;;
    -h | --help            ) usage         ; exit  1 ;;
*) break ;;
esac
done

if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; usage; exit 1 ; fi

while [[ -z "$IMAGE" ]]; do
    read -r -p "${1:-Please enter your origin docker image id :} " IMAGE
    if [[ -z "$IMAGE" ]]; then
        echo "Image ID can NOT be empty! "
    fi
done

while [[ -z "$TAG" ]]; do
    read -r -p "${1:-Please enter your building Nimbix docker image id (ie. $IMAGE-nimbix) :} " TAG
    if [[ -z "$TAG" ]]; then
        echo "New Image ID can NOT be empty! "
    fi
done

while [[ -z "$NAME" ]]; do
    read -r -p "${1:-Please enter your building Nimbix application name :} " NAME
    if [[ -z "$NAME" ]]; then
        echo "App name can NOT be empty! "
    fi
done

if [[ -z "$DESC" ]]; then
    read -r -p "${1:-Please enter your building Nimbix application description (optional) :} " NAME
fi


TIMESTAMP=$(date +"%Y%m%d%H%M%S")
mkdir -p build_history/$TIMESTAMP
if [ $? != 0 ] ; then echo "Failed make directory." >&2 ; exit 1 ; fi

cp Dockerfile.example           build_history/$TIMESTAMP/Dockerfile
cp AppDef.json.example          build_history/$TIMESTAMP/AppDef.json
cp help.html.example            build_history/$TIMESTAMP/help.html
cd build_history/$TIMESTAMP

sed -i "s/__from_image__/${IMAGE}/g" Dockerfile
sed -i "s/__dockerfile_name__/${NAME}/g" AppDef.json
sed -i "s/__dockerfile_description__/${DESC}/g" AppDef.json

if grep -q "__update machine types here__" AppDef.json; then
  echo "Please update machine types in AppDef.json.example before building application. "
  echo ""
  list
  exit 1
fi

echo "docker build -t $TAG ."

if [[ "$PUSH" == "1" ]]; then
    echo "docker push $TAG"
else
    echo "Push docker image $TAG by: docker push $TAG"
fi