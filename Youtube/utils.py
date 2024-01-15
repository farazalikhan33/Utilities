import json
import os
import shutil
import traceback
import re
import requests

from creds import bot_token, yt_channel_id

tracker_json_path = 'tracker.json'


def cleanup_media_folders():
    media_folders = ['Subs', 'Audios', 'Videos']
    for folder in media_folders:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"Folder '{folder}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting folder '{folder}': {e}")
        try:
            os.makedirs(folder)
            print(f"Folder '{folder}' created successfully.")
        except Exception as e:
            print(f"Error creating folder '{folder}': {e}")


def process_title(post_title):
    try:
        lst = post_title.split(' ')
        if len(lst) > 5:
            lst = lst[:5]
            formatted_title = ' '.join([word for word in lst])
            return formatted_title
        return post_title
    except Exception as e:
        print(f'Unknown exception processing title: {e}')
        return "AITA?"
        traceback.print_exc()

def is_uploaded(post_id):
    try:
        with open(tracker_json_path, 'r') as tracker_json:
            data = json.loads(tracker_json.read())
            if post_id in data:
                print(f'"{post_id}" is already in Tracker data!')
                return True
            return False
    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f'Error updating tracker for {post_id}: {e}')
        traceback.print_exc()


def update_tracker(post_id=None, video_id=None):
    try:
        data = None
        with open(tracker_json_path, 'r') as tracker_json:
            data = json.loads(tracker_json.read())

        with open(tracker_json_path, 'w') as tracker_json:
            data[post_id] = video_id
            json.dump(data, tracker_json, indent=4)
    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f'Error updating tracker for {post_id}: {e}')
        traceback.print_exc()


def escape_all_special_chars(text):
    special_chars = r'[_*[\]()~`>#+-=|{}.!]'
    escaped_text = re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)
    return escaped_text


def send_message(message):
    message = escape_all_special_chars(message)
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': yt_channel_id,
        'text': message,
        'parse_mode': 'MarkdownV2'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message. Status code:", response.status_code)
        print(response.content)
