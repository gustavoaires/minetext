import pandas
import operator
import math
from sets import Set


class NaiveBayes(object):

    def __init__(self, training_set, test_set, label_field, labels, text_field_name='text'):
        self.training_set = training_set
        self.test_set = test_set
        self.label_field = label_field
        self.text_field = text_field_name
        self.labels = labels
        # words for indexing data frame
        self.words = Set()
        # data frame with the frequency
        self.df = pandas.DataFrame(columns=labels, index=self.words)
        self.classes_prob = self.init_classes_zero()

    def count_freq(self):
        words_set = Set()
        for document in self.training_set:
            label = document[self.label_field]
            text = document[self.text_field_name].split()
            for word in text:
                if word not in words_set:
                    words_set.add(word)
                    self.df.loc[word] = [0] * len(self.labels)
                    self.df.ix[word][label] += 1
                else:
                    self.df.ix[word][label] += 1
        self.df.sort_index(by=self.labels, ascending=[True] * len(self.labels), inplace=True)
        return self.df

    def init_classes_zero(self):
        classes_prob = dict()
        for item in self.labels:
            classes_prob[item] = 0.0
        return classes_prob

    def calculate_class_probability(self):
        class_counts = self.init_classes_zero()
        total = 0.0
        for index, row in self.df.iterrows():
            class_counts[max(row.iteritems(), key=operator.itemgetter(1))[0]] += 1.0
            total += 1.0
        for key in class_counts.keys():
            self.classes_prob[key] = class_counts[key] / total
        return self.classes_prob

    # classifier
    def naive_bayes_classify(self, document, labels, processed_words, class_probabilities, words_per_class):
        no_words_in_doc = len(document)
        current_class_prob = {}

        for label in labels:
            prob = math.log(class_probabilities[label], 2) - no_words_in_doc * math.log(words_per_class[label], 2)
            for word in document:
                if word in processed_words:
                    occurence = self.df.loc[word][label]
                    if occurence > 0:
                        prob = prob + math.log(occurence, 2)
                    else:
                        prob = prob + math.log(1, 2)
                else:
                    prob = prob + math.log(1, 2)
            current_class_prob[label] = prob

        sorted_labels = sorted(current_class_prob.items(), key=operator.itemgetter(1))
        most_probable_class = sorted_labels[-1][0]
        return most_probable_class


    def classify(self):
        self.count_freq()

        processed_words = []

        class_prob_neg, class_prob_pos = self.calculate_class_probability()

        for word in dataframe.index:
            processed_words.append(word)

        class_probabilities = {'neg': class_prob_neg, 'pos': class_prob_pos}
        labels = class_probabilities.keys()
        words_per_class = {}

        for label in labels:
            words_per_class[label] = dataframe[label].sum()

        qtd_pos = 0
        qtd_neg = 0
        neg = self.incomplete_path + "neg/"
        pos = self.incomplete_path + "pos/"
        errou_neg = 0
        errou_pos = 0
        for document in self.test_set:
            classification = self.naive_bayes_classify(document[:-1], labels, processed_words, class_probabilities,
                                                  words_per_class)
            if classification == 'neg':
                qtd_neg += 1
                if neg not in document[-1]:
                    errou_neg += 1
            else:
                qtd_pos += 1
                if pos not in document[-1]:
                    errou_pos += 1
            print classification
            document.append(classification)
        self.write_test_set_classified()
        print dataframe
        print qtd_pos, ' - ', qtd_neg
        print errou_pos, ' - ', errou_neg
        print class_prob_neg, ' - ', class_prob_pos
