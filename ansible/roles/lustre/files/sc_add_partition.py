#! /usr/bin/python

# This scrips creates an unformatted partition using the rest of the unallocated disk space

import os, sys, re, subprocess


free_space_cmd = 'parted /dev/vda unit s print free | grep "Free Space" | tail -1 | grep -E "[0-9]"'
free_space_res = subprocess.Popen([free_space_cmd], stdout=subprocess.PIPE, shell=True)
free_space_res = free_space_res.communicate()[0]
print(free_space_res)
free_block = re.findall('[0-9]+', free_space_res)[0]
print(free_block)
os.system('parted /dev/vda mkpart primary ext4 {}s -- -1s'.format(free_block))
