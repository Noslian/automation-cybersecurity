from g_functions import CLIENTS, get_auth, get_host_details, get_version, query_host

# if __name__ == "__main__":
def sensor_update():
    for client in CLIENTS:
        falcon = get_auth(client)
        auth = falcon.authenticate()

        if auth == True:
            filter_platform_query = {"win": "platform:'windows'", "lin": "platform:'linux' + os:'Debian'", "mac": "platform:'mac'"}
            indexs = [3, 4, 5]
            sort = "version|desc"
            
            for index in indexs:
                version_update_windows  = get_version(falcon, filter_platform_query['win'], index, sort) + ".0"
                version_update_linux = get_version(falcon, filter_platform_query['lin'], index, sort) + ".0"
                version_update_mac = get_version(falcon, filter_platform_query['mac'], index, sort) + ".0"
                
                filter_query_win = f"platform_name:'Windows' + agent_version:'{version_update_windows}'" 
                host_win_out_version = query_host(falcon, filter_query_win)
                filter_query_lin = f"platform_name:'Linux' + agent_version:'{version_update_linux}'"
                host_lin_out_version = query_host(falcon, filter_query_lin)
                filter_query_mac = f"platform_name:'Mac' + agent_version:'{version_update_mac}'"
                host_mac_out_version = query_host(falcon, filter_query_mac)
                
                if index == 3:
                    host_61_90_days = host_win_out_version + host_lin_out_version + host_mac_out_version
                elif index == 4:
                    host_31_60_days = host_win_out_version + host_lin_out_version + host_mac_out_version
                else:
                    host_30_days = host_win_out_version + host_lin_out_version + host_mac_out_version

            if not host_61_90_days:
                print(f"\nCliente: {client['CLIENT']} - Sem hosts com sensor desatualizado: 61-90 dias")
            else:
                print(f"\nCliente: {client['CLIENT']} - Hosts com sensor suportado até 61-90 dias: {len(host_61_90_days)} hosts")
                for idhost in host_61_90_days:
                    host_details = get_host_details(falcon, [idhost])
                    for detail in host_details:
                        #print(f"Hostname: {detail['Hostname']} - Versão do Sensor: {detail['Versao_Sensor']} - IP: {detail['Connection_IP']} - Last Seen: {detail['Last_Seen']} - First Seen: {detail['First_Seen']} - OS Version: {detail['OS_Version']}")
                        print(f"{detail['Hostname']} - {detail['OS_Version']} - {detail['Connection_IP']}")
                        
            if not host_31_60_days:
                print(f"\nCliente: {client['CLIENT']} - Sem hosts com sensor desatualizado: 31-60 dias")
            else:
                print(f"\nCliente: {client['CLIENT']} - Hosts com sensor suportado até 31-60 dias: {len(host_31_60_days)} hosts")
                for idhost in host_31_60_days:
                    host_details = get_host_details(falcon, [idhost])
                    for detail in host_details:
                        #print(f"Hostname: {detail['Hostname']} - Versão do Sensor: {detail['Versao_Sensor']} - IP: {detail['Connection_IP']} - Last Seen: {detail['Last_Seen']} - First Seen: {detail['First_Seen']} - OS Version: {detail['OS_Version']}")
                        print(f"{detail['Hostname']} - {detail['OS_Version']} - {detail['Connection_IP']}")
                        
            if not host_30_days:
                print(f"\nCliente: {client['CLIENT']} - Sem hosts com sensor desatualizado: 30 dias")
            else:
                print(f"\nCliente: {client['CLIENT']} - Hosts com sensor suportado até 30 dias: {len(host_30_days)} hosts")
                for idhost in host_30_days:
                    host_details = get_host_details(falcon, [idhost])
                    for detail in host_details:
                        #print(f"Hostname: {detail['Hostname']} - Versão do Sensor: {detail['Versao_Sensor']} - IP: {detail['Connection_IP']} - Last Seen: {detail['Last_Seen']} - First Seen: {detail['First_Seen']} - OS Version: {detail['OS_Version']}")
                        print(f"{detail['Hostname']} - {detail['OS_Version']} - {detail['Connection_IP']}")
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credênciais.")