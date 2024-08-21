from g_functions import CLIENTS, get_auth, get_host_id, get_host_details

if __name__ == "__main__":
# def sensor_rfm():
    for client in CLIENTS:
        
        falcon = get_auth(client)
        auth = falcon.authenticate()

        if auth == True:
            filter_query = f"reduced_functionality_mode:'yes'"
            idhost = get_host_id(falcon,filter_query)
            if idhost != []:
                host_details = get_host_details(falcon, idhost)
                
                print(f"Cliente: {client['CLIENT']} - Presença de hosts com Sensor em RFM: {len(host_details)} hosts") 
                for detail in host_details:
                    print(f"{detail['Hostname']} - {detail['OS_Version']} - {detail['Connection_IP']} - {detail['Versao_Sensor']}")
                    #print(f"Hostname: {detail['Hostname']} - IP: {detail['Connection_IP']} - Last Seen: {detail['Last_Seen']} - First Seen: {detail['First_Seen']} - OS Version: {detail['OS_Version']}")
                print(" ")   
            else:             
                print(f"\nCliente: {client['CLIENT']} - Sem sensor RFM") 
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credênciais.")



          