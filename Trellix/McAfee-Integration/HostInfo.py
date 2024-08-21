import requests
import json
import logging

class EDR():
    
    def __init__(self, client_id, client_secret, base_url):
        self.iam_url = 'iam.mcafee-cloud.com/iam/v1.1'
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = True
        self.auth(client_id, client_secret)
        self.limit = 10000  # Ajustável conforme necessário

    def auth(self, client_id, client_secret):
        payload = {
            'scope': 'soc.hts.c soc.hts.r soc.rts.c soc.rts.r soc.qry.pr',
            'grant_type': 'client_credentials',
            'audience': 'mcafee'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = self.session.post(f'https://{self.iam_url}/token', headers=headers, data=payload, auth=(client_id, client_secret))
        if res.ok:
            self.session.headers['Authorization'] = f'Bearer {res.json()["access_token"]}'
            logging.debug('Successfully authenticated.')
        else:
            logging.error('Authentication failed: {}'.format(res.text))
            raise Exception('Authentication failed')

    def list_hostnames(self):
        url = f'https://{self.base_url}/active-response/api/v1/searches'
        payload = {
            "projections": [
                {"name": "HostInfo", "outputs": ["hostname", "ip_address", "os", "connection_status", "platform"]}
            ],
            "limit": self.limit
        }
        response = self.session.post(url, json=payload)
        if response.ok:
            query_id = response.json()['id']
            logging.info("Query started successfully, ID: {}".format(query_id))
            return query_id
        else:
            logging.error("Failed to start query: {}".format(response.text))
            return None

    def fetch_results(self, query_id):
        url = f'https://{self.base_url}/active-response/api/v1/searches/{query_id}/results'
        response = self.session.get(url)
        if response.ok:
            results = response.json().get('items', [])
            for item in results:
                hostname_info = item['output'].get('HostInfo|hostname', 'N/A')
                ip_address = item['output'].get('HostInfo|ip_address', 'N/A')
                os = item['output'].get('HostInfo|os', 'N/A')
                connection_status = item['output'].get('HostInfo|connection_status', 'N/A')
                platform = item['output'].get('HostInfo|platform', 'N/A')
                print(f"Hostname: {hostname_info}, IP Address: {ip_address}, OS: {os}, Connection Status: {connection_status}, Platform: {platform}")
        else:
            logging.error("Failed to retrieve results: {}".format(response.text))

def load_client_data():
    with open('clients.json', 'r') as file:
        return json.load(file)

def main():
    logging.basicConfig(level=logging.INFO)
    clients = load_client_data()
    for client in clients:
        edr = EDR(client['EDR_CLIENT_ID'], client['EDR_CLIENT_SECRET'], client['BASE_URL'])
        query_id = edr.list_hostnames()
        if query_id:
            edr.fetch_results(query_id)

if __name__ == "__main__":
    main()