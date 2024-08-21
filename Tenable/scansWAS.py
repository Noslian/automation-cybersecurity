from tenable.io import TenableIO
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json

load_dotenv()

keys_env = os.getenv("KEYS")

if keys_env:
    api_keys = json.loads(keys_env)
    seven_days_ago = datetime.today() - timedelta(days=7)
    seven_days_ago_formatted = seven_days_ago.strftime('%Y/%m/%d')

    for client, keys in api_keys.items():
        print("\n")
        print(f"Client: {client}")

        access_key = keys['accessKey']
        secret_key = keys['secretKey']
        tio = TenableIO(access_key=access_key, secret_key=secret_key)

        unique_scans = {} 
        scans_found = False

        # Tenta buscar varreduras WAS com status 'aborted' e 'completed'
        for status in ['aborted', 'completed']:
            was_iterator = tio.was.export(
                and_filter=[
                    ("scans_started_at", "gte", seven_days_ago_formatted),
                    ("scans_status", "eq", status)
                ]
            )

            for finding in was_iterator:
                scans_found = True
                scan_id = finding['scan']['scan_id'] 
                scan_name = finding.get('config', {}).get('name', 'Nome do Scan não disponível')
                scan_status = finding.get('scan', {}).get('status', 'Status do Scan não disponível')

                # Usa o ID do scan como chave para garantir a unicidade
                unique_scan_key = f"{scan_id}-{scan_status}"  
                if unique_scan_key not in unique_scans:
                    unique_scans[unique_scan_key] = f"   Nome do Scan: {scan_name}, Status: {scan_status}"

        if not scans_found:
            print(f"   Nenhuma varredura (WAS) encontrada para o cliente {client} nos últimos 7 dias.")
        else:
            for scan_details in unique_scans.values():
                print(scan_details)

else:
    print("API keys not found.")


#         Lógica somente para Scans WAS abortados.

#         seven_days_ago_formatted = seven_days_ago.strftime('%Y/%m/%d')

#         was_iterator = tio.was.export(
#             and_filter=[
#                 ("scans_started_at", "gte", seven_days_ago_formatted),
#                 ("scans_status", "contains", ["aborted"]) #aborted
#             ]
#         )
    
#         unique_scans = {}

#         for finding in was_iterator:
#             scan_id = finding['scan']['scan_id'] 
#             scan_name = finding.get('config', {}).get('name', 'Nome do Scan não disponível')
#             scan_status = finding.get('scan', {}).get('status', 'Status do Scan não disponível')
            
#             if scan_id not in unique_scans:
#                 unique_scans[scan_id] = f"Nome do Scan: {scan_name}, Status: {scan_status}"

#         for scan_details in unique_scans.values():
#             print(scan_details)