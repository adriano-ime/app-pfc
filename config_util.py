import configparser

def save_config(conf_file):
    with open(r"configurations.ini", 'w') as configfileObj:
        print("Updating configuration.ini file...")
        conf_file.write(configfileObj)
        configfileObj.flush()
        configfileObj.close()

def display_config_content():
    print("Config file 'configurations.ini' updated")
    read_file = open("configurations.ini", "r")
    content = read_file.read()
    print("Content of the config file are:\n")
    print(content)
    read_file.flush()
    read_file.close()

def get_config_values():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config
