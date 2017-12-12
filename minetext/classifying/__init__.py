from minetext.classifying.naivebayes import NaiveBayes
from minetext.filemanager.filemanagement import *
from random import shuffle


def main():
    input_file = 'aug_jac_clusters.json'
    output_file = 'aug_jac_class.json'

    file_management = JSONFileManagement()

    set = file_management.read_file(input_file)

    shuffle(set)

    training_set = list()
    test_set = list()
    cluster_0 = 0
    cluster_1 = 0
    cluster_2 = 0
    cluster_3 = 0
    cluster_4 = 0
    for document in set:
        if document["cluster"] == 0 and cluster_0 < 158:
            cluster_0 += 1
            training_set.append(document)
        elif document["cluster"] == 1 and cluster_1 < 158:
            cluster_1 += 1
            training_set.append(document)
        elif document["cluster"] == 2 and cluster_2 < 158:
            cluster_2 += 1
            training_set.append(document)
        elif document["cluster"] == 3 and cluster_3 < 158:
            cluster_3 += 1
            training_set.append(document)
        elif document["cluster"] == 4 and cluster_4 < 158:
            cluster_4 += 1
            training_set.append(document)
        elif len(test_set) < 48:
            test_set.append(document)

    classifier = NaiveBayes(training_set, test_set, 'cluster', [0, 1, 2, 3, 4])

    result = classifier.train()

    correct_total = 0
    incorrect_total = 0

    for document in result:
        if document["predicted_class"] == document["cluster"]:
            correct_total += 1
        else:
            incorrect_total += 1

    # training set
    correct_percent = correct_total / len(result)
    incorrect_percent = incorrect_total / len(result)

    print('train correct total', correct_total)
    print('train incorrect total', incorrect_total)
    print('train correct percent', correct_percent * 100)
    print('train incorrect percent', incorrect_percent * 100)

    # test set
    result = classifier.test()

    correct_total = 0
    incorrect_total = 0

    for document in result:
        if document["predicted_class"] == document["cluster"]:
            correct_total += 1
        else:
            incorrect_total += 1

    correct_percent = correct_total / len(result)
    incorrect_percent = incorrect_total / len(result)

    print('test correct total', correct_total)
    print('test incorrect total', incorrect_total)
    print('test correct percent', correct_percent * 100)
    print('test incorrect percent', incorrect_percent * 100)

    file_management.write_file(output_file, result)

if __name__ == "__main__":
    main()
