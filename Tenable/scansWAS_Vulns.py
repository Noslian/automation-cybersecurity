from tenable.io import TenableIO
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json

load_dotenv()
keys_env = os.getenv("KEYS")

if keys_env:
    api_keys = json.loads(keys_env)
    seven_days_ago = datetime.today() - timedelta(days=30)
    seven_days_ago_formatted = seven_days_ago.strftime('%Y/%m/%d')

    for client, keys in api_keys.items():
        print(f"\nClient: {client}")

        scans_found = False
        tio = TenableIO(keys['accessKey'], keys['secretKey'])
        processed_scans = set()  

        for status in ['aborted', 'completed']:
            was_iterator = tio.was.export(
                and_filter=[
                    ("scans_started_at", "gte", seven_days_ago_formatted),
                    ("scans_status", "eq", status)
                ]
            )

            for finding in was_iterator:
                scan_id = finding['scan']['scan_id']
                scan_name = finding.get('config', {}).get('name', 'Nome do Scan não disponível')
                scan_status = finding.get('scan', {}).get('status', 'Status do Scan não disponível')

                # Imprime informações do scan independentemente das vulnerabilidades
                if scan_id not in processed_scans:
                    print(f"Nome do Scan: {scan_name}, Status: {scan_status}")
                    processed_scans.add(scan_id)
                    scans_found = True;               
                
                # Verifica se a vulnerabilidade possui um fator de risco relevante antes de imprimir
                finding_name = finding.get('finding', {}).get('name', 'Nome não disponível')
                risk_factor = finding.get('finding', {}).get('risk_factor', 'Severidade não disponível')
                relevant_risks_count = 0
                
                if risk_factor in ['high', 'critical']:
                    print(f"   Vulnerabilidade: {finding_name}, Fator de risco: {risk_factor}")

        if not scans_found:
            print(f"   Nenhuma varredura (WAS) encontrada para o cliente {client} nos últimos 7 dias.")

else:
    print("API keys not found.")

                