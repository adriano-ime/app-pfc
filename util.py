from server import Server

BASE_COMMAND = "ssh -i /home/pfc_navarro_adriano/snap/microstack/common/.ssh/id_microstack cirros@"

def get_server_enum(selected_server):
    server_list = list(Server)
    for server in server_list:
        if selected_server == server.value:
            return server.name
    raise Exception("Selected server not in the possible servers list")

def get_server_access_command(server_networks):
    return BASE_COMMAND + server_networks.split(',')[-1]