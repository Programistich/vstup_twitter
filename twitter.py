import os

from tweety import Twitter, filters
from tweety.types import SelfThread

twitter_username = os.getenv("TWITTER_USERNAME")
twitter_password = os.getenv("TWITTER_PASSWORD")
twitter_cookies = os.getenv("TWITTER_COOKIES")

twitter = Twitter("session")


def login():
    try:
        twitter.sign_in(twitter_username, twitter_password)
        print("Logged in successfully")
    except Exception as e:
        print("Error occurred while signing in: %s", e)
        cookies_value = os.getenv("TWITTER_COOKIES")
        try:
            twitter.load_cookies(cookies_value)
            print("Logged in successfully")
        except Exception as e:
            print("Error occurred while loading cookies: %s", e)


def get_tweet_by_search(keyword: str):
    tweets = []
    for search in twitter.iter_search(keyword=keyword, pages=1, filter_="Latest"):
        for tweet in search[1]:
            if isinstance(tweet, SelfThread):
                tweets.extend(tweet.tweets)
            else:
                tweets.append(tweet)
    tweets.reverse()
    return tweets

