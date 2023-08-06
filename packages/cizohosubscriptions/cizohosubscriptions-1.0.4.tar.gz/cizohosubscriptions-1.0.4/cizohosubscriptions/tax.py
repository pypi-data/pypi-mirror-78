import ast

from requests import HTTPError

from client.client import Client

try:
    from django.conf import settings as configuration

except ImportError:
    try:
        import config as configuration
    except ImportError:
        print("Zoho configurations not found in config/django settings, must be passed while initializing")


class Tax:
    def __init__(self, config=None):
        if config is None:
            self.client = Client(configuration.ZOHO_SUBSCRIPTION_CONFIG)
        else:
            self.client = Client(config)

    def list_taxes(self):
        list_of_taxes_uri = 'settings/taxes'
        result = self.client.send_request('GET', list_of_taxes_uri)
        response = result['taxes']

        return response