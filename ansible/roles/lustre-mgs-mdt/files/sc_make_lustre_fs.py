#! /usr/bin/python

# Create lustre fs
import os, subprocess

p = subprocess.Popen('fdisk -lu | grep "vda4"', shell=True, stdout=subprocess.PIPE)
output, _ = p.communicate()
is_mounted = subprocess.Popen('mount -t lustre | grep "lustre"', shell=True, stdout=subprocess.PIPE)
output2, _ = is_mounted.communicate()
if p.returncode == 1: # no matches found
    print ('ERROR: Creating lustre partition')
elif is_mounted.returncode == 1: #no lustre partition mounted
    print('mounting...')
    os.system('mkfs.lustre --reformat --fsname=DATA --mgs --mdt /dev/vda4')
