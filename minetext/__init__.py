from minetext.clustering.distance import *
from minetext.clustering.kmedoids import *
from minetext.filemanager.filemanagement import *


def main():
    print 'start'
    input_file = 'clustering/tweets_22_05_pln.tsv'
    output_file = 'clustering/tweets_with_clusters_jaccard.json'
    output_file2 = 'clustering/centroids.json'
    distance_calculator = JaccardCalculatorDistance()
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

        kmedoids = Kmedoids(k=3, tweets=points['tweets'], distance_calculator=distance_calculator)
        kmedoids.clustering()

        print kmedoids.n_most_similar_for_clusters_medoid(3)

        # tweets = list()
        # centroids = list()

        # for cluster in kmedoids.clusters:
        #     centroids.append(cluster['medoid'])
        #     tweets += cluster['tweets']

        # file_writer.write_file(output_file, tweets)
        # file_writer.write_file(output_file2, centroids)

if __name__ == "__main__":
    main()
