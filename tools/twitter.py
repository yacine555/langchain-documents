import os
from datetime import datetime, timezone
import logging
import tweepy
import json
from pathlib import Path
from pprint import pprint


logger = logging.getLogger("twitter")

# use Twittter API v2
twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
)


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """

    data = []
    try:
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
        )
        data = tweets.data
    except:
        file_path = "tools/tweets_data.json"
        data = json.loads(Path(file_path).read_text())
        # pprint(data)

    tweet_list = []
    for tweet in data:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweetid = tweet["id"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweetid}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    print(scrape_user_tweets(username="@ybouakkaz"))
