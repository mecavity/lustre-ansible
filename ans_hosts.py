#!/usr/bin/python

import os, subprocess, re

def mgs_exists(cluster_name):
    with open("/etc/ansible/hosts") as f:
        lines = f.read().splitlines()
        correct_host = 0
        for line in lines:
            if line == "[lustre-mgs-mdt]":
                correct_host = 1
                continue
            if correct_host and re.search("\[.*\]", line):
                break
            if correct_host and re.search(r'cluster_name={0}(?:\s|$)'.format(re.escape(cluster_name)), line):
                return True
        return False

def add_host(ip, role, cluster_name):
    # This checks if an mgs is available for the oss
    # or if we are not overriding an existing mgs
    if mgs_exists(cluster_name):
        if role == 'mgs-mdt':
            print("An mgs for that FS name already exists!")
            quit() #TODO handle better
    elif role == 'oss':
        print("You need to create a mgs FS with that name")
        quit() #TODO handle better

    # Remove new ip from hosts file
    os.system("sudo sed -i '/10.250.12.{0}/d' /etc/ansible/hosts".format(ip))
    if role == 'mgs-mdt':
      add_host = "sudo sed -i 's/\(\[lustre-{0}\]\)/\\1\\n10.250.12.{1} cluster_name={2}/' /etc/ansible/hosts".format(role, ip, cluster_name)
      os.system(add_host)
    elif role == 'oss':
      mgs_ip = subprocess.Popen(["cat /etc/ansible/hosts | grep -m 1 '{0}' | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | tr -d '\n'".format(cluster_name)], stdout=subprocess.PIPE, shell=True)
      mgs_ip = "mgs_ip={0}".format(mgs_ip.communicate()[0])
      add_host = "sudo sed -i 's/\(\[lustre-{0}\]\)/\\1\\n10.250.12.{1} cluster_name={2} {3}/' /etc/ansible/hosts".format(role, ip, cluster_name, mgs_ip)
      print(add_host)
      os.system(add_host)
