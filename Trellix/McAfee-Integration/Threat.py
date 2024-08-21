import requests
import base64
from datetime import datetime, timedelta

def auth(username, password):
    auth_url = 'https://api.soc.trellix.com/identity/v1/login'
    encoded_credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Cache-Control': 'no-cache',
    }
    response = requests.get(auth_url, headers=headers)
    if response.status_code == 200:
        print("Autenticação bem-sucedida!")
        return response.json()['AuthorizationToken']
    else:
        print(f"Falha na autenticação: {response.status_code} - {response.text}")
        return None

def get_threats(token, from_time_ms):
    url = 'https://api.soc.trellix.com/ft/api/v2/ft/threats'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept-Encoding': 'gzip'
    }
    params = {
        'sort': '-rank',
        'filter': '{"severities":["s1", "s2", "s3", "s4", "s5"]}',
        'limit': 5,
        'from': from_time_ms
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar ameaças: {response.status_code} - {response.text}")
        return {}

def count_severities(threats, counts):
    if 'threats' in threats:
        for threat in threats['threats']:
            severity = threat['severity']
            if severity in counts:
                counts[severity] += 1
    else:
        print("Não foram encontrados dados na resposta.")

if __name__ == "__main__":
    username = "username"
    password = "password"

    token = auth(username, password)
    if token:
        current_time = datetime.utcnow()
        counts = {'s1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0}

        # Iterar sobre cada hora das últimas 24 horas
        for offset in range(24):
            next_pull = current_time - timedelta(hours=offset + 1)
            epoch_pull = str(int(datetime.timestamp(next_pull) * 1000))[:13]  # Convertendo e truncando

            threats = get_threats(token, epoch_pull)
            count_severities(threats, counts)

        print(f"Counts of threats from the last 24 hours: {counts}")
