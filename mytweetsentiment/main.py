from collecting import datacollect


# test file

def main():
    CONSUMER_KEY = '4jtRRPl3WvYyzPvRnNKRaaLGr'
    CONSUMER_SECRET = 'dFr8l0HDQ2RA3sQhiTjkMvJs9ML38BLkEoofDNr50tBEOCmZNA'
    OAUTH_TOKEN = '98992106-OsffZtvTWPxeHCkA5G9golyjU4inlvb7XB6g0oDva'
    OAUTH_TOKEN_SECRET = 'eD0RE8AyfTDmyYnOKfWLo3XvjILKktRJOIoQnlmHCmbip'

    twitter_api = datacollect.TwitterAccess().connect(CONSUMER_KEY, CONSUMER_SECRET,
                                                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    print twitter_api

    query = "previdencia OR reforma da presidencia OR reforma da previdencia"
    initial_date = "2017-03-15"
    final_date = "2017-03-22"
    tweets = datacollect.TwitterAccess().getTweetsByDate(query, initial_date, final_date)

    for tweet in tweets:
        print tweet

    # final_query = query + " since:" + initial_date + " until:" + final_date
    #
    # for tweet in query_tweets(final_query, 10)[:10]:
    #     print tweet.text.encode('utf-8')
main()