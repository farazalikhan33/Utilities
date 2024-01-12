import re

import requests

from creds import bot_token, channel_id, test_channel_id


def escape_all_special_chars(text):
    special_chars = r'[_*[\]()~`>#+-=|{}.!]'
    escaped_text = re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)
    return escaped_text


def send_message(message, alert_test_channel=None):
    message = escape_all_special_chars(message)
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    if alert_test_channel:
        payload = {
            'chat_id': test_channel_id,
            'text': message,
            'parse_mode': 'MarkdownV2'
        }
    else:
        payload = {
            'chat_id': channel_id,
            'text': message,
            'parse_mode': 'MARKDOWNV2'
        }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message. Status code:", response.status_code)
        print(response.content)
