import time
import tweepy
import herrbot_secrets


def report_error(api, e):
    """ Report an exception to the owner of this bot

        :param: api: tweepy.API instance
        :param: e: exception instance

    """
    error_msg = e.__class__.__name__ + ": " + str(e)

    api.send_direct_message(
        screen_name = herrbot_secrets.owner,
        text = error_msg[-130:] + ": " + time.strftime("%H:%M:%S"),
    )

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
