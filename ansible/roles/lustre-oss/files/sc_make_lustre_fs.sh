#!/bin/bash

cluster_name=$1
mgs_ip=$2
is_mounted=$(mount -t lustre)

if [[ $is_mounted == *"mnt"* ]]
then
    echo "Already mounted"
else
    mkfs.lustre --reformat --mgsnode=$mgs_ip@tcp --fsname=$cluster_name --ost --index=0 /dev/vda4 > log.log
fi
