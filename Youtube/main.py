import json
import time
import traceback

from utils import cleanup_media_folders, is_uploaded, update_tracker, process_title, send_message
from get_reddit_data import Reddit
from audio_services import generate_audio_and_transcription
from video_service import compile_video
from youtube_utils import upload_video

cleanup_media_folders()

reddit = Reddit()
posts = reddit.get_top_posts(time_filter='day', limit=3)

for post in posts:
    post_id = post['id']
    title = post['title']
    title = process_title(title)
    description = f'Original Post Credits: {post["url"]}'
    tags = ['askreddit', 'reddit', 'shorts']
    try:
        if is_uploaded(post_id):
            continue
        with open(f'Posts/{post["id"]}.json', 'w') as post_file:
            json.dump(post, post_file, indent=4)
        audio_file, srt_file = generate_audio_and_transcription(content=post['content'], post_id=post_id)

        output_video_path = compile_video(f'Audios/{audio_file}', f'Subs/{srt_file}', post_id)
        time.sleep(5)

        response = upload_video(f'Videos/{output_video_path}', title, description, tags)
        update_tracker(post_id, response['id'])
        send_message(f"{post_id} uploaded video: {response['id']}\nTitle: {title}\nOP: {post['url']}")
        time.sleep(2)

    except Exception as e:
        print(f'Unknown Exception for {post_id}')
        traceback.print_exc()

