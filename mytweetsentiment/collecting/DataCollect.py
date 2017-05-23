import tweepy as tw
from twitterscraper import query_tweets

class DataCollect(object):
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
        all the request can be done using this object
        """
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.access_token = access_token
        auth.access_token_secret = access_token_secret

        return tw.API(auth, wait_on_rate_limit=True)

    def getTweetsByScraping(self, query, limit=None):
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
        if query:
            for tweet in query_tweets(query, limit=limit):
                dict = {}
                dict['id'] = tweet.id
                dict['text'] = tweet.text
                dict['screen_name'] = tweet.user
                dict['created_at'] = str(tweet.timestamp)
                tweets.append(dict)

        return tweets

    def getTweetsFromREST(self, query, lang="pt", limit=None):
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