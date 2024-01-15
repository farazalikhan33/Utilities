import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


youtube = build("youtube", "v3", credentials=authenticate())


def upload_video(video_file, title, description, tags):
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27",  # Category ID for Shorts
        },
        "status": {"privacyStatus": "public"},
    }

    media_file = MediaFileUpload(video_file, resumable=True)
    response = youtube.videos().insert(
        part=",".join(request_body.keys()),
        body=request_body,
        media_body=media_file,
    ).execute()
    return response


def comment_on_video(youtube, video_id, comment_text):
    print(f'Commenting on video: {video_id}')
    request_body = {
        "snippet": {
            "videoId": video_id,
            "textOriginal": comment_text,
        },
    }

    youtube.commentThreads().insert(
        part="snippet",
        body=request_body,
    ).execute()


def main():
    video_file_path = "Videos/195sutc_words_output_video.mp4"
    video_title = "Your Shorts Video Title"
    video_description = "Your video description goes here."
    video_tags = ["tag1", "tag2", "tag3"]
    channel_id = 'UCgmVULqCEaV89NJG4GDrbOQ'
    response = upload_video(youtube, video_file_path, video_title, video_description, video_tags)
    comment_text = "This is actually a great video!"
    if response:
        video_id = response["id"]
        print(video_id)
        # comment_on_video(youtube, video_id, comment_text)
    print(response)


if __name__ == "__main__":
    main()
