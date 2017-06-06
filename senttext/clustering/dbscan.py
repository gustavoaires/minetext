from collections import defaultdict
from datetime import datetime
from math import sqrt, exp
from random import shuffle

progress = 0


def euclideanDistance(point, point2):
    x = float(point['latitude'])
    x1 = float(point2['latitude'])
    y = float(point['longitude'])
    y1 = float(point2['longitude'])

    return sqrt((x - x1) ** 2 + (y - y1) ** 2)


def fadingDistance(text1, text2):
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


def jaccardDistance(text1, text2):
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


def neighborhood(point, tweets, eps):
    neighborPts = []
    for point2 in tweets:

        # CHAME AQUI SUA MEDIDA DE SIMILARIDADE
        # distance = euclideanDistance(point, point2)
        # distance = fadingDistance(point, point2)
        distance = jaccardDistance(point, point2)

        if distance > eps:
            neighborPts.append(point2);
    return neighborPts


def expandCluster(tweets, point, neighborPts, cluster, eps, minPts):
    global progress
    point['cluster'] = cluster
    point['core'] = True

    for point1 in neighborPts:
        if not point1['visited']:
            point1['visited'] = True
            neighborPts1 = neighborhood(point1, tweets, eps)
            progress = progress + 1
            if len(neighborPts1) >= minPts:
                point1['core'] = True
                neighborPts.extend(neighborPts1)
        if point1['cluster'] == 0:
            point1['cluster'] = cluster


def dbScan(tweets, eps, minPts):
    global progress
    cluster = 0

    for point in tweets:
        if not point['visited']:
            point['visited'] = True
            neighborPts = neighborhood(point, tweets, eps)
            progress = progress + 1
            if len(neighborPts) < minPts:
                point['cluster'] = -1
            else:
                cluster += 1
                expandCluster(tweets, point, neighborPts, cluster, eps, minPts)


print '- - - - - - - - - - START - - - - - - - - - -'

# import json
import simplejson as json

# Coloque o CAMINHO/NOME do seu arquivo de entrada dentro da funcao open()
with open('tweets_25_05_pln.tsv') as json_data:
    # A linha abaixo le um arquivo em formato JSON
    # points = json.load(json_data)
    
    # O codigo abaixo le um arquivo txt(tabulado)
    points = {}
    points['tweets'] = []
    for line in json_data:
        data = line.split('\t')
        if data[0] == 'id' and data[1] == 'text': continue
        point = {}

        # Aqui vc deve criar os atributos que voce ira utilizar no DBSCAN
        # Por exemplo: Na medida de fadding, voce ira precisar do atributo de tempo.
        point['id'] = data[0]
        point['text'] = data[1].strip()
        # point['time'] = data[2].strip()
        point['visited'] = False
        point['cluster'] = 0
        point['core'] = False
        points['tweets'].append(point)

    # embaralhando os tweets
    shuffle(points['tweets'])

    # A funcao DBSCAN recebe um array de pontos, eps e minPoints.
    dbScan(points['tweets'], 0.4, 35)


print "######## CLUSTERS ########"

# Print cluster amount
groups = defaultdict(list)

for obj in points['tweets']:
    groups[obj['cluster']].append(obj)

# Caminho do arquivo de saida dos clusters
output_file = open('result_25_eps04_min35.txt', 'w')
for key in groups.keys():
    print ' -> ' + str(groups[key][0]['cluster']) + ': ' + str(len(groups[key]))
    for point in groups[key]:
        text = point['text']
        row = str(key) + "," + point['id'] + "," + text.encode('utf-8', 'ignore') + "," + str(point['core']) + "\n"
        output_file.write(row)


# print "######## CLUSTERS ########"

print '- - - - - - - - - -  END  - - - - - - - - - -'

