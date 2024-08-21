import requests

api_endpoint = "https://{url}.goskope.com/api/v1/security_assessment"

api_token = ""

params = {
    "token": api_token,
    "platform": "aws",
    "status": "Failed",  # This filters for 'Failed' findings directly in the API call
    "limit": 100
}

response = requests.get(api_endpoint, params=params)

if response.status_code == 200:
    data = response.json()

    if data.get("status") == "success":
        findings = data.get("data", [])

        print(f"Number of failed findings: {len(findings)}")

        for finding in findings:
            print(f"Status: {finding['status']}")
            print(f"Account Name: {finding['account_name']}")
            print(f"Severity: {finding['severity']}")
            print(f"Resource Type: {finding['resource_type']}")
            print(f"Cloud Provider: {finding['cloud_provider']}")
            print("-" * 40) 
    else:
        print("The API call was not successful: ", data.get("msg"))
else:
    print("Failed to retrieve data: HTTP Status Code ", response.status_code)

