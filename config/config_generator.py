# Atualizar esse arquivo sempre que necessário acrescentar uma nova configuração de servidor
import configparser
from config_util import save_config, display_config_content

conf_file = configparser.ConfigParser()

# Editar essa parte do arquivo para atualizar a configuração
# INICIO_DA_PARTE_MANUAL
conf_file["ServerOne"] = {
    "IPAddress": "172.16.31.220",
    "Username": "pfc_navarro_adriano"
}

conf_file["ServerTwo"] = {
    "IPAddress": "172.16.31.192",
    "Username": "pfc_navarro_adriano"
}
# FIM_DA_PARTE_MANUAL

save_config(conf_file)
display_config_content()