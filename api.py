# This file mocks the provisioning of VM from the MicroStack machines
import paramiko
from config_util import get_config_values
from util import get_server_enum
import os

VM_PORT = 22

# Returns the result of the provisioning
def provision_vm(selected_server):
    server_name = get_server_enum(selected_server)
    config = get_config_values()[server_name]
    ipaddress = config["ipaddress"]
    username = config["username"]
    pwd = input("Insert host {} passsword: \n".format(ipaddress))
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    print("Connecting to host {}, with username {} and password {}".format(ipaddress, username, pwd))
    p.connect(ipaddress, port=VM_PORT, username=username, password=pwd)
    print("Connection successful. Reserving virtual machine ...")
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


open_vm(1)