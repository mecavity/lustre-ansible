#!/usr/bin/python

import os, sys, fileinput

if len(sys.argv) < 2:
    print("-h for help")
    quit()

if sys.argv[1] == '-h':
    print("First argument: Machine name")
    print("Second argument: Machine IP")
    print("Third argument: Machine role in lustre [mgs-mdt|oss]")
    quit()

if len(sys.argv) < 4:
    print("ERROR: Missing arguments. -h for help")
    quit()

name = sys.argv[1]
ip_number = sys.argv[2]
vm_role = sys.argv[3]

print(vm_role)
if vm_role != 'mgs-mdt' and vm_role != 'oss':
    print("Machine role must be [msg-mdt|oss]")
    quit()

ansible_host_groups = ['centOS', 'lustre-{}'.format(vm_role)]
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

# Add the new ip to all the correct groups in ansible hosts file
for host in ansible_host_groups:
    add_host = "sudo sed -i 's/\(\[{}\]\)/\\1\\n10.250.12.{}/' /etc/ansible/hosts".format(host, ip_number)
    print(add_host)
    os.system(add_host)

print(vm_install_cmd)
os.system(vm_install_cmd)
