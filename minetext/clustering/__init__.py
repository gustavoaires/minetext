from minetext.clustering.distance import *
from minetext.clustering.kmedoids import *
from minetext.filemanager.filemanagement import *
from minetext.textprocessor.portugueseprocessor import TextCleaner, NamedEntity

import minetext.visualization.wordcloud_visualization as wcv
import minetext.visualization.xy_plot as elbow_plotter


def main():
    print("start")
    input_file = "aug.json"
    target = "aug.json"
    output_file = "aug_jac_clusters.json"
    out_readable = "aug_jac_clusters_readable.json"
    # output_file2 = "clustering/centroids_levenshtein.json"
    distance_calculator = JaccardCalculatorDistance()
    file_writer = JSONFileManagement()
    file_reader = JSONFileManagement()

    target = file_reader.read_file(target)

    # clean readable data to plot word cloud
    text_processor = TextCleaner()
    named_entity = NamedEntity()
    for document in target:
        text = document["text"].lower()
        text = text_processor.removeAccent(text)
        text = text_processor.removeSymbols(text)
        text = text_processor.removeLinks(text)
        text = text_processor.removeStopwords(text)
        text = named_entity.removeTwitterUsername(text)
        document["text"] = text

    new_tweets = list()
    tweets = file_reader.read_file(input_file)
    for document in tweets:
        if "RT " not in document["text"]:
            text = document["text"].lower()
            text = text_processor.removeAccent(text)
            text = text_processor.removeSymbols(text)
            text = text_processor.removeLinks(text)
            text = text_processor.removeSufPort(text)
            text = text_processor.removeStopwords(text)
            text = named_entity.removeTwitterUsername(text)
            document["text"] = text
            new_tweets.append(document)

    kmedoids = Kmedoids(k=5, documents=new_tweets, distance_calculator=distance_calculator, collection_field="tweets", k_max=10)
    # result = kmedoids.calculate_elbow()
    # elbow_plotter.generate_xy_elbow_plot(result, "elbow.png")
    kmedoids.clustering()
    wcv.generate_readable_word_cloud_from_clusters("aug_jac", target, kmedoids.clusters, "tweets", "text",
                                     ["rt", "previdencia", "social", "reforma", "da", "de", "que", "para"])

    # print(result)

    # print kmedoids.n_most_similar_for_clusters_medoid(10)

    # tweets = list()
    # centroids = list()

    # for cluster in kmedoids.clusters:
    #     centroids.append(cluster["medoid"])
    #     tweets += cluster["tweets"]

    target = "aug.json"
    originals = file_reader.read_file(target)

    for document in kmedoids.documents:
        for original in originals:
            if document["id"] == original["id"]:
                original["cluster"] = document["cluster"]

    file_writer.write_file(output_file, kmedoids.documents)
    file_writer.write_file(out_readable, originals)

if __name__ == "__main__":
    main()
