#version=DEVEL
# System authorization information
auth --enableshadow --passalgo=sha512
# Use network installation
url --url="http://mirror.i3d.net/pub/centos/7/os/x86_64"
# Use graphical install
graphical
# Run the Setup Agent on first boot
firstboot --enable
ignoredisk --only-use=sda
# Keyboard layouts
keyboard --vckeymap=fr --xlayouts='fr','gb'
# System language
lang en_GB.UTF-8
reboot

# Network information
network  --bootproto=static --device=ens3 --gateway=10.250.12.254 --ip=10.250.12.85 --nameserver=8.8.8.8 --netmask=255.255.255.0 --ipv6=auto --activate
network  --hostname=localhost.localdomain

# Root password
rootpw --iscrypted $6$uBFmnJsMJwDCSg6X$0ravUa6sStRGGqKAXj3W8XojLJ0U9GGUQfbBXWiRIxQJ.4tQ24Z3Yav2CaR12baI5qnw8UNLXpOK8tmw5UZRU1
# System timezone
timezone Europe/Paris --isUtc
user --name=elliot --password=$6$74eCHOigwdSLZtbG$Wnu8trrrs1y48Jm.JQLNCjRza/Am2dkvxGHV8rg2lfQqe8PUrPaTG0qYKV8q4uO7bfMBjdzQTWNMyXXzVH.33/ --iscrypted --gecos="elliot"
# System bootloader configuration
bootloader --append=" crashkernel=auto" --location=mbr --boot-drive=vda
#autopart --type=lvm
zerombr
clearpart --all --drives=vda
part /boot --asprimary --size=500
part / --asprimary --size=8000
part swap --size=1024
# Partition clearing information
#clearpart --none --initlabel

%packages
@^minimal
@core
kexec-tools

%end

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end
