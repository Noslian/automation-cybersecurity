from falconpy import APIHarnessV2
from key import CLIENTS

# Função responsável por autênticar e executar ações na console do falcon
def get_auth(client):
    response = APIHarnessV2(client_id=client['CLIENT_ID'], client_secret=client['CLIENT_SECRET'])
    return response

# Função responsável por pegar o detalhe doo host
def get_host_details(falcon, idlist):
    response = falcon.command("GetDeviceDetailsV2", ids=idlist)

    host_details_list = []

    for resource in response['body']['resources']:
        host_name = resource.get("hostname", "N/A")
        connection_ip = resource.get("connection_ip", "N/A")
        os_version = resource.get("os_version", "N/A")
        agent_version = resource.get("agent_version", "N/A")
        first_seen = resource.get("first_seen", "N/A")
        last_seen = resource.get("last_seen", "N/A")
        host_details_list.append({"Hostname": host_name, "Connection_IP": connection_ip, "OS_Version": os_version, "Versao_Sensor": agent_version, "First_Seen": first_seen, "Last_Seen": last_seen})

    return host_details_list

def get_version(falcon, filter, index, sort):
    response = falcon.command("GetCombinedSensorInstallersByQuery",
                          sort=sort,
                          filter=filter
                          )
    
    version = response['body']['resources'][index]['version']
    return version

# Função que pega o id do host baseado no filtro
def get_host_id(falcon, filter, offset=None):
    response = falcon.command("QueryDevicesByFilter",
                                offset = offset,
                                sort = 'hostname.asc',
                                filter=filter
    )
    
    hostid = response['body']['resources']
    return hostid

def query_host(falcon, filter):
    idhost_matrix = [[]]
    offset = 0
    idhost = get_host_id(falcon, filter, offset)

    while len(idhost) > 0:
        idhost_matrix[0].extend(idhost)
        offset += len(idhost)
        idhost = get_host_id(falcon, filter, offset)
    
    return idhost_matrix[0]

if __name__ == "__main__":
    for client in CLIENTS:
        falcon = get_auth(client)
        auth = falcon.authenticate()

        if auth == True:
            filter_platform_query = {"win": "platform:'windows'", "lin": "platform:'linux'", "mac": "platform:'mac'"}
            index = 0
            sort="version|asc"

            minor_version_windows  = get_version(falcon, filter_platform_query['win'], index, sort) + ".0"
            minor_version_linux = get_version(falcon, filter_platform_query['lin'], index, sort) + ".0"
            minor_version_mac = get_version(falcon, filter_platform_query['mac'], index, sort) + ".0"

            filter_query_win = f"platform_name:'Windows' + agent_version:<='{minor_version_windows}'" 
            host_win_unsupp = query_host(falcon, filter_query_win)
            filter_query_lin = f"platform_name:'Linux' + agent_version:<='{minor_version_linux}'"
            host_lin_unsupp = query_host(falcon, filter_query_lin)
            filter_query_mac = f"platform_name:'Mac' + agent_version:<='{minor_version_mac}'"
            host_mac_unsupp = query_host(falcon, filter_query_mac)
            host_unsupp = host_win_unsupp + host_lin_unsupp + host_mac_unsupp

            if not host_unsupp:
                print(f"\nCliente: {client['CLIENT']} - Sem hosts com versão do sensor não suportados")
            else:
                print(f"\nCliente: {client['CLIENT']} - Hosts com versão do sensor não suportados: {len(host_unsupp)} hosts")
                for idhost in host_unsupp:
                    host_details = get_host_details(falcon, [idhost])
                    for detail in host_details:
                        #print(f"Hostname: {detail['Hostname']} - IP: {detail['Connection_IP']} - Last Seen: {detail['Last_Seen']} - First Seen: {detail['First_Seen']} - OS Version: {detail['OS_Version']}")
                        print(f"{detail['Hostname']} - {detail['Versao_Sensor']}")
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credênciais.")