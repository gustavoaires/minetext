# -*- coding: latin-1 -*-
from collecting.datacollect import APICollect, ScrapeCollect
from textprocessor.portugueseprocessor import TextCleaner, NamedEntity
from filemanager.filemanagement import JSONFileManagement, CSVTSVFileManagement
import json


def main():
    CONSUMER_KEY = '4jtRRPl3WvYyzPvRnNKRaaLGr'
    CONSUMER_SECRET = 'dFr8l0HDQ2RA3sQhiTjkMvJs9ML38BLkEoofDNr50tBEOCmZNA'
    ACCESS_TOKEN = '98992106-OsffZtvTWPxeHCkA5G9golyjU4inlvb7XB6g0oDva'
    ACCESS_TOKEN_SECRET = 'eD0RE8AyfTDmyYnOKfWLo3XvjILKktRJOIoQnlmHCmbip'

    files = ['tweets_22_05.json', 'tweets_23_05.json', 'tweets_24_05.json', 'tweets_25_05.json']
    tsv_text = 'result_22_25_eps04_min50.txt'
    output_file = 'tweets_28_08.json'

    print output_file

    query = "previdencia social OR reforma da previdencia OR reforma da presidencia OR previdencia since:2017-08-28 until:2017-08-29"
    scrape = ScrapeCollect()
    tweets = scrape.scrape_tweets(query)

    # api = APICollect(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # tweets = api.rest_tweets(query=query)

    # print len(tweets)

    json_management = JSONFileManagement()
    json_management.write_file(output_file, tweets, 'w')
    # tweets_json = []
    # for j_file in files:
    #     for tweet in json_management.read_file(j_file):
    #         tweets_json.append(tweet)
    #
    # print len(tweets_json)
    #
    # tweets_tsv = []
    # with open(tsv_text) as tsv_data:
    #
    #     for line in tsv_data:
    #         data = line.split(',')
    #         tweet = dict()
    #         tweet['cluster'] = data[0]
    #         tweet['id'] = data[1]
    #         tweets_tsv.append(tweet)
    #
    # clusters = dict()
    # clusters['1'] = []
    # clusters['2'] = []
    # clusters['3'] = []
    # clusters['4'] = []
    # clusters['-1'] = []
    #
    # for tweet in tweets_json:
    #     for data in tweets_tsv:
    #         if tweet['id'] == int(data['id']):
    #             clusters[data['cluster']].append(tweet)
    #
    # for key in clusters.keys():
    #     output = open('cluster_'+key+'.txt', 'w')
    #     row = ''
    #     for tweet in clusters[key]:
    #         row = row + (tweet['text']).encode('utf-8') + '\n'
    #     output.write(row)
    #
    # print tweets[0]
    # for tweet in tweets:
    #     json.dump(tweet, output_file)
    #     output_file.write("\n")

    #
    # cleaner = TextCleaner()
    # named = NamedEntity()
    # csv_management = CSVTSVFileManagement()
    #
    # print 'reading1'
    # tweets = json_management.read_file(input_file)

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

    # csv_management.write_file(output_file, new_tweets, delimiter='\t')

main()
