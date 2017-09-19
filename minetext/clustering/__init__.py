from distance import *
from kmedoids import *
from minetext.filemanager.filemanagement import *


def main():

    input_file = 'tweets_22_05_pln.tsv'
    output_file = 'tweets_with_clusters.json'
    output_file2 = 'centroids.json'
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
            centroids.append(cluster['centroid'])
            tweets += cluster['tweets']

        file_writer.write_file(output_file, tweets)
        file_writer.write_file(output_file2, centroids)

main()