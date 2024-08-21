import requests
import logging
import json

class InvestigationAPI:
    
    def __init__(self, client_id, client_secret, base_url):
        self.iam_url = 'iam.mcafee-cloud.com/iam/v1.1'
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = True
        self.auth(client_id, client_secret)

    def auth(self, client_id, client_secret):
        payload = {
            'scope': 'soc.hts.c soc.hts.r soc.rts.c soc.rts.r soc.qry.pr',
            'grant_type': 'client_credentials',
            'audience': 'mcafee'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        res = self.session.post(f'https://{self.iam_url}/token', headers=headers, data=payload, auth=(client_id, client_secret))
        if res.ok:
            self.session.headers['Authorization'] = f'Bearer {res.json()["access_token"]}'
            self.session.headers['Content-Type'] = 'application/vnd.api+json'
            logging.debug('Successfully authenticated.')
        else:
            logging.error('Authentication failed: {}'.format(res.text))
            raise Exception('Authentication failed')

    def get_investigations(self, offset=0, limit=10, sort='created'):
        url = f'https://{self.base_url}/edr/v2/investigations'
        params = {
            'page[offset]': offset,
            'page[limit]': limit,
            'sort': sort
        }
        response = self.session.get(url, params=params)
        if response.ok:
            return response.json()
        else:
            logging.error(f"Failed to retrieve investigations: {response.text}")
            response.raise_for_status()

def load_client_data():
    """Load client data from a JSON file."""
    with open('clients.json', 'r') as file:
        return json.load(file)

def main():
    clients = load_client_data()
    for client in clients:
        try:
            api = InvestigationAPI(client['EDR_CLIENT_ID'], client['EDR_CLIENT_SECRET'], client['BASE_URL'])
            investigations = api.get_investigations()
            print(f"Investigations Data for {client['EDR_CLIENT_NAME']}:", investigations)
        except Exception as e:
            logging.error(f"Failed to process client {client['EDR_CLIENT_NAME']}: {e}")

if __name__ == "__main__":
    main()
