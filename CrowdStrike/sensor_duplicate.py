from falconpy import APIHarnessV2
from key import CLIENTS
from concurrent.futures import ThreadPoolExecutor

def get_auth(client):
    response = APIHarnessV2(client_id=client['CLIENT_ID'], client_secret=client['CLIENT_SECRET'])
    return response

def get_host_details(falcon, idlist):
    response = falcon.command("GetDeviceDetailsV2", ids=idlist)
    host_details_list = [
        {k: resource.get(k, "N/A") for k in ["hostname", "connection_ip", "os_version", "agent_version", "first_seen", "last_seen"]}
        for resource in response['body']['resources']
    ]
    return host_details_list

def query_host(falcon, filter):
    idhost_matrix = []
    offset = 0
    while True:
        response = falcon.command("QueryDevicesByFilter", offset=offset, sort='hostname.asc', filter=filter)
        idhost = response['body']['resources']
        if not idhost:
            break
        idhost_matrix.extend(idhost)
        offset += len(idhost)
    return idhost_matrix

def collect_and_check_duplicates(falcon, hosts_ids):
    all_details = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_host_details, falcon, hosts_ids[i:i+100]) for i in range(0, len(hosts_ids), 100)]
        for future in futures:
            all_details.extend(future.result())

    hostname_count = {}
    for detail in all_details:
        hostname = detail['hostname']
        hostname_count[hostname] = hostname_count.get(hostname, 0) + 1

    duplicates = {host: count for host, count in hostname_count.items() if count > 1}
    return duplicates

if __name__ == "__main__":
    for client in CLIENTS:
        falcon = get_auth(client)
        auth = falcon.authenticate()
        if auth:
            filter_query_win = "platform_name:'Windows'" 
            host_win = query_host(falcon, filter_query_win)
            filter_query_lin = "platform_name:'Linux'"
            host_lin = query_host(falcon, filter_query_lin)
            filter_query_mac = "platform_name:'Mac'"
            host_mac = query_host(falcon, filter_query_mac)
            all_host = host_win + host_lin + host_mac

            duplicates = collect_and_check_duplicates(falcon, all_host)

            if not duplicates:
                print(f"Cliente: {client['CLIENT']} - Sem hosts com hostname duplicado.")
            else:
                print(f"Cliente: {client['CLIENT']} - {len(duplicates)} Hostnames duplicados encontrados.")
                print("Exibindo os primeiros 10 dispositivos.")
                for i, (hostname, count) in enumerate(duplicates.items()):
                    if i < 10:
                        print(f"    {hostname}: {count}")
                    else:
                        break
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credenciais.")