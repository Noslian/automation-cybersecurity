import os
import json
from netskope_api.iterator.netskope_iterator import NetskopeIterator
from netskope_api.iterator.const import Const
from requests.exceptions import RequestException
import traceback
import time
from dotenv import load_dotenv

load_dotenv()

tenants_json = os.getenv('TENANTS')

if tenants_json:
    tenants = json.loads(tenants_json)

    for tenant in tenants:
        params = {
            Const.NSKP_TOKEN: tenant['API_TOKEN'],
            Const.NSKP_TENANT_HOSTNAME: tenant['TENANT_URL'].replace('https://', ''),
            Const.NSKP_EVENT_TYPE: Const.EVENT_TYPE_ALERT,
            Const.NSKP_ALERT_TYPE: Const.ALERT_TYPE_COMPROMISEDC_CREDENTIALS,
            Const.NSKP_ITERATOR_NAME: "ITERATOR_NAME", 
            Const.NSKP_USER_AGENT: "USER_AGENT" 
        }

        iterator = NetskopeIterator(params)

        end_timestamp = int(time.mktime(time.localtime()))     
           
        start_timestamp = end_timestamp - (24 * 60 * 60)
        
        eventos_filtrados = []

        for offset in range(0, 24 * 3600, 3600):
            current_timestamp = start_timestamp + offset
            
            try:
                response = iterator.download(current_timestamp)

                if response.status_code == Const.SUCCESS_OK_CODE:
                    data = response.json()
                    
                    if data.get('result'):
                        for evento in data.get('result', []):
                            evento_filtrado = {
                                "_id": evento.get("_id"),
                                "user": evento.get("user"),
                                "matched_username": evento.get("matched_username"),
                                "breach_date": evento.get("breach_date"),
                                "breach_description": evento.get("breach_description"),
                                "email_source": evento.get("email_source")
                            }
                            eventos_filtrados.append(evento_filtrado)
                else:
                    print(f"Erro na chamada da API para o timestamp {current_timestamp}: {response.status_code}")

            except RequestException as e:
                print(f"Exceção ao fazer requisições para a API: {e}")
                traceback.print_exc()

        print(f"Credenciais comprometidas filtrados para tenant da {tenant['CLIENTE']['NOME']}: {len(eventos_filtrados)}, nas últimas 24 horas.\n")
        for evento in eventos_filtrados:
            print(f"ID: {evento['_id']}")
            print(f"Usuário: {evento['user']}")
            print(f"Usuário correspondente: {evento['matched_username']}")   
            print(f"Metodo de Acesso: {evento['email_source']}")
            print(f"Descrição da violação: {evento['breach_description']}\n")
else:
    print("Não foi possível encontrar a variável de ambiente 'TENANTS'.")
