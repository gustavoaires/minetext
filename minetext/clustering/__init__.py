from distance import *
from kmedoids import *


def main():

    input_file = 'tweets_test.tsv'
    distance_calculator = LevenshteinCalculator()

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

        kmedoids = Kmedoids(k=3, tweets=points['tweets'], distance_calculator=distance_calculator)
        result = kmedoids.clustering()

        val = dict()

        for cluster in result:
            print cluster
            val[cluster['id']] = len(cluster['tweets'])

        print val
main()