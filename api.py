# This file mocks the provisioning of VM from the MicroStack machines
from sqlite3 import connect
import paramiko
from config_util import get_config_values
from util import get_server_enum
import os

VM_PORT = 22

def connect_to_host(selected_server):
    server_name = get_server_enum(selected_server)
    config = get_config_values()[server_name]
    ipaddress = config["ipaddress"]
    username = config["username"]
    pwd = input("Insert host {} passsword: \n".format(ipaddress))
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    print("Connecting to host {}, with username {} and password {}".format(ipaddress, username, pwd))
    p.connect(ipaddress, port=VM_PORT, username=username, password=pwd)
    print("Connection successful")
    return p

# Returns the result of the provisioning
def provision_vm(selected_server):
    p = connect_to_host(selected_server)
    print("Reserving virtual machine ...")
    stdin, stdout, stderr = p.exec_command("microstack launch cirros -n test")
    opt = stdout.readlines()
    opt = "".join(opt)
    print("Virtual Machine successfully reserved")
    return opt

def open_vm(selected_server):
    server_name = get_server_enum(selected_server)
    config = get_config_values()[server_name]
    ipaddress = config["ipaddress"]
    username = config["username"]
    command = "ssh {}@{} 'ls -l'".format(username, ipaddress)
    os.system("""osascript -e 'tell application "Terminal" to do script "{}"'""".format(command))

def get_server_list(selected_server):
    p = connect_to_host(selected_server)
    print("Gathering information ...")
    stdin, stdout, stderr = p.exec_command("microstack.openstack server list")
    opt = stdout.readlines()
    opt = "".join(opt)
    return opt

s = get_server_list(1)
# for element in s: 
#     print(element)
# print(s)