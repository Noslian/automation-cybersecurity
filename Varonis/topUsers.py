import json
import requests
from requests_ntlm import HttpNtlmAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('keys.json', 'r') as file:
    api_keys = json.load(file)

for client, keys in api_keys.items():
    print(f"Cliente: {client}")

    port = keys['port']
    hostname = keys['hostname']
    username = keys['username']
    password = keys['password']

    auth_url = f"https://{hostname}:{port}/DatAdvantage/api/authentication/win"
    payload = "grant_type=client_credentials"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    auth_response = requests.post(auth_url, headers=headers, data=payload, auth=HttpNtlmAuth(username, password), verify=False)

    if auth_response.status_code == 200:
        access_token = auth_response.json().get("access_token")

        if access_token:
            alerts_url = f"https://{hostname}:{port}/DatAdvantage/api/alert/alert/GetAlerts"
            params = {
                'lastDays': 1, 
                'maxResult': 50
            }

            alert_headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            user_counts = {}
            from_alert_seq_id = 0
            has_more_alerts = True

            while has_more_alerts:
                params['fromAlertSeqId'] = from_alert_seq_id
                alerts_response = requests.get(alerts_url, headers=alert_headers, params=params, verify=False)

                if alerts_response.status_code == 200:
                    alerts = alerts_response.json()
                    
                    if not alerts:
                        has_more_alerts = False
                    else:
                        for alert in alerts:
                            user = alert.get('UserName')
                            if user in user_counts:
                                user_counts[user] += 1
                            else:
                                user_counts[user] = 1

                        from_alert_seq_id = max(alert['AlertSeqId'] for alert in alerts)
                else:
                    print(f"Erro na requisição de alertas: {alerts_response.status_code}")
                    print(alerts_response.text)
                    has_more_alerts = False

            top_users = sorted(user_counts.items(), key=lambda item: item[1], reverse=True)[:5]

            print(" Top 5 usuários com mais alertas nas últimas 24 horas:")
            for user, count in top_users:
                print(f"  User: {user}\n  Quantidade de Alertas: {count}")
                print()
        else:
            print("Access Token não encontrado na resposta.")
    else:
        print(f"Erro na requisição de autenticação: {auth_response.status_code}")
        print(auth_response.text)