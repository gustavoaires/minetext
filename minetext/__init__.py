from minetext.clustering.distance import *
from minetext.clustering.kmedoids import *
from minetext.filemanager.filemanagement import *
from minetext.textprocessor.portugueseprocessor import TextCleaner, NamedEntity

import minetext.visualization.wordcloud_visualization as wcv
import minetext.visualization.xy_plot as elbow_plotter


def main():
    print("start")
    input_file = "clustering/tweets_22_05_pln.tsv"
    target = "tweets_22_05.json"
    # output_file = "clustering/tweets_with_clusters_levenshtein.json"
    # output_file2 = "clustering/centroids_levenshtein.json"
    distance_calculator = JaccardCalculatorDistance()
    file_writer = JSONFileManagement()

    target = file_writer.read_file(target)

    # clean readable data to plot word cloud
    text_processor = TextCleaner()
    named_entity = NamedEntity()
    for document in target:
        text = document["text"].lower()
        text = text_processor.removeAccent(text)
        text = text_processor.removeSymbols(text)
        text = text_processor.removeLinks(text)
        text = named_entity.removeTwitterUsername(text)
        document["text"] = text

    with open(input_file) as json_data:
        points = dict()
        points["tweets"] = []

        for line in json_data:
            data = line.split("\t")
            if data[0] != "id" and data[1] != "text":
                point = dict()

                point["id"] = data[0]
                point["text"] = data[1].strip()
                points["tweets"].append(point)
            else:
                continue

        kmedoids = Kmedoids(k=4, documents=points["tweets"], distance_calculator=distance_calculator, collection_field="tweets", k_max=10)
        result = kmedoids.calculate_elbow()
        # elbow_plotter.generate_xy_elbow_plot(result, "elbow.png")
        kmedoids.clustering()
        wcv.generate_readable_word_cloud_from_clusters("22_05_read", target, kmedoids.clusters, "tweets", "text",
                                         ["rt", "previdencia", "social", "reforma", "da", "de", "que", "para"])

        # print(result)

        # print kmedoids.n_most_similar_for_clusters_medoid(10)

        # tweets = list()
        # centroids = list()

        # for cluster in kmedoids.clusters:
        #     centroids.append(cluster["medoid"])
        #     tweets += cluster["tweets"]

        # file_writer.write_file(output_file, tweets)
        # file_writer.write_file(output_file2, centroids)

if __name__ == "__main__":
    main()
