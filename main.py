from twitbot import (
    get_api,
    list_unresponded_mentions,
    respond_to_tweet,
)
from germanizator import english_to_deutsch
from herrbot_secrets import debug

api = get_api()
for tweet in list_unresponded_mentions(api):
    respond_to_tweet(api, tweet, english_to_deutsch, debug=debug)
