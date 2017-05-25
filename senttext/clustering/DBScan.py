from collections import defaultdict
from datetime import datetime
from datetime import timedelta
import math

progress = 0

def euclideanDistance(point, point2):
    x = float(point['latitude'])
    x1 = float(point2['latitude'])
    y = float(point['longitude'])
    y1 = float(point2['longitude'])

    return sqrt((x - x1)**2 + ( y - y1)**2)

def fadingDistance(text1, text2):

    FMT = '%H:%M:%S'
    if datetime.strptime(text1['time'], FMT) > datetime.strptime(text2['time'], FMT):
        tdelta = datetime.strptime(text1['time'], FMT) - datetime.strptime(text2['time'], FMT)
    else:
        tdelta = datetime.strptime(text2['time'], FMT) - datetime.strptime(text1['time'], FMT)

    timeDifference = tdelta.seconds/60.0/60

    words1 = set(text1['text'].split())
    words2 = set(text2['text'].split())

    duplicates = words1.intersection(words2)
    uniques = words1.union(words2.difference(words1))
    
    try:
        simi = float(len(duplicates))/(len(uniques) * math.exp(timeDifference))
        return simi
    except:
        print "Error to get similarity"
        return 0.0

def jaccardDistance(text1, text2):

    words1 = set(text1['text'].split())
    words2 = set(text2['text'].split())

    duplicates  = words1.intersection(words2)
    uniques = words1.union(words2.difference(words1))
    
    try:
        simi = float(len(duplicates))/(len(uniques))
        return simi
    except:
        print "Error to get similarity"
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

    for point1 in neighborPts:	
        if not point1['visited']:
            point1['visited'] = True
            neighborPts1 = neighborhood(point1, tweets, eps)
            progress = progress + 1
            print progress
            print " ----- Neibohood inside = " + str(len(neighborPts1))
            if len(neighborPts1) >= minPts:
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
            print progress
            print " --- Neibohood = " + str(len(neighborPts))
            if len(neighborPts) < minPts:
                point['cluster'] = -1
            else:
                print " ----- Criou um cluster -----"
                cluster += 1
                # point['cluster'] = cluster
                expandCluster(tweets, point, neighborPts, cluster, eps, minPts)


print '- - - - - - - - - - START - - - - - - - - - -'

#import json
import simplejson as json

# Coloque o CAMINHO/NOME do seu arquivo de entrada dentro da funcao open()
with open('tweets_30.tsv') as json_data:
    # A linha abaixo le um arquivo em formato JSON
    # points = json.load(json_data)
    
    # O codigo abaixo le um arquivo txt(tabulado)
    points = {}
    points['tweets'] = []
    for line in json_data:
        data = line.split('\t')
        point = {}

        # Aqui vc deve criar os atributos que voce ira utilizar no DBSCAN
        # Por exemplo: Na medida de fadding, voce ira precisar do atributo de tempo.
        point['id'] = data[0]
        point['text'] = data[1].strip()
        point['time'] = data[2].strip()
        points['tweets'].append(point)
    

    for point in points['tweets']:
        point['visited'] = False
        point['cluster'] = 0
    
    # A funcao DBSCAN recebe um array de pontos, eps e minPoints.
    dbScan(points['tweets'], 0.3, 500)
    


print "######## CLUSTERS ########"

# Print cluster amount
groups = defaultdict(list)

for obj in points['tweets']:
    groups[obj['cluster']].append(obj)

output_file = 0
new_list = groups.values()
quantCluster = len(new_list)

# Caminho do arquivo de saida dos clusters
output_file = open('/Users/LeonelJR/Documents/TCC/DBSCAN/result_30_eps03_min500.txt','a')
for x in range(0, quantCluster):
    print ' -> ' + str(new_list[x][0]['cluster']) + ': ' + str(len(new_list[x]))
    for y in range(0, len(new_list[x])):
        # if new_list[x][y]['cluster'] != -1:
        #     print new_list[x][y]['id']
        if new_list[x][y]['cluster'] != -1:
            text = new_list[x][y]['text']
            row = (text).encode('utf-8','ignore')+"\n"
            output_file.write(row)


# print "######## CLUSTERS ########"

print '- - - - - - - - - -  END  - - - - - - - - - -'

