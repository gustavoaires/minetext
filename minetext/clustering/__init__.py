from distance import *
from kmedoids import *
from minetext.filemanager.filemanagement import *


def main():

    input_file = 'tweets_22_05_pln.tsv'
    output_file = 'tweets_with_clusters.json'
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

        for cluster in result:
            # print cluster
            # val[cluster['id']] = len(cluster['tweets'])
            tweets += cluster['tweets']

        file_writer.write_file(output_file, tweets)

main()