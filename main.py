from twitbot import (
    get_api,
    list_unresponded_mentions,
    respond_to_tweet,
)


api = get_api()
for tweet in list_unresponded_mentions(api):
    respond_to_tweet(api, tweet, lambda _: "I'm responding for the first and last time", debug=True)
