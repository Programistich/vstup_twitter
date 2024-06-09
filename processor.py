import asyncio
import time
import sqlite3

from tweety.types import Tweet

import telegram
from twitter import get_tweet_by_search

connector = sqlite3.connect("storage.db")
prompt = "(нмт AND вступ) OR нмт OR наукма OR могилянка OR кма OR NAUKMA"


async def process_loop_search():
    print("Start searching")
    while True:
        print("Searching...")
        await process_search()
        time.sleep(60 * 10)  # 10 minutes


async def process_search():
    tweets = get_tweet_by_search(prompt)
    for tweet in tweets:
        if not is_tweet_exist(tweet):
            await process_tweet(tweet)
        else:
            print("Tweet already exist")


async def process_tweet(tweet: Tweet):
    print("Tweet:", tweet)
    try:
        await telegram.send_tweet(tweet)
        save_tweet(tweet)
    except Exception as e:
        print("Error:", e)
    await asyncio.sleep(10)  # 5 seconds
    print("----------------")


def init_db():
    print("Init database")
    cursor = connector.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id TEXT
        )
        """
    )


def save_tweet(tweet: Tweet):
    print("Save tweet in db")
    cursor = connector.cursor()
    cursor.execute("""
        INSERT INTO tweets (tweet_id) VALUES (?)
        """, (tweet.id,))
    connector.commit()


def is_tweet_exist(tweet: Tweet) -> bool:
    cursor = connector.cursor()
    cursor.execute("""
        SELECT * FROM tweets WHERE tweet_id = ?
        """, (tweet.id,))
    return cursor.fetchone() is not None
