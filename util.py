from server import Server

def get_server_enum(selected_server):
    server_list = list(Server)
    for server in server_list:
        if selected_server == server.value:
            return server.name
    raise Exception("Selected server not in the possible servers list")
