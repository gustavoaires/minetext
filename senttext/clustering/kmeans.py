from random import shuffle


class Kmeans(object):
    def __init__(self, k, tweets, distance_calculator):
        self.distance_calculator = distance_calculator
        self.k = k
        self.clusters = []
        self.tweets = tweets
        self.max = float("inf")
        self.init_clusters()
        self.set_random_centroids()

    def init_clusters(self):
        for i in range(self.k):
            cluster = dict()
            cluster['id'] = i
            cluster['centroid'] = None
            cluster['tweets'] = []
            self.clusters.append(cluster)

    def set_random_centroids(self):
        possible_centroids = []
        for i in range(len(self.tweets)):
            possible_centroids.append(i)

        shuffle(possible_centroids)

        for j in range(self.k):
            centroid = self.tweets[possible_centroids[j]]
            centroid['cluster'] = j
            self.clusters[j]['centroid'] = centroid

    def clear_clusters(self):
        for cluster in self.clusters:
            cluster['tweets'] = []

    def get_centroids(self):
        centroids = []
        for cluster in self.clusters:
            centroid = cluster['centroid']
            centroid['cluster'] = cluster['id']
            centroids.append(centroid)

        return centroids

    def assign_cluster(self):
        min = self.max
        self.clear_clusters()
        centroids = self.get_centroids()
        cluster_id = -1

        for i in range(len(self.tweets)):
            for j in range(len(centroids)):
                distance = self.distance_calculator.calculate(self.tweets[i], centroids[j])
                if distance < min:
                    min = distance
                    cluster_id = centroids[j]['cluster']

            self.tweets[i]['cluster'] = cluster_id
            self.get_cluster_by_id(cluster_id)['tweets'].append(self.tweets[i])
            cluster_id = -1
            min = self.max

    def calculate_centroids(self):
        dist = self.max
        centroids = []
        for i in range(len(self.clusters)):
            tweets = self.clusters[i]['tweets']
            tweets.append(self.clusters[i]['centroid'])
            for j in range(len(tweets)):
                acc_distance = 0.0
                for k in range(len(tweets)):
                    if not tweets[j]['id'] == tweets[k]['id']:
                        acc_distance += self.distance_calculator.calculate(tweets[j], tweets[k])

                try:
                    mean = acc_distance / (len(tweets) - 1)
                except ZeroDivisionError:
                    mean = dist
                if mean < dist:
                    dist = mean
                    self.clusters[j]['centroid'] = tweets[j]

            self.clusters[i]['centroid']['cluster'] = self.clusters[i]['id']
            centroids.append(self.clusters[i]['centroid'])
            dist = self.max
        return centroids

    def get_cluster_by_id(self, cluster_id):
        for i in range(len(self.clusters)):
            if self.clusters[i]['id'] == cluster_id:
                return self.clusters[i]
        return None

    def centroids_percent_variation(self, old_centroids, new_centroids):
        distance = 0.0
        for i in range(len(old_centroids)):
            distance += self.distance_calculator.calculate(old_centroids[i], new_centroids[i])
        mean = distance / len(old_centroids)
        return mean

    def clustering(self):
        for i in range(self.k):
            self.assign_cluster()
            self.calculate_centroids()
        return self.clusters
