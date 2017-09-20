from minetext.classifying.naivebayes import NaiveBayes
from minetext.filemanager.filemanagement import *


def main():
    input_file = 'classifying/tweets_with_clusters.json'

    file_management = JSONFileManagement()

    documents = file_management.read_file(input_file)

    classifier = NaiveBayes(documents[0:500], documents[500:], 'cluster', [0, 1, 2, 3, 4])

    classifier.run()

main()
