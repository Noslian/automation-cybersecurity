import requests
import base64
import json


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
        access_token = response.json().get('AuthorizationToken')
        print(access_token)
    else:
        print(f"Falha na autenticação: {response.status_code} - {response.text}")
    

if __name__ == "__main__":
    # Substitua com suas credenciais do cliente
    username = "username"
    password = "password"

    # Obtenha o token de autenticação
    token = auth(username, password)


