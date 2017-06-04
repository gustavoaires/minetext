from datetime import datetime
from math import sqrt, exp


class DistanceCalculator(object):
    def levenshtein_distance(string1, string2):
        pass

    def euclidean_distance(point, point2):
        x = float(point['latitude'])
        x1 = float(point2['latitude'])
        y = float(point['longitude'])
        y1 = float(point2['longitude'])

        return sqrt((x - x1) ** 2 + (y - y1) ** 2)

    def fading_distance(text1, text2):
        FMT = '%H:%M:%S'
        if datetime.strptime(text1['time'], FMT) > datetime.strptime(text2['time'], FMT):
            tdelta = datetime.strptime(text1['time'], FMT) - datetime.strptime(text2['time'], FMT)
        else:
            tdelta = datetime.strptime(text2['time'], FMT) - datetime.strptime(text1['time'], FMT)

        timeDifference = tdelta.seconds / 60.0 / 60

        words1 = set(text1['text'].split())
        words2 = set(text2['text'].split())

        duplicates = words1.intersection(words2)
        uniques = words1.union(words2.difference(words1))

        try:
            simi = float(len(duplicates)) / (len(uniques) * exp(timeDifference))
            return simi
        except:
            return 0.0

    def jaccard_distance(text1, text2):
        words1 = set(text1['text'].split())
        words2 = set(text2['text'].split())

        duplicated = len(words1.intersection(words2))
        # uniques = len(words1.union(words2.difference(words1)))

        tam1 = len(text1['text'].split())
        tam2 = len(text2['text'].split())

        if tam1 > tam2:
            maior = tam1
        else:
            maior = tam2

        try:
            simi = float(duplicated) / maior
            return simi
        except ZeroDivisionError:
            return 0.0
