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
                'lastDays': 7,
                'maxResult': 50
            }
            alert_headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            alerts_response = requests.get(alerts_url, headers=alert_headers, params=params, verify=False)

            if alerts_response.status_code == 200:
                alerts = alerts_response.json()
                alert_counts = {}

                for alert in alerts:
                    user = alert.get('UserName')
                    name = alert.get('Name')
                    severity = alert.get('Severity')
                    key = (user, name)
                    if key in alert_counts:
                        alert_counts[key] += 1
                    else:
                        alert_counts[key] = 1

                sorted_alert_counts = sorted(alert_counts.items(), key=lambda item: item[1], reverse=True)

                print(" Contagem de alertas por usuário e ameaça nas últimas 7 dias:")
                for (user, name), count in sorted_alert_counts:
                    print(f"  Usuário: {user}\n  Ameaça: {name}, Severidade: {severity}\n  Quantidade de Alertas: {count}")
                    print()
            else:
                print(f"Erro na requisição de alertas: {alerts_response.status_code}")
                print(alerts_response.text)
        else:
            print("Access Token não encontrado na resposta.")
    else:
        print(f"Erro na requisição de autenticação: {auth_response.status_code}")
        print(auth_response.text)
