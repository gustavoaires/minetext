# -*- coding: latin-1 -*-
from collecting.datacollect import APICollect
from textprocessor.portugueseprocessor import TextCleaner, NamedEntity
from filemanagement.filemanagement import JSONFileManagement, CSVTSVFileManagement


def main():
    # CONSUMER_KEY = '4jtRRPl3WvYyzPvRnNKRaaLGr'
    # CONSUMER_SECRET = 'dFr8l0HDQ2RA3sQhiTjkMvJs9ML38BLkEoofDNr50tBEOCmZNA'
    # OAUTH_TOKEN = '98992106-OsffZtvTWPxeHCkA5G9golyjU4inlvb7XB6g0oDva'
    # OAUTH_TOKEN_SECRET = 'eD0RE8AyfTDmyYnOKfWLo3XvjILKktRJOIoQnlmHCmbip'

    input_file = 'dataset_until_22_05_pln.json'
    output_file = 'dataset_until_22_05_pln.csv'

    # query = "previdencia social OR reforma da previdencia OR reforma da presidencia ' \
    #         'OR previdencia since:2017-05-23 until:2017-05-24"
    # scrape = datacollect.ScrapeCollect()
    # tweets = scrape.scrape_tweets(query, 20)

    # api = APICollect(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    # tweets = api.rest_tweets(query=query, limit=5)
    #
    # for tweet in tweets:
    #     json.dump(tweet, output_file)
    #     output_file.write("\n")

    # cleaner = TextCleaner()
    # named = NamedEntity()
    # json_management = JSONFileManagement()
    csv_management = CSVTSVFileManagement()

    print 'reading1'
    tweets = csv_management.read_file(output_file)
    print len(tweets)
    # tweets = json_management.read_file(input_file)

    # new_tweets = []

    print 'writing1'
    # for tweet in tweets:
    #     text = tweet['text']
    #     text = text.lower()
    #     text = named.removeTwitterUsername(text)
    #     text = cleaner.removeStopwords(text)
    #     text = cleaner.removeSymbols(text)
    #     text = cleaner.removeLinks(text)
    #     text = cleaner.removeSufPort(text)
    #     text = cleaner.removeAccent(text)
    #     tweet['text'] = text
    #     new_tweets.append(tweet)

    # csv_management.write_file(output_file, tweets)

main()
