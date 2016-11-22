#!/usr/bin/python

import os, sys

if len(sys.argv) < 3:
    print("ERROR: Missing vm name and/or ip number")
    quit()

name = sys.argv[1]
ip_number = sys.argv[2]
vm_name = '{}_{}'.format(name, ip_number)
ks_file = open("/home/mecavity/.kickstart/{}.ks".format(vm_name), 'w')

ks_str = "\
#version=DEVEL\n\
# System authorization information\n\
auth --enableshadow --passalgo=sha512\n\
# Use network installation\n\
url --url=\"http://mirror.i3d.net/pub/centos/7/os/x86_64\"\n\
# Use graphical install\n\
graphical\n\
# Run the Setup Agent on first boot\n\
firstboot --enable\n\
ignoredisk --only-use=vda\n\
# Keyboard layouts\n\
keyboard --vckeymap=fr --xlayouts='fr','gb'\n\
# System language\n\
lang en_GB.UTF-8\n\
reboot\n\
\n\
# Network information\n\
network  --bootproto=static --device=ens3 --gateway=10.250.12.254 --ip=10.250.12.{} --nameserver=8.8.8.8 --netmask=255.255.255.0 --ipv6=auto --activate\n\
network  --hostname=localhost.localdomain\n\
\n\
# Root password\n\
rootpw --iscrypted $6$uBFmnJsMJwDCSg6X$0ravUa6sStRGGqKAXj3W8XojLJ0U9GGUQfbBXWiRIxQJ.4tQ24Z3Yav2CaR12baI5qnw8UNLXpOK8tmw5UZRU1\n\
# System timezone\n\
timezone Europe/Paris --isUtc\n\
user --name=elliot --password=$6$74eCHOigwdSLZtbG$Wnu8trrrs1y48Jm.JQLNCjRza/Am2dkvxGHV8rg2lfQqe8PUrPaTG0qYKV8q4uO7bfMBjdzQTWNMyXXzVH.33/ --iscrypted --gecos=\"elliot\"\n\
# System bootloader configuration\n\
bootloader --append=\" crashkernel=auto\" --location=mbr --boot-drive=vda\n\
autopart --type=lvm\n\
# Partition clearing information\n\
clearpart --none --initlabel\n\
\n\
%packages\n\
@^minimal\n\
@core\n\
kexec-tools\n\
\n\
%end\n\
\n\
%addon com_redhat_kdump --enable --reserve-mb='auto'\n\
\n\
%end \
".format(ip_number)

ks_file.write(ks_str)
ks_file.close()

vm_install_cmd = "virt-install \
--name={} --memory=1024 --vcpus=1 \
--location='http://mirror.i3d.net/pub/centos/7/os/x86_64' \
--disk=/var/lib/libvirt/images/{}.qcow2,device=disk,bus=virtio,size=20 \
--network bridge:br0 \
--os-type=linux \
--initrd-inject='{}' \
--extra-args 'ks=file:/{}.ks'\
".format(vm_name, vm_name, os.path.realpath(ks_file.name), vm_name)

print(vm_install_cmd)
os.system(vm_install_cmd)
