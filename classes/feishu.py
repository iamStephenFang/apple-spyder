import logging

import requests
import yaml
import json


def _get_feishu_config():
    with open("res/config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            print(config)
        except yaml.YAMLError as exc:
            print(exc)
    return config['feishu']


class Feishu:
    def __init__(self):
        config = _get_feishu_config()
        self.enable = config['enable']
        self.webhook_url = config['webhook-url']

    def send_message(self, message):
        if not self.enable:
            logging.warning("Feishu posting feature is DISABLED.")
            return

        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        response = requests.post(self.webhook_url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            logging.error(f"Request to Feishu returned an error {response.status_code}, the response is: {response.text}")