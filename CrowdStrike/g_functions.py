from key import CLIENTS #, C_LABS
import datetime
from datetime import timedelta
from falconpy import APIHarnessV2
import json

# Função para pegar os dias atrás (qtd que você quer)
def get_date_days_ago(day):
    days_ago = datetime.datetime.now() - timedelta(days=day)
    formatted_date = days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
    return formatted_date

# Função responsável por autênticar e executar ações na console do falcon
def get_auth(client):
    response = APIHarnessV2(client_id=client['CLIENT_ID'], client_secret=client['CLIENT_SECRET'])
    return response

# Função responsável por pegar o ltds pra função get_detection
def get_ldts(falcon, filter_query):
    response = falcon.command("QueryDetects", parameters={
        "filter": filter_query,
    })
    
    ldts = response['body']['resources']
    return ldts

# Função que traz a quantidade de detecções de acordo com o filtro
def get_detection(falcon,ldts):
    
    BODY = {
     "ids": ldts
    }
    
    response = falcon.command("GetDetectSummaries", body=BODY)
    
    return response['body']['resources']

# Função que pega o id do host baseado no filtro
def get_host_id(falcon, filter, offset=None):
    response = falcon.command("QueryDevicesByFilter",
                                offset = offset,
                                sort = 'hostname.asc',
                                filter=filter
    )
    
    hostid = response['body']['resources']
    return hostid

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

def query_host(falcon, filter):
    idhost_matrix = [[]]
    offset = 0
    idhost = get_host_id(falcon, filter, offset)

    while len(idhost) > 0:
        idhost_matrix[0].extend(idhost)
        offset += len(idhost)
        idhost = get_host_id(falcon, filter, offset)
    
    return idhost_matrix[0]

def status_offline(falcon, idhosts):
    all_offline_hosts = []
    for i in range(0, len(idhosts), 100):
        ids_chunk = idhosts[i:i + 100]
        
        response = falcon.command("GetOnlineState_V1", ids=ids_chunk)
        
        for resource in response['body']['resources']:
            idhost_off = resource.get("id", "N/A")
            state_off = resource.get("state", "N/A")
            
            if state_off == "offline":
                all_offline_hosts.append(idhost_off)
    
    return all_offline_hosts
