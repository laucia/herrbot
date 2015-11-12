from twitbot import (
    get_api,
    list_unresponded_mentions,
    respond_to_tweet,
)
from en2de import end2de


api = get_api()
for tweet in list_unresponded_mentions(api):
    respond_to_tweet(api, tweet, end2de, debug=True)
