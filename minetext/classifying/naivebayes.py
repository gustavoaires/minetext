import pandas
import operator
import math
from sets import Set


class NaiveBayes(object):
    def __init__(self, training_set, test_set, label_field, labels, text_field_name='text'):
        self.training_set = training_set
        self.test_set = test_set
        self.label_field = label_field
        self.text_field_name = text_field_name
        self.labels = labels
        # words for indexing data frame
        self.words = Set()
        self.load_words_set()
        # data frame with the frequency
        self.df = pandas.DataFrame(columns=labels, index=self.words)
        self.classes_prob = self.assign_zero_to_classes()

    def load_words_set(self):
        for document in self.training_set:
            for word in document.split():
                self.words.add(word)

    def count_freq(self):
        words = Set()
        for document in self.training_set:
            label = document[self.label_field]
            text = document[self.text_field_name].split()
            for word in text:
                if word not in words:
                    words.add(word)
                    self.df.loc[word] = [0] * len(self.labels)
                    self.df.ix[word][label] += 1
                else:
                    self.df.ix[word][label] += 1
        self.df.sort_index(by=self.labels, ascending=[True] * len(self.labels), inplace=True)
        return self.df

    def assign_zero_to_classes(self):
        classes_prob = dict()
        for label in self.labels:
            classes_prob[label] = 0.0
        return classes_prob

    def calculate_class_probability(self):
        class_counts = self.assign_zero_to_classes()
        total = 0.0
        for index, row in self.df.iterrows():
            class_counts[max(row.iteritems(), key=operator.itemgetter(1))[0]] += 1.0
            total += 1.0
        for key in class_counts.keys():
            self.classes_prob[key] = class_counts[key] / total
        return self.classes_prob

    def naive_bayes(self, document, processed_words, words_per_class):
        no_words_in_doc = len(document[self.text_field_name].split())
        current_class_prob = dict()

        for label in self.labels:
            prob = math.log(self.classes_prob[label], 2) - no_words_in_doc * math.log(words_per_class[label], 2)
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

        self.calculate_class_probability()

        for word in self.df.index:
            processed_words.append(word)

        words_per_class = dict()

        for label in self.labels:
            words_per_class[label] = self.df[label].sum()

        for document in self.test_set:
            classification = self.naive_bayes_classify(document, processed_words, words_per_class)
            document['predicted_class'] = classification

        return self.test_set
