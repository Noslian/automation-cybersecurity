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
    api_endpoint_publishers = '/api/v2/infrastructure/publishers'

    cliente_info = tenant_info.get('CLIENTE', {})
    cliente_nome = cliente_info.get('NOME', 'Nome não fornecido')

    try:
        url_publishers = f'{tenant_url}{api_endpoint_publishers}'
        headers_publishers = {
            'accept': 'application/json',
            'Netskope-Api-Token': api_token
        }

        response_publishers = requests.get(url_publishers, headers=headers_publishers)
        response_publishers.raise_for_status()

        data_publishers = response_publishers.json()
        publishers = data_publishers.get('data', {}).get('publishers', [])

        for publisher in publishers:
            publisher_id = publisher.get('publisher_id')
            url_apps = f'{tenant_url}{api_endpoint_publishers}/{publisher_id}/apps'
            headers_apps = {
                'accept': 'application/json',
                'Netskope-Api-Token': api_token
            }

        response_apps = requests.get(url_apps, headers=headers_apps)
        response_apps.raise_for_status()

        data_apps = response_apps.json()
        
        if isinstance(data_apps, dict) and 'data' in data_apps:
            private_apps_count = len(data_apps['data'])
            reachable_count = 0
            unreachable_count = 0
            unknown_count = 0

            for app in data_apps['data']:
                reachability = app.get('reachability')
                if reachability is None:
                    unknown_count += 1
                elif isinstance(reachability, dict) and not reachability.get('reachable'):
                    unreachable_count += 1
                elif isinstance(reachability, dict) and reachability.get('reachable'):
                    reachable_count += 1

            print(f"\nCliente: {cliente_nome}")
            print(f"Total de Private Apps criados: {private_apps_count}, Acessíveis: {reachable_count}, Inacessíveis: {unreachable_count}, Desconhecido: {unknown_count}\n")

            for app in data_apps['data']:
                app_name = app.get('name')
                reachability = app.get('reachability')

                if isinstance(reachability, dict) and not reachability.get('reachable'):
                    print('-' * 30)
                    print(f"Aplicação: {app_name}")
                    error_string = reachability.get('error_string', 'Sem informação de erro')
                    print(f"Erro: {error_string}")
                    print("Acessível: Não")
                    # print('-' * 30)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a chamada para o Tenant {tenant_url}: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao analisar a resposta JSON para o Tenant {tenant_url}: {e}")
