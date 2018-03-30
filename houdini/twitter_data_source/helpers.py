import os
import requests
import json 

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', None)


def to_slack(message):

    payload = {
        'channel': '#houdini', 'username': 'houdini-bot',
        'text': 'An urgent message!',
        'attachments': [
            {
                'text': message
            }
        ]
    }

    requests.post(
        SLACK_WEBHOOK_URL,
        data=json.dumps(payload)
    )