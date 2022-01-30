import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from purdue_brain.wrappers.discord_wrapper import DiscordWrapper

load_dotenv()
endpoint_url = "http://api.nessieisreal.com"
api_key = os.getenv('CAPITAL_ONE_API_KEY')


def process_request(url, payload):
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers={'content-type': 'application/json', "Accept": "application/json"}
    )
    return response is not None and response.status_code == 201, response


def process_get(url):
    response = requests.get(
        url=url
    )
    return response is not None and response.status_code == 200, response


def create_content(response):
    if response.status_code in [200, 201, 202]:
        my_json = response.content.decode('utf8')
        return json.loads(my_json)
    return None


def get_merchants():
    url = endpoint_url + f"/merchants?lat={40.42353}&lng={-86.921738}&rad={50}&key={api_key}"
    is_valid, response = process_get(url)
    content = create_content(response)
    return content if is_valid else None


def get_purchase_details(purchase_id):
    url = endpoint_url + f"/purchases/{purchase_id}?key={api_key}"
    is_valid, response = process_get(url)
    content = create_content(response)
    return content if is_valid else None


def get_merchant_details(merchant_id):
    url = endpoint_url + f"/merchants/{merchant_id}?key={api_key}"
    is_valid, response = process_get(url)
    content = create_content(response)
    return content if is_valid else None


def get_robinhood_merchant():
    config = DiscordWrapper.fire.get_discord_config()
    if 'robinhood_merchant_id' in config:
        return config['robinhood_merchant_id']

    url = endpoint_url + f"/merchants?key={api_key}"
    payload = {
        "name": "Robinhood",
        "address": {
            "street_number": "84",
            "street_name": "Willow Road",
            "city": "Menlo Park",
            "state": "CA",
            "zip": "94025"
        },
        "geocode": {
            "lat": 37.452961,
            "lng": -122.181725
        }
    }
    is_valid, response = process_request(url, payload)
    content = create_content(response)
    if is_valid:
        robinhood_id = content['objectCreated']['_id']
        DiscordWrapper.fire.set_discord_config({'robinhood_merchant_id': robinhood_id})
        return robinhood_id
    return None


class Nessie:

    def __init__(self, customer_id, account_id):
        self.customer_id = customer_id
        self.account_id = account_id

    @staticmethod
    def get_nessile_from_user_id(author_id):
        account_information = DiscordWrapper.fire.get_property('nessie_customer_id', author_id)
        if account_information:
            account_id, customer_id = account_information['account_id'], account_information['customer_id']
            return Nessie(customer_id, account_id)
        return None

    def get_customer_data(self):
        url = endpoint_url + f"/accounts/{self.account_id}?key={api_key}"
        is_valid, response = process_get(url)
        content = create_content(response)
        return content if is_valid else None

    def get_purchases(self):
        url = endpoint_url + f"/accounts/{self.account_id}/purchases?key={api_key}"
        is_valid, response = process_get(url)
        content = create_content(response)
        return content if is_valid else None

    def create_customer(self):
        url = endpoint_url + f"/customers?key={api_key}"
        payload = {
            "first_name": "Purdue",
            "last_name": "Pete",
            "address": {
                "street_number": "610",
                "street_name": "Purdue Mall",
                "city": "West Lafayette",
                "state": "IN",
                "zip": "47907"
            }
        }
        is_valid, response = process_request(url, payload)
        content = create_content(response)
        self.customer_id = content['objectCreated']['_id'] if is_valid else None
        return self.customer_id is not None

    def perform_purchase(self, amount, merchant_id=None, description='no description'):
        if merchant_id is None:
            merchant_id = get_robinhood_merchant()
            if description == 'no description':
                description = 'Bought Stock on Robinhood'

        url = endpoint_url + f"/accounts/{self.account_id}/purchases?key={api_key}"
        now = datetime.now()
        payload = {
            "merchant_id": merchant_id,
            "medium": "balance",
            "purchase_date": f'{now.strftime("%Y-%m-%d")}',
            "amount": amount,
            "status": "completed",
            "description": description
        }
        is_valid, response = process_request(url, payload)
        content = create_content(response)
        return content if is_valid else None

    def add_money_to_account(self, amount, description='no description'):
        url = endpoint_url + f'/accounts/{self.account_id}/deposits?key={api_key}'
        now = datetime.now()
        payload = {
            "medium": "balance",
            "transaction_date": f'{now.strftime("%Y-%m-%d")}',
            "status": "completed",
            'amount': amount,
            "description": description
        }
        is_valid, response = process_request(url, payload)
        content = create_content(response)
        return content if is_valid else None

    def create_account(self):
        if self.customer_id is not None:
            url = endpoint_url + f"/customers/{self.customer_id}/accounts?key={api_key}"
            payload = {
                'type': 'Checking',
                'nickname': 'FinDiscord',
                'rewards': 10000,
                'balance': 10000,
            }
            is_valid, response = process_request(url, payload)
            content = create_content(response)
            self.account_id = content['objectCreated']['_id'] if is_valid else None
            return is_valid
        return False
