from random import shuffle


class Kmedoids(object):
    def __init__(self, k, documents, distance_calculator, collection_field="documents", text_field_name="text", k_min=2, k_max=None, max_err_increase=None):
        self.distance_calculator = distance_calculator
        self.k = k
        self.clusters = []
        self.documents = documents
        self.max = float("inf")
        self.k_min = k_min
        self.k_max = k_max
        self.max_err_increase = max_err_increase
        self.text_field_name = text_field_name
        self.collection_field = collection_field
        self.medoid_field = "medoid"

    def init_clusters(self):
        for i in range(self.k):
            cluster = dict()
            cluster["id"] = i
            cluster[self.medoid_field] = None
            cluster[self.collection_field] = []
            self.clusters.append(cluster)

    def init_documents(self):
        for i in range(len(self.documents)):
            self.documents[i]["cluster"] = None

    def set_random_medoids(self):
        possible_medoids = []
        for i in range(len(self.documents)):
            possible_medoids.append(i)

        shuffle(possible_medoids)

        for j in range(self.k):
            medoid = self.documents[possible_medoids[j]]
            medoid["cluster"] = j
            
            self.clusters[j][self.medoid_field] = medoid

    def clear_clusters(self):
        for cluster in self.clusters:
            cluster[self.collection_field] = []

    def get_medoids(self):
        medoids = []
        for cluster in self.clusters:
            medoid = cluster[self.medoid_field]
            medoid["cluster"] = cluster["id"]
            medoids.append(medoid)

        return medoids

    def assign_cluster(self):
        min_dist = self.max
        self.clear_clusters()
        medoids = self.get_medoids()
        cluster_id = -1

        for i in range(len(self.documents)):
            if not self.documents[i]["cluster"]:
                for j in range(len(medoids)):
                    distance = self.distance_calculator\
                        .calculate(self.documents[i][self.text_field_name], medoids[j][self.text_field_name])

                    if distance < min_dist:
                        min_dist = distance
                        cluster_id = medoids[j]["cluster"]
            else:
                cluster_id = self.documents[i]["cluster"]

            self.documents[i]["cluster"] = cluster_id
            self.get_cluster_by_id(cluster_id)[self.collection_field].append(self.documents[i])

            cluster_id = -1
            min_dist = self.max

    def calculate_medoids(self):
        dist = self.max
        medoids = []
        for i in range(len(self.clusters)):
            documents = self.clusters[i][self.collection_field]
            documents.append(self.clusters[i][self.medoid_field])
            for j in range(len(documents)):
                acc_distance = 0.0
                for k in range(len(documents)):
                    if not documents[j]["id"] == documents[k]["id"]:
                        acc_distance += self.distance_calculator\
                            .calculate(documents[j][self.text_field_name], documents[k][self.text_field_name])

                mean = acc_distance / (len(documents))

                if mean < dist:
                    dist = mean
                    self.clusters[i][self.medoid_field] = documents[j]

            self.clusters[i][self.medoid_field]["cluster"] = self.clusters[i]["id"]
            medoids.append(self.clusters[i][self.medoid_field])
            dist = self.max
        return medoids

    def get_cluster_by_id(self, cluster_id):
        for i in range(len(self.clusters)):
            if self.clusters[i]["id"] == cluster_id:
                return self.clusters[i]
        return None

    def clustering(self):
        self.setup_environment()
        self.assign_cluster()
        return self.clusters

    def calculate_sse(self):
        distance_sum = 0
        for cluster in self.clusters:
            for document in cluster[self.collection_field]:
                distance = self.distance_calculator\
                    .calculate(document[self.text_field_name], cluster[self.medoid_field][self.text_field_name])
                distance_sum += distance * distance
        return distance_sum

    def calculate_elbow(self):
        original_k = self.k
        sses = dict()
        for k in range(self.k_min, self.k_max+1):
            self.k = k
            self.clustering()
            sses[k] = self.calculate_sse()
            if self.max_err_increase is not None \
                    and k is not self.k_min \
                    and (sses[k] - sses[k-1]) > self.max_err_increase:
                break
        self.k = original_k
        return sses

    def setup_environment(self):
        self.init_clusters()
        self.init_documents()
        self.set_random_medoids()

    def set_k(self, k):
        self.k = k

    def n_most_similar_for_clusters_medoid(self, n):
        n_most_similar = dict()
        for cluster in self.clusters:
            n_most_similar[cluster["id"]] = sorted(
                [self.calculate_distance_document_tuple(document, cluster[self.medoid_field])
                    for document in cluster[self.collection_field]],
                key=lambda x: x[0]
            )[:n]
        return n_most_similar

    def calculate_distance_document_tuple(self, document, target):
        distance = self.distance_calculator \
            .calculate(document[self.text_field_name], target[self.text_field_name])
        return distance, document
