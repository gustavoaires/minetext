import twitter
from twitterscraper import query_tweets
import json
import datetime

class TwitterAccess(object):

    def connect(self, consumer_key, consumer_secret,
                oauth_token, oauth_token_secret):
        """
        :param consumer_key: 
        :param consumer_secret: 
        :param oauth_token: 
        :param oauth_token_secret: 
        :return: object to access the twitter api
        all the request can be done using this object
        """

        auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                   consumer_key, consumer_secret)
        return twitter.Twitter(auth=auth)

    def getTweetsByDate(self, query, initial_date, final_date):
        """
        :param query: should contain all the words and can includ logic operators
        ex: trump OR hillary
        :param initial_date and final_date must be in the following format
        ex: YYYY-mm-dd
        :return: created_at value is based on the following format
        ex: YYYY-mm-dd HH:mm:ss
        """
        final_query = query + " since:" + initial_date + " until:" + final_date

        tweets = []

        for tweet in query_tweets(final_query, 10)[:10]:
            dict = {}
            dict['id'] = tweet.id.encode('utf-8')
            dict['text'] = tweet.text
            dict['screen_name'] = tweet.user.encode('utf-8')
            dict['created_at'] = str(tweet.timestamp)
            tweets.append(dict)

        return tweets
