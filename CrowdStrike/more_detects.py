"""
Script para listar as detecções novas, não atribuídas na console do Crowdstrike. 

O intuito é notificar o cliente a fim de cadastrar falso positivo e diminuir o número de detecções.

brunoabreusz
Data: 25/03/2024
Versão: 2.0
"""

from falconpy import APIHarnessV2
from g_functions import CLIENTS

EMPTY_FILENAME = "(empty)"

def get_auth(client):
    """Autentica na console do Falcon e retorna a sessão."""
    return APIHarnessV2(client_id=client['CLIENT_ID'], client_secret=client['CLIENT_SECRET'])

def get_ldts(falcon, filter_query):
    """Obtém todos os identificadores de detecção baseados em uma consulta de filtro."""
    all_ldts = []
    offset = 0
    while True:
        response = falcon.command("QueryDetects", parameters={"filter": filter_query, "offset": offset})
        ldts = response['body']['resources']
        if not ldts:
            break
        all_ldts.extend(ldts)
        offset += len(ldts)
    return all_ldts

def get_detection(falcon, ldts):
    """Obtém sumários de detecção a partir de uma lista de identificadores de detecção."""
    response = falcon.command("GetDetectSummaries", body={"ids": ldts})
    return response['body']['resources']

def process_detections(detections):
    """Conta a frequência de cada filename e retorna uma lista ordenada dos 10 primeiros."""
    filename_counts = {}
    processed_behaviors = set()

    for detection in detections:
        for behavior in detection.get("behaviors", []):
            behavior_key = (detection['detection_id'], behavior['behavior_id'])
            if behavior_key in processed_behaviors:
                continue
            processed_behaviors.add(behavior_key)

            filename = behavior.get("filename", "").strip() or EMPTY_FILENAME
            filename_counts[filename] = filename_counts.get(filename, 0) + 1

    top_filenames = sorted(filename_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_filenames

if __name__ == "__main__":
    for client in CLIENTS:
        falcon = get_auth(client)
        if falcon.authenticate():
            all_ldts = get_ldts(falcon, filter_query="(status:'new')")
            detections = get_detection(falcon, all_ldts)
            top_filenames = process_detections(detections)
            
            print(f"Cliente: {client['CLIENT']}")
            print(f"   {len(all_ldts)} Detecções com o Status 'new'")
            if top_filenames:
                for filename, count in top_filenames:                    
                    print(f"   Filename: {filename}, Quantidade: {count}")
            else:
                print("   Não existem detecções em aberto.")
        else:
            print(f"Cliente: {client['CLIENT']} - Não autenticado, favor verificar as credenciais.")