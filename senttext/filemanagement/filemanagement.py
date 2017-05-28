# -*- coding: latin-1 -*-
import json
import csv
from ..textprocessor import coordinateformater


class JSONFileManagement(object):
    def read_file(self, path):
        """
        :param path: diretory of storage
        :return: list of tweets from the file
        """
        tweets = []
        input_file = open(path, 'r')

        for line in input_file:
            tweets.append(json.loads(line))

        input_file.close()
        return tweets

    def write_file(self, path, tweets, mode='w'):
        """
        :param path: diretory of storage 
        :param tweets: list of tweets to save
        :param mode: how to write (w: write, a:append, etc)
        :return: void 
        """
        output_file = open(path, mode)

        for tweet in tweets:
            json.dump(tweet, output_file)
            output_file.write('\n')

        output_file.close()


class CSVTSVFileManagement(object):
    def __init__(self):
        """
        :header: used to print the first line of the csv or tsv file
        :points: used to format the coordinates value into latitude and longitude
        """
        self.header = 'id|text|lat|lon'
        self.points = coordinateformater.CoordinateFormater()

    def read_file(self, path, delimiter=','):
        """
        :param path: just the string conatining the file path 
        :param delimiter: value delimiter inside the file
        :return: list of tweets from the file
        """
        tweets = []
        input_file = open(path, 'r')
        reader = csv.DictReader(input_file, delimiter=delimiter)

        for line in reader:
            tweets.append(line)

        input_file.close()
        return tweets

    def write_file(self, path, tweets, mode='w', delimiter=','):
        """
        :param path: just the string conatining the file path
        :param tweets: list of tweets to save
        :param mode: how to write (w: write, a:append, etc)
        :param delimiter: value delimiter inside the file
        :return: void
        """
        output_file = open(path, mode)
        self.header.replace('|', delimiter)
        output_file.write(self.header)

        for tweet in tweets:
            try:
                lat_lon = tweet["coordinates"]
                lat_lon = self.points.formatCoordinate(lat_lon)
                lat = lat_lon[0]
                lon = lat_lon[1]
                row = tweet["id"] + delimiter + tweet['text'] + delimiter + lat + delimiter + lon + "\n"
                output_file.write(row)
            except (UnicodeDecodeError, csv.Error, AttributeError, KeyError) as e:
                print e, "\n"
                print "Tweet should contain id, text and coordinates"

        output_file.close()
