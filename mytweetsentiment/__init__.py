from collecting.DataCollect import APICollect
from textprocessor import PortugueseProcess as pln

# test file

def main():
    CONSUMER_KEY = '4jtRRPl3WvYyzPvRnNKRaaLGr'
    CONSUMER_SECRET = 'dFr8l0HDQ2RA3sQhiTjkMvJs9ML38BLkEoofDNr50tBEOCmZNA'
    OAUTH_TOKEN = '98992106-OsffZtvTWPxeHCkA5G9golyjU4inlvb7XB6g0oDva'
    OAUTH_TOKEN_SECRET = 'eD0RE8AyfTDmyYnOKfWLo3XvjILKktRJOIoQnlmHCmbip'

    query = "previdencia OR reforma da presidencia OR reforma da previdencia since:2017-05-23 until:2017-05-24"
    # scrape = datacollect.ScrapeCollect()
    # tweets = scrape.scrape_tweets(query, 20)

    api = APICollect(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    tweets = api.rest_tweets(query=query, limit=5)

    cleaner = pln.TextCleaner()
    named = pln.NamedEntity()

    for tweet in tweets:
        d = tweet['text']
        text = d.lower()
        d = named.removeTwitterUsername(text)
        text = cleaner.removeSymbols(d)
        d = cleaner.removeStopwords(text)
        text = cleaner.removeAccent(d)
        d = cleaner.removeLinks(text)
        text = cleaner.removeSufPort(d)
        print text

main()
