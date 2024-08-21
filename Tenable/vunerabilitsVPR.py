from tenable.io import TenableIO
from dotenv import load_dotenv
import os
import json

load_dotenv()

keys_env = os.getenv("KEYS")

if keys_env:
    api_keys = json.loads(keys_env)

    severity_mapping = {4: "Critical", 3: "High", 2: "Medium", 1: "Low", 0: "Info"}

    for client, keys in api_keys.items():
        print(f"Cliente: {client}")

        access_key = keys['accessKey']
        secret_key = keys['secretKey']

        tio = TenableIO(access_key=access_key, secret_key=secret_key)

        try:
            vulnerabilities = tio.workbenches.vulns()
        except Exception as e:
            print(f"Failed to retrieve vulnerabilities for client {client}: {e}")
            continue

        critical_vulnerabilities = [
            vuln for vuln in vulnerabilities
            if vuln.get("severity", 0) == 4 and vuln.get('vpr_score', 0) >= 10
        ]

        high_vulnerabilities = [
            vuln for vuln in vulnerabilities
            if vuln.get("severity", 0) == 3 and vuln.get('vpr_score', 0) >= 10
        ]

        # Concatenar as listas de vulnerabilidades críticas e altas
        filtered_vulnerabilities = critical_vulnerabilities + high_vulnerabilities

        if not filtered_vulnerabilities:
            print("Não há vulnerabilidades críticas e altas com VPR igual a 10.")
        else:
            # Ordenar as vulnerabilidades filtradas por severidade e contagem
            sorted_vulnerabilities = sorted(
                filtered_vulnerabilities,
                key=lambda x: (x.get("severity", 0), x.get("count", 0)),
                reverse=True
            )

            for idx, vulnerability in enumerate(sorted_vulnerabilities[:10], 1):
                severity_text = severity_mapping.get(vulnerability.get("severity"), "Unknown")
                print(f"{idx}. Plugin ID: {vulnerability.get('plugin_id', 'N/A')}")
                print(f"   Plugin Name: {vulnerability.get('plugin_name', 'N/A')}")
                print(f"   Vulnerability State: {vulnerability.get('vulnerability_state', 'N/A')}")
                print(f"   Severity: {severity_text}")
                print(f"   VPR Score: {vulnerability.get('vpr_score', 'N/A')}")
                print(f"   Count: {vulnerability.get('count', 'N/A')}")
            print("\n")
else:
    print("API keys not found.")
