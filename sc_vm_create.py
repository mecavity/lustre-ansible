#!/usr/bin/python

import os, sys, fileinput, subprocess, ans_hosts

if len(sys.argv) < 2:
    print("-h for help")
    quit()

if sys.argv[1] == '-h':
    print("First argument: Machine name")
    print("Second argument: Machine IP")
    print("Third argument: Machine role in lustre [mgs-mdt|oss]")
    print("Thourth argument: FS name")
    quit()

if len(sys.argv) < 5:
    print("ERROR: Missing arguments. -h for help")
    quit()

name = sys.argv[1]
ip_number = sys.argv[2]
vm_role = sys.argv[3]
clst_name = sys.argv[4]

if vm_role != 'mgs-mdt' and vm_role != 'oss':
    print("Machine role must be [msg-mdt|oss]")
    quit()

vm_name = '{}_{}'.format(name, ip_number)

# Add new vm to ansible hosts
ans_hosts.add_host(ip_number, vm_role, clst_name)

ssh_pub_key = subprocess.Popen(['cat /home/mecavity/.ssh/id_rsa.pub'], stdout=subprocess.PIPE, shell=True)
ssh_pub_key = ssh_pub_key.communicate()[0]

# New kickstarter file
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
##autopart --type=lvm\n\
## Partition clearing information\n\
##clearpart --none --initlabel\n\
clearpart --all --drives=vda\n\
part /boot  --asprimary --size=521\n\
part /      --asprimary --size=8000\n\
part swap               --size=1024\n\
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
%end \n\
%post\n\
mkdir /root/.ssh\n\
echo '{}' > /root/.ssh/authorized_keys\n\
%end\
".format(ip_number, ssh_pub_key)
ks_file.write(ks_str)
ks_file.close()

# Launch vm creation, be carefull if you changed the path to the kickstart file we just created!
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
