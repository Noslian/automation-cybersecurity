from tenable.io import TenableIO
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta

load_dotenv()

keys_env = os.getenv("KEYS")

if keys_env:
    api_keys = json.loads(keys_env)

    for client, keys in api_keys.items():
        print("\n")
        print(f"Client: {client}")

        access_key = keys['accessKey']
        secret_key = keys['secretKey']

        tio = TenableIO(access_key=access_key, secret_key=secret_key)

        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        vulnerabilities = tio.workbenches.vulns()

        found_vulnerabilities = False

        for vuln in vulnerabilities:
            plugin_id = vuln['plugin_id']
            vuln_info = tio.workbenches.vuln_info(plugin_id)

            state = vuln_info.get('state')
            if state != 'FIXED':
                plugin_details = vuln_info.get('plugin_details', {})
                publication_date = plugin_details.get('publication_date')
                name = plugin_details.get('name')
                severity = plugin_details.get('severity')
                state = plugin_details.get('state')
                vpr_info = vuln_info.get('vpr', {})  
                vpr_score = vpr_info.get('score')

                if publication_date >= seven_days_ago and vpr_score and float(vpr_score) > 8:
                    found_vulnerabilities = True
                    print(f'   Plugin ID: {plugin_id}: {name}, VPR Score: {vpr_score}, Publicada: {publication_date}')
        if not found_vulnerabilities:
            print(f"   Não há novas vulnerabilidades com o VPR > 8 para ({client}) nos últimos 7 dias.")       
