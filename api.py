# This file mocks the provisioning of VM from the MicroStack machines
from sqlite3 import connect
import paramiko
from config_util import get_config_values
from parser import parse_microstack_table
from objects import FlavorObject, ImageObject, NetworkObject, SecurityGroupObject, ServerObject, UsageObject
from util import get_server_enum
import os

VM_PORT = 22

def connect_to_host(selected_server):
    server_name = get_server_enum(selected_server)
    config = get_config_values()[server_name]
    ipaddress = config["ipaddress"]
    username = config["username"]
    # pwd = input("Insert host {} passsword: \n".format(ipaddress))
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    print("Connecting to host {}, with username {} and password se9@ime_".format(ipaddress, username))
    p.connect(ipaddress, port=VM_PORT, username=username, password="se9@ime_")
    print("Connection successful")
    return p

# Returns the result of the provisioning
def provision_default_vm(selected_server, name_server):
    name = name_server
    if not name_server or name_server == "":
        name = "test"
    p = connect_to_host(selected_server)
    print("Reserving virtual machine ...")
    stdin, stdout, stderr = p.exec_command("microstack launch cirros -n " + name)
    opt = stdout.readlines()
    opt = "".join(opt)
    print("Virtual Machine successfully reserved")
    return opt 

def provision_vm(selected_server, name, flavor, image, network_id, sec_group_id):
    p = connect_to_host(selected_server)
    print("Reserving virtual machine ...")
    command = "microstack.openstack server create " + name + " --flavor " +flavor + " --image " + image + " --nic net-id=" + network_id + " --security-group " + sec_group_id
    stdin, stdout, stderr = p.exec_command(command)
    opt = stdout.readlines()
    opt = "".join(opt)
    print("Virtual Machine successfully reserved")
    return opt 

def delete_vm(selected_server, vm_id):
    p = connect_to_host(selected_server)
    print("Deleting virtual machine ...")
    stdin, stdout, stderr = p.exec_command("microstack.openstack server delete " + vm_id)
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

def get_list_table(selected_server, command):
    p = connect_to_host(selected_server)
    print("Gathering information ...")
    stdin, stdout, stderr = p.exec_command(command)
    opt = stdout.readlines()
    opt = "".join(opt)
    print("Information succesfully retrieved")
    print(opt)
    return opt

def get_multiple_output_tables(selected_server, command_list):
    print("Gathering multiple information information ...")
    opt_list = []
    for command in command_list:
        print("Running command ", command)
        output = get_list_table(selected_server, command)
        opt_list.append(output)
    return opt_list

def get_usage_objects(usage_table):
    usage_list = parse_microstack_table(usage_table)
    usage_object_list = []
    for index in range(1, len(usage_list)):
        usage_object = UsageObject(usage_list[index][0], usage_list[index][1], usage_list[index][2], usage_list[index][3], usage_list[index][4])
        usage_object_list.append(usage_object)
    return usage_object_list
    
#TODO: Turn all these methods into a single one
def get_available_flavors(flavor_table):
    flavor_list = parse_microstack_table(flavor_table)
    flavor_object_list = []
    for index in range(1, len(flavor_list)):
        flavor_object = FlavorObject(flavor_list[index][1], flavor_list[index][2], flavor_list[index][3], flavor_list[index][4], flavor_list[index][5], flavor_list[index][6])
        flavor_object_list.append(flavor_object)
    return flavor_object_list

def get_available_images(image_table):
    image_list = parse_microstack_table(image_table)
    image_object_list = []
    for index in range(0, len(image_list)):
        image_object = ImageObject(image_list[index][0], image_list[index][1],image_list[index][2])
        image_object_list.append(image_object)
    return image_object_list

def get_available_networks(network_table):
    network_list = parse_microstack_table(network_table)
    network_object_list = []
    for index in range(1,len(network_list)):
        network_object = NetworkObject(network_list[index][0], network_list[index][1], network_list[index][2])
        network_object_list.append(network_object)
    return network_object_list

def get_available_security_groups(security_group_table):
    security_group_list = parse_microstack_table(security_group_table)
    security_group_object_list = []
    for index in range(1,len(security_group_list)):
        security_group_object = SecurityGroupObject(security_group_list[index][0], security_group_list[index][1], security_group_list[index][2], security_group_list[index][3], security_group_list[index][4])
        security_group_object_list.append(security_group_object)
    return security_group_object_list

def get_instantiated_servers(server_table):
    server_list = parse_microstack_table(server_table)
    print(server_list)
    server_object_list = []
    for index in range(1, len(server_list)):
        server_object = ServerObject(server_list[index][0], server_list[index][1], server_list[index][2], server_list[index][3], server_list[index][4], server_list[index][5])
        server_object_list.append(server_object)
    return server_object_list

# s = get_list_table(1, "microstack.openstack server list")
# a = get_instantiated_servers(s)
# print(a[0].networks)