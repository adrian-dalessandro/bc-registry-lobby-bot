from src.scrape_registry import *
from src.twitter import *
import json
import os

results = poll_registry()
format_string = open("tweet.format.txt").read()
filters = json.load(open("filters.json"))
app_info = json.load(open("app.info.json"))

# check for most recent stashed results
if os.path.isfile(".last_checked.json"):
    last_checked = json.load(open(".last_checked.json"))
    try:
        last_index = results.index(last_checked)
        results = results[0:last_index]
    except:
        pass
if len(results) > 0:
    json.dump(results[0], open(".last_checked.json", "w"))

    api = authenticate(app_info)
    for info in results:
        tweet_str = tweet_parser(format_string, info)
        if any([True for f in filters if f.lower() in info["organization"].lower()]):
            tweets = break_tweet(tweet_str)
            tweet_id = api.update_status(tweets[0]).id_str

            if len(tweets) > 1:
                for tweet in tweets[1:]:
                    tweet_id = api.update_status(tweet, in_reply_to_status_id = tweet_id,
                                                 auto_populate_reply_metadata = True).id_str


