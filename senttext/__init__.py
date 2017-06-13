# -*- coding: latin-1 -*-
from collecting.datacollect import APICollect
from textprocessor.portugueseprocessor import TextCleaner, NamedEntity
from filemanagement.filemanagement import JSONFileManagement, CSVTSVFileManagement
import json


def main():
    CONSUMER_KEY = '4jtRRPl3WvYyzPvRnNKRaaLGr'
    CONSUMER_SECRET = 'dFr8l0HDQ2RA3sQhiTjkMvJs9ML38BLkEoofDNr50tBEOCmZNA'
    ACCESS_TOKEN = '98992106-OsffZtvTWPxeHCkA5G9golyjU4inlvb7XB6g0oDva'
    ACCESS_TOKEN_SECRET = 'eD0RE8AyfTDmyYnOKfWLo3XvjILKktRJOIoQnlmHCmbip'

    input_file = 'tweets_25_05.json'
    output_file = 'tweets_09_06.json'

    query = "previdencia social OR reforma da previdencia OR reforma da presidencia OR previdencia since:2017-06-09 until:2017-06-10"
    # scrape = datacollect.ScrapeCollect()
    # tweets = scrape.scrape_tweets(query, 20)

    api = APICollect(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    tweets = api.rest_tweets(query=query)

    print len(tweets)

    json_management = JSONFileManagement()
    json_management.write_file(output_file, tweets)

    # for tweet in tweets:
    #     json.dump(tweet, output_file)
    #     output_file.write("\n")

    # cleaner = TextCleaner()
    # named = NamedEntity()
    # csv_management = CSVTSVFileManagement()

    # print 'reading1'
    tweets = json_management.read_file(input_file)

    # new_tweets = []

    # print 'writing1'
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
    #
    # csv_management.write_file(output_file, new_tweets, delimiter='\t')

main()
