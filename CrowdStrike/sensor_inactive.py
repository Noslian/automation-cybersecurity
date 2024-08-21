from g_functions import CLIENTS, get_auth, get_host_details, get_date_days_ago, query_host

if __name__ == "__main__":

    for client in CLIENTS:
        falcon = get_auth(client)
        auth = falcon.authenticate()

        if auth == True:
            sensor_inactive = get_date_days_ago(30)
            filter_query = f"(last_seen:<'{sensor_inactive}')"
            idhost = query_host(falcon, filter_query)

            if not idhost:
                print(f"\nCliente: {client['CLIENT']} - Sem hosts no status de Inactive Sensor")
            else:
                print(f"\nCliente: {client['CLIENT']} - Hosts no status de Inactive Sensor (30 dias ou mais): {len(idhost)} hosts")
                for idhost in idhost:
                    host_details = get_host_details(falcon, [idhost])
                    for detail in host_details:
                        #print(f"Hostname: {detail['Hostname']} - IP: {detail['Connection_IP']} - Last Seen: {detail['Last_Seen']} - First Seen: {detail['First_Seen']} - OS Version: {detail['OS_Version']}")
                        print(f"{detail['Hostname']} - {detail['OS_Version']} - {detail['Connection_IP']}")
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credênciais.")