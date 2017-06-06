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

        kmeans = Kmeans(k=3, tweets=points['tweets'], distance_calculator=distance_calculator)
        result = kmeans.clustering()

        cluster0 = 0
        cluster1 = 0
        cluster2 = 0

        for cluster in result:
            for tweet in cluster['tweets']:
                if tweet['cluster'] == 0: cluster0 += 1
                elif tweet['cluster'] == 1: cluster1 += 1
                else: cluster2 += 1

        print cluster0, cluster1, cluster2
main()