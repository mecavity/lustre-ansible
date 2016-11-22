# lustre-ansible
Fully automated lustre installation and deployment (work in progress!)
---------------------------------------------------------------------

The goal here is purely for educational puposes, I've never done anything like this before and I'm trying to learn through this exercice. I'm want to fully automate the creation of three CentOS VM's using only one script and then install and deploy lustre on them.

One VM will be used as the mgs and mdt, the second as the oss and the third as the client.

I have used KVM as the hypervisor and virsh as a tool to interact with KVM.

A script will launch the creation of the VM's using a kickstarter file I have generated to setup the CentOS machine.

Finaly, the ansible playbook takes care of adding the correct repos, installing the right kernal and the all the modules needed.

Next up
-------

* Formating lustre on the VM spare disk and mounting them.
* Adding the client.
