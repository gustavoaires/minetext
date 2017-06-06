from datetime import datetime
from math import sqrt, exp
import numpy as np


class LevenshteinCalculator(object):
    def calculate(self, source, target):
        if len(source) < len(target):
            return self.calculate(target, source)

        if len(target) == 0:
            return len(source)

        source = np.array(tuple(source))
        target = np.array(tuple(target))

        previous_row = np.arange(target.size + 1)
        for s in source:
            current_row = previous_row + 1

            current_row[1:] = np.minimum(current_row[1:], np.add(previous_row[:-1], target != s))

            current_row[1:] = np.minimum(current_row[1:], current_row[0:-1] + 1)

            previous_row = current_row

        return previous_row[-1]


class EuclideanCalculator(object):
    def calculate(self, source, target):
        x1 = float(source['latitude'])
        x2 = float(target['latitude'])
        y1 = float(source['longitude'])
        y2 = float(target['longitude'])

        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class FadingCalculator(object):
    def calculate(self, source, target):
        FMT = '%H:%M:%S'
        if datetime.strptime(source['time'], FMT) > datetime.strptime(target['time'], FMT):
            tdelta = datetime.strptime(source['time'], FMT) - datetime.strptime(target['time'], FMT)
        else:
            tdelta = datetime.strptime(target['time'], FMT) - datetime.strptime(source['time'], FMT)

        timeDifference = tdelta.seconds / 60.0 / 60

        words1 = set(source['text'].split())
        words2 = set(target['text'].split())

        duplicates = words1.intersection(words2)
        uniques = words1.union(words2.difference(words1))

        try:
            simi = float(len(duplicates)) / (len(uniques) * exp(timeDifference))
            return simi
        except:
            return 0.0


class JaccardCalculator(object):
    def calculate(self, source, target):
        words1 = set(source['text'].split())
        words2 = set(target['text'].split())

        duplicated = len(words1.intersection(words2))
        # uniques = len(words1.union(words2.difference(words1)))

        tam1 = len(words1)
        tam2 = len(words2)

        if tam1 > tam2:
            maior = tam1
        else:
            maior = tam2

        try:
            simi = float(duplicated) / maior
            return simi
        except ZeroDivisionError:
            return 0.0
