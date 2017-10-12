import tweepy as tw
from tweepy.streaming import StreamListener
from tweepy import Stream
from twitterscraper import query_tweets


class APICollect(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.api = self.connect(consumer_key, consumer_secret, access_token, access_token_secret)

    def connect(self, consumer_key, consumer_secret,
                access_token, access_token_secret):
        """
        :param consumer_key: 
        :param consumer_secret: 
        :param oauth_token: 
        :param oauth_token_secret: 
        :return: object to access the twitter api
        all the request can be done by using this object
        """
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.access_token = access_token
        auth.access_token_secret = access_token_secret

        return tw.API(auth, wait_on_rate_limit=True)

    def rest_tweets(self, query, lang="pt", limit=None):
        """
        returns all the tweets within 7 days top according to the query received by this method
        returns the complete tweet
        :param query: should contain all the words and can include logic operators
        should also provide the period of time for the search
        ex: rock OR axe 
        (visit https://dev.twitter.com/rest/public/search to see how to create a query)
        :param lang: the language of the tweets
        :param limit: defines the maximum amount of tweets to fetch
        :return: tweets: a list of all tweets obtained after the request
        """
        tweets = []

        for tweet in tw.Cursor(self.api.search, q=query, lang=lang).items(limit):
            tweets.append(tweet._json)

        return tweets

    def stream_tweets(self, follow=None, track=None, async=False, locations=None,
               stall_warnings=False, languages=None, encoding="utf8", filter_level=None):
        l = StdOutListener()
        stream = Stream(self.api.auth, l)
        stream.filter(follow, track, async, locations, stall_warnings, languages, encoding, filter_level)


class StdOutListener(StreamListener):
    """ 
    A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


class ScrapeCollect(object):
    def scrape_tweets(self, query, limit=None):
        """
        all the results obtained with this method 
        has just id, user, text and timestamp metadata

        :param query: should contain all the words and can include logic operators
        should also provide the period of time for the search
        ex: rock OR axe
        (visit https://dev.twitter.com/rest/public/search to see how to create a query)
        :param limit: defines the maximum amount of tweets to fetch
        :return: tweets: a list of all tweets obtained after the request
        """
        tweets = []

        for tweet in query_tweets(query, limit=limit):
            new_tweet = {}
            new_tweet["id"] = tweet.id
            new_tweet["text"] = tweet.text
            new_tweet["screen_name"] = tweet.user
            new_tweet["created_at"] = str(tweet.timestamp)
            tweets.append(new_tweet)

        return tweets
