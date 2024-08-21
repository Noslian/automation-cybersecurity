import json
import requests
from requests_ntlm import HttpNtlmAuth
import urllib3
import time
from datetime import datetime, timezone, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('keys.json', 'r') as file:
    api_keys = json.load(file)

def get_access_token(hostname, port, username, password):
    auth_url = f"https://{hostname}:{port}/DatAdvantage/api/authentication/win"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(auth_url, headers=headers, data="grant_type=client_credentials", auth=HttpNtlmAuth(username, password), verify=False)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Erro na requisição de autenticação: {response.status_code}")
        print(response.text)
        return None

def monitor_alerts():
        since_time = datetime.now(timezone.utc) - timedelta(minutes=2240)

        for client, keys in api_keys.items():
            access_token = get_access_token(keys['hostname'], keys['port'], keys['username'], keys['password'])
            
            if access_token:
                alerts_url = f"https://{keys['hostname']}:{keys['port']}/DatAdvantage/api/alert/alert/GetAlerts"
                params = {
                    'severity': ['Medium'],
                    'startTime': since_time.isoformat(), # Pega alertas de 20 min atrás
                    'maxResult': 50,
                    'descendingOrder': True # Pegar os ultimos alertas 
                }

                headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

                response = requests.get(alerts_url, headers=headers, params=params, verify=False)
                
                if response.status_code == 200:
                    alerts = response.json()
                    high_alert = [alert for alert in alerts if alert.get('Severity') == 'Medium']

                    if high_alert:
                        print(f"[NORMAL] Existe {len(high_alert)} alertas nos últimos 20 minutos na console do Varonis do Cliente: {client}")
                    else:
                        print(f"Sem novos alertas de alta severidade nos últimos 20 minutos na console do Varonis do Cliente: {client}")
                else:
                    print(f"Erro na requisição de alertas: {response.status_code}")
                    print(response.text)
        
if __name__ == "__main__":
    monitor_alerts()