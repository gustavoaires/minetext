from wordcloud import WordCloud
import matplotlib.pyplot as plt
import minetext.visualization.utils as utils


def generate_pure_word_cloud_from_clusters(save_dir_file, clusters, collection_field, text_field_name, ignored_words=list()):
    for cluster in clusters:
        __generate_word_cloud(save_dir_file, cluster, collection_field, text_field_name, ignored_words)


def generate_readable_word_cloud_from_clusters(save_dir_file, target, clusters, collection_field,
                                               text_field_name, ignored_words=list()):
    new_clusters = list()
    for cluster in clusters:
        matched_documents = utils.match_documents(cluster[collection_field], target)
        new_cluster = cluster
        new_cluster[collection_field] = matched_documents
        new_clusters.append(new_cluster)
        __generate_word_cloud(save_dir_file, new_cluster, collection_field, text_field_name, ignored_words)
    return new_clusters


def __generate_word_cloud(save_dir_file, cluster, collection_field, text_field_name, ignored_words):
    corpus = ""
    for document in cluster[collection_field]:
        filtered_words = [word for word in document[text_field_name].split() if word not in ignored_words]
        corpus += "".join(" ".join(filtered_words))
    generate_word_cloud(corpus, save_dir_file + "_" + str(cluster["id"]) + ".png")


def generate_word_cloud(corpus, save_dir):
    wc = WordCloud().generate(corpus)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(save_dir)

