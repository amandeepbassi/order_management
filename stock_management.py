import requests
from model import quantity_available_uri
import json as dict_json


class StockManagement:
    def __init__(self, product_id):
        self.product_id = product_id

    def availablility(self):
        payload = {"product_id": self.product_id}
        r = requests.get(quantity_available_uri, data=dict_json.dumps(payload))
        return r.json()['quantity']

