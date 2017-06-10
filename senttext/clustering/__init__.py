from distance import *
from kmeans import *


def main():

    input_file = 'tweets_25_05_pln.tsv'
    distance_calculator = LevenshteinCalculator()

    with open(input_file) as json_data:
        points = dict()
        points['tweets'] = []

        for line in json_data:
            data = line.split('\t')
            if data[0] == 'id' and data[1] == 'text': continue
            point = dict()

            point['id'] = data[0]
            point['text'] = data[1].strip()
            points['tweets'].append(point)

        kmeans = Kmeans(k=20, tweets=points['tweets'], distance_calculator=distance_calculator)
        result = kmeans.clustering()

        val = dict()

        for cluster in result:
            print cluster
            val[cluster['id']] = len(cluster['tweets'])

        print val
main()