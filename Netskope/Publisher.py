import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

tenants_str = os.getenv('TENANTS')

try:
    tenants = json.loads(tenants_str) if tenants_str else []
except json.JSONDecodeError as e:
    print(f"Erro ao analisar a string TENANTS: {e}")
    tenants = []

for tenant_info in tenants:
    tenant_url = tenant_info.get('TENANT_URL')
    api_token = tenant_info.get('API_TOKEN')
    api_endpoint = '/api/v2/infrastructure/publishers'

    cliente_info = tenant_info.get('CLIENTE', {})
    cliente_nome = cliente_info.get('NOME', 'Nome não fornecido')

    url = f'{tenant_url}{api_endpoint}'

    headers = {
        'accept': 'application/json',
        'Netskope-Api-Token': api_token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta uma exceção se a solicitação for mal-sucedida

        data = response.json()

        publishers = data['data']['publishers']
        for publisher in publishers:
            publisher_name = publisher['publisher_name']
            status = publisher['status']
            version = publisher['assessment']['version']

            print("\n" + '-' * 30)
            print(f"Cliente: {cliente_nome}")
            print(f"Tenant URL: {tenant_url}")
            print(f"Publisher Name: {publisher_name}")
            print(f"Status: {status}")
            print(f"Version: {version}")
            print('-' * 30)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a chamada para o Tenant {tenant_url}: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao analisar a resposta JSON para o Tenant {tenant_url}: {e}")
