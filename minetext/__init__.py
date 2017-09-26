from minetext.classifying.naivebayes import NaiveBayes
from minetext.filemanager.filemanagement import *

from minetext.clustering.distance import *
from minetext.clustering.kmedoids import *
from minetext.filemanager.filemanagement import *


def main():

    input_file = 'clustering/tweets_22_05_pln.tsv'
    output_file = 'clustering/tweets_with_clusters.json'
    output_file2 = 'clustering/centroids.json'
    distance_calculator = LevenshteinCalculator()
    file_writer = JSONFileManagement()

    with open(input_file) as json_data:
        points = dict()
        points['tweets'] = []

        for line in json_data:
            data = line.split('\t')
            if data[0] != 'id' and data[1] != 'text':
                point = dict()

                point['id'] = data[0]
                point['text'] = data[1].strip()
                points['tweets'].append(point)
            else:
                continue

        kmedoids = Kmedoids(k=5, tweets=points['tweets'], distance_calculator=distance_calculator)
        result = kmedoids.clustering()

        tweets = list()
        centroids = list()

        for cluster in result:
            centroids.append(cluster['medoid'])
            tweets += cluster['tweets']

        file_writer.write_file(output_file, tweets)
        file_writer.write_file(output_file2, centroids)

main()

# def main():
#     training_set = 'classifying/training_set.json'
#     test_set = 'classifying/test_set.json'
#     output_file = 'classifying/classified_tweets.json'
#
#     file_management = JSONFileManagement()
#
#     training_set = file_management.read_file(training_set)
#     test_set = file_management.read_file(test_set)
#
#     classifier = NaiveBayes(training_set, test_set, 'cluster', [1, 2, 3])
#
#     result = classifier.train()
#
#     file_management.write_file(output_file, result)
#
# main()
