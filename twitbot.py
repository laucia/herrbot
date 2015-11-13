import time
from collections import namedtuple
from functools import wraps

import tweepy
import herrbot_secrets


# Authentication
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_api():
    """ login and return an usable api

        :returns: tweepy.API instance
    """
    auth = tweepy.OAuthHandler(
        herrbot_secrets.consumer_key,
        herrbot_secrets.consumer_secret,
    )
    auth.set_access_token(
        herrbot_secrets.herrbot_token,
        herrbot_secrets.herrbot_secret,
    )
    return tweepy.API(auth)


# Error Reporting
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def report_error(api, e):
    """ Report an exception to the owner of this bot

        :param: api: tweepy.API instance
        :param: e: exception instance

    """
    error_msg = e.__class__.__name__ + ": " + str(e)

    try:
        api.send_direct_message(
            screen_name = herrbot_secrets.owner,
            text = error_msg[-130:] + ": " + time.strftime("%H:%M:%S"),
        )
    except Exception as e:
        pass  # we still want to log the original error



def with_report_error(f):
    """ Decorator to automatically report errors via twitter when they happen
    within a function
    """
    @wraps(f)
    def wrapper(api, *args, **kwargs):
        try:
            return f(api ,*args, **kwargs)
        except Exception as e:
            report_error(api, e)
            raise

    return wrapper


# Error Reporting
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

BOT_SCREEN_NAME = "herrbot_DE"
NOT_EN_ERROR_MSG = "Entschuldigung Ich spieke nur Deutsch von Englisch"


RespondableTweet = namedtuple(
    typename='RespondableTweet',
    field_names = ["tweet", "bot_caller"],
)


def _clean_bot_name(text):
    """ Remove the bots own name from the text we send back """
    clean_text = text.replace("@{0}".format(BOT_SCREEN_NAME), "")
    clean_text = clean_text.replace("@{0}".format(BOT_SCREEN_NAME.lower()), "")
    clean_text = clean_text.strip()
    return clean_text


@with_report_error
def list_unresponded_mentions(api):
    """ List all the "unresponded" tweets.
    Unresponded is determined by non-favorited.

        :param: api: tweepy.API instance
    """
    mention_tweets = api.mentions_timeline()
    tweets_to_respond_to = []

    tweets_to_fetch = {}

    # Parse the direct mention tweets
    for tweet in mention_tweets:
        if tweet.in_reply_to_status_id:
            tweets_to_fetch[tweet.in_reply_to_status_id_str] = (
                tweet.user.screen_name
            )
        elif not tweet.favorited:
            tweets_to_respond_to.append(
                RespondableTweet(
                    tweet=tweet,
                    bot_caller=tweet.user.screen_name,
                )
            )

    # fetch the tweets we should respond to
    if tweets_to_fetch:
        fetched_tweets = api.statuses_lookup(tweets_to_fetch.keys())
        for tweet in fetched_tweets:
            if not tweet.favorited:
                tweets_to_respond_to.append(
                    RespondableTweet(
                        tweet=tweet,
                        bot_caller=tweets_to_fetch[str(tweet.id)]
                    )
                )

    return tweets_to_respond_to

@with_report_error
def respond_to_tweet(api, respondable_tweet, transformation_fn, debug=False):
    """ Make the bot respond to a tweet, and favorite it so it is not responded
    again.

        :param: api: tweepy.API instance
        :param: respondable_tweet: RespondableTweet instance
        :param: transformation_fn: string->string function
        :param: debug: boolean: When true the function print instead of hitting
        the twitter API

    """
    # Extract important informations
    id_to_respond_to = respondable_tweet.tweet.id
    original_caller_name = respondable_tweet.bot_caller
    original_text = respondable_tweet.tweet.text
    is_english = respondable_tweet.tweet.lang == "en"

    # Generate status text, depending on tweet language
    if is_english:
        status_text = _clean_bot_name(original_text)
        status_text = transformation_fn(status_text)
    else:
        status_text = NOT_EN_ERROR_MSG

    # Get callers
    if original_caller_name == respondable_tweet.tweet.user.screen_name:
        callers = "@{0} ".format(original_caller_name)
    else:
        callers = "@{0} @{1} ".format(
            original_caller_name,
            respondable_tweet.tweet.user.screen_name,
        )
    status_text = callers + status_text[-(141 - len(callers)):]

    # Send messages
    if debug:
        print(status_text)
        print(id_to_respond_to)
    else:
        api.update_status(
            status=status_text,
            in_reply_to_status_id=id_to_respond_to,
        )
        api.create_favorite(id_to_respond_to)
