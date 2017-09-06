import pandas
import operator
import math
from sets import Set

training_set = []
test_set = []

# words to indexing data frame
words = Set()

# data frame with the frequency
df = pandas.DataFrame(columns=['neg', 'pos'], index=words)


def count_freq():
    words_set = Set()
    for item in training_set:
        label = item[1]
        text = item[0]
        for word in text:
            if word not in words_set:
                words_set.add(word)
                df.loc[word] = [0, 0]
                df.ix[word][label] += 1
            else:
                df.ix[word][label] += 1
    df.sort_index(by=['neg', 'pos'], ascending=[True, True], inplace=True)
    return df


# class probabilities
class_prob_pos = 0.0
class_prob_neg = 0.0


def calculate_class_probability(df):
    count_pos = 0.0
    count_neg = 0.0
    total = 0.0
    for index, row in df.iterrows():
        if row['neg'] > row['pos']:
            count_neg = count_neg + 1.0
        elif row['neg'] < row['pos']:
            count_pos = count_pos + 1.0
        total = total + 1.0
    class_prob_neg = count_neg / total
    class_prob_pos = count_pos / total
    class_prob_neg = class_prob_neg
    class_prob_pos = class_prob_pos
    return class_prob_neg, class_prob_pos


# classifier
def naive_bayes_classify(document, labels, processed_words, class_probabilities, words_per_class, df):
    no_words_in_doc = len(document)
    current_class_prob = {}

    for label in labels:
        prob = math.log(class_probabilities[label], 2) - no_words_in_doc * math.log(words_per_class[label], 2)
        for word in document:
            if word in processed_words:
                occurence = df.loc[word][label]
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


def main():
    df = count_freq()

    dataframe = df[-12000:]

    processed_words = []

    class_prob_neg, class_prob_pos = calculate_class_probability(dataframe)

    for word in dataframe.index:
        processed_words.append(word)

    class_probabilities = {'neg': class_prob_neg, 'pos': class_prob_pos}
    labels = class_probabilities.keys()
    words_per_class = {}

    for label in labels:
        words_per_class[label] = df[label].sum()

    for document in test_set:
        classification = naive_bayes_classify(document[:-1], labels, processed_words, class_probabilities,
                                              words_per_class, dataframe)
        document.append(classification)

main()
