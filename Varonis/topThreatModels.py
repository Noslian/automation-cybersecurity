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

    # Montar a URL
    auth_url = f"https://{hostname}:{port}/DatAdvantage/api/authentication/win"

    payload = "grant_type=client_credentials"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Usar autenticação NTLM 
    auth_response = requests.post(auth_url, headers=headers, data=payload, auth=HttpNtlmAuth(username, password), verify=False)

    if auth_response.status_code == 200:
        auth_response_json = auth_response.json()
        access_token = auth_response_json.get("access_token")

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

            alert_counts = {}
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
                            name = alert.get('Name')
                            severity = alert.get('Severity')
                            if name not in alert_counts:
                                alert_counts[name] = {}
                            if severity in alert_counts[name]:
                                alert_counts[name][severity] += 1
                            else:
                                alert_counts[name][severity] = 1

                        from_alert_seq_id = max(alert['AlertSeqId'] for alert in alerts)
                else:
                    print(f"Erro na requisição de alertas: {alerts_response.status_code}")
                    print(alerts_response.text)
                    has_more_alerts = False

            print(" Principais modelos de ameaças com alertas nas últimas 24 horas:")
            for name, severities in alert_counts.items():
                for severity, count in severities.items():
                    print(f"  Ameaça: {name} \n  Severidade: {severity} \n  Quantidade de Alertas: {count}")
                    print()
        else:
            print("Access Token não encontrado na resposta.")
    else:
        print(f"Erro na requisição de autenticação: {auth_response.status_code}")
        print(auth_response.text)