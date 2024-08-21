from g_functions import CLIENTS, get_auth, get_host_id, get_host_details, status_offline, query_host

if __name__ == "__main__":
# def server_off():
    for client in CLIENTS:
        
        falcon = get_auth(client)
        auth = falcon.authenticate()

        if auth == True:
            filter_query = f"(product_type_desc: 'Server') OR (product_type_desc: 'Domain Controller')"
            idhost_ = query_host(falcon, filter_query)
            host_offline = status_offline(falcon, idhost_) 
            
            if host_offline != []:
                host_details = get_host_details(falcon, host_offline)
                print(f"\nCliente: {client['CLIENT']} - Servidores offline: {len(host_offline)}") 
                for detail in host_details:
                    print(f"{detail['Hostname']} - {detail['OS_Version']} - {detail['Connection_IP']} ") #- Last Seen: {detail['Last_Seen']}
            else:             
                print(f"\nCliente: {client['CLIENT']} - Sem Servidores offline")
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credênciais.")