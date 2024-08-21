import requests
import logging
from datetime import datetime, timedelta
import json

class EDR():
    
    def __init__(self, client_id, client_secret, base_url):
        self.iam_url = 'iam.mcafee-cloud.com/iam/v1.1'
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = True

        self.auth(client_id, client_secret)
        self.limit = 10000

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


    def get_threats(self, client_name):
        next_pull = datetime.now() - timedelta(days=7)
        epoch_pull = str(int(datetime.timestamp(next_pull) * 1000))

        skip = 0
        severity_counts = {"Low": 0, "Medium": 0, "High": 0}

        while True:
            filter = {'severities': ["s1", "s2", "s3", "s4", "s5"]}
            res = self.session.get(f'https://api.{self.base_url}/ft/api/v2/ft/threats?sort=-lastDetected&filter={json.dumps(filter)}&from={epoch_pull}&limit={self.limit}&skip={skip}')
            if res.ok:
                data = res.json()
                if 'threats' in data and data['threats']:
                    for threat in data['threats']:
                        severity = threat['severity']
                        if severity == 's1':
                            severity_counts['Low'] += 1
                        elif severity == 's2':
                            severity_counts['Medium'] += 1
                        elif severity in ['s3', 's4', 's5']:
                            severity_counts['High'] += 1
                else:
                    print("No more threats found.")
                if int(data['skipped']) + int(data['items']) >= int(data['total']):
                    break
                else:
                    skip += int(data['items'])
            else:
                logging.error('Failed to retrieve threats: {}'.format(res.text))
                break
        
        print(f"Cliente: {client_name}, Alertas HIGH, Medium e LOW não tratados dos últimos 7 dias.")
        for label, count in severity_counts.items():
            print(f" {label}: {count}")

def load_client_data():
    with open('clients.json', 'r') as file:
        return json.load(file)

def main():
    clients = load_client_data()
    for client in clients:
        edr = EDR(client['EDR_CLIENT_ID'], client['EDR_CLIENT_SECRET'], client['BASE_URL'])
        edr.get_threats(client['EDR_CLIENT_NAME'])

if __name__ == "__main__":
    main()
