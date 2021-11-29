import tweepy
import re
from liquid import Template

def authenticate(app_info):
    auth = tweepy.OAuthHandler(app_info["API Key"], app_info["API Key Secret"])
    auth.set_access_token(app_info["Access Token"], app_info["Access Token Secret"])
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
        return api
    except:
        print("Error during authentication")
        return -1

def tweet_parser(format_string, format_dict):
    template = Template(format_string)
    return template.render(**format_dict)

def break_tweet(tweet_str):
    index = [0]
    breaks = [i for i, s in enumerate(tweet_str) if s == " "]
    for b in breaks:
        if b - index[-1] >= 280:
            index.append(last)
            diff = b
        last = b
    return [tweet_str[i:j].lstrip(" ") for i,j in zip(index, index[1:]+[None])]
