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
            Const.NSKP_ALERT_TYPE: Const.ALERT_TYPE_DLP,
            Const.NSKP_ITERATOR_NAME: "ITERATOR_NAME", 
            Const.NSKP_USER_AGENT: "USER_AGENT" 
        }

        iterator = NetskopeIterator(params)

        end_timestamp = int(time.mktime(time.localtime()))     

        start_timestamp = end_timestamp - (24 * 60 * 60)

        incidentes_unicos = {}

        for offset in range(0, 24 * 3600, 3600):
            current_timestamp = start_timestamp + offset
            try:
                response = iterator.download(current_timestamp)

                if response.status_code == Const.SUCCESS_OK_CODE:
                    data = response.json()
                            
                    if data.get('result'):
                        for evento in data.get('result', []):
                            if evento.get("exposure") == "external":
                                identificador = evento.get("object") 
                                if identificador not in incidentes_unicos:
                                    incidentes_unicos[identificador] = evento
                                # else:
                                #     evento_existente = incidentes_unicos[identificador]
                                #     if evento.get("severity") > evento_existente.get("severity"):
                                #         incidentes_unicos[identificador] = evento
                else:
                    print(f"Erro na chamada da API para o timestamp {current_timestamp}: {response.status_code}")
            except RequestException as e:
                print(f"Exceção ao fazer requisições para a API: {e}")
                traceback.print_exc()

        print(f"Incidentes DLP filtrados para o tenant {tenant['CLIENTE']['NOME']}: {len(incidentes_unicos)}, nas últimas 24 horas.\n")
        for evento in incidentes_unicos.values():
            print(f"ID: {evento.get('_id')}")
            print(f"Usuário: {evento.get('user')}")
            print(f"Exposição: {evento.get('exposure')}")
            print(f"Aplicação: {evento.get('app')}")
            print(f"Nome do Alerta: {evento.get('alert_name')}")
            print(f"Nome do Objeto: {evento.get('object')}")
            print(f"Metodo de Acesso: {evento.get('access_method')}")
            print(f"Atividade: {evento.get('activity')}")
            print(f"Regra de DLP: {evento.get('dlp_rule')}\n")