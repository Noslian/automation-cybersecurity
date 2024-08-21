from g_functions import CLIENTS, get_date_days_ago, get_auth, get_ldts, get_detection

# if __name__ == "__main__":
def detects():
    for client in CLIENTS:
        
        falcon = get_auth(client)
        auth = falcon.authenticate()

        if auth == True:
         
            three_days_ago_date = get_date_days_ago(day=3)
            filter_query = f"(max_severity_displayname:['High', 'Critical']) + (status:'new') + (assigned_to_name:null)  ')" #   + (last_behavior:>'{three_days_ago_date}
            ldts = get_ldts(falcon,filter_query)
            detections = get_detection(falcon,ldts)

            count_severity = {"Critical": 0, "High": 0}

            for detection in detections:
    
                 id = detection['device']['cid']
                 behaviors = detection['behaviors']
                 severity = detection['max_severity_displayname']
         
                 if severity == "High":
                     count_severity[severity] += 1 
                 elif severity == "Critical":
                     count_severity[severity] += 1 
            
            print(f"Cliente: {client['CLIENT']} - Detecções HIGH e CRITICAL não atribuída.") 
            print("Critical: %3d\nHigh: %3d\n" % (count_severity["Critical"], count_severity["High"]))
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credênciais.")