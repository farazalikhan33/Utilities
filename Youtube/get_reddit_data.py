import praw

from creds import reddit_secret
from audio_services import stitch_audio


class Reddit:
    def __init__(self):
        self.reddit_instance = praw.Reddit(
            client_id="VrAvv87K8TJ4qU5o3pYatA",
            client_secret=reddit_secret,
            user_agent='Sampeledatabot using RedditBot',
        )

    def get_top_posts(self, sub='AITAH', time_filter='day', limit=1):
        subreddit = self.reddit_instance.subreddit(sub)
        top_posts = subreddit.top(time_filter=time_filter, limit=limit)
        posts = list()

        for post in top_posts:
            data = dict()
            data['id'] = post.id
            data['title'] = post.title
            data['content'] = post.selftext
            data['url'] = post.url
            data['upvotes'] = post.score
            posts.append(data)

        for i in posts:
            print(i['id'], i['title'])
        return posts


