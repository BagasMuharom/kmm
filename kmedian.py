import numpy as np
import math
import distance

def centroidAwal(data, jumlah_cluster):
    temp = []
    for i in range(jumlah_cluster):
        rand = np.random.randint(len(data))
        
        while (temp.count(rand) > 0):
            rand = np.random.randint(len(data))
            
        temp.append(rand)
            
    return data[temp,:]

def clustering(centroid, data, distance = 'euclidean'):
    # list untuk menyimpan cluster baru dari data yang dihitung
    cluster_baru = []
    for i in data:
        # menyimpan hasil distance dari data tertentu terhadap semua centroid
        hasil_per_centroid = []
        # menghitung distance dari setiap centroid
        for k in centroid:
            if distance == 'euclidean':
                hasil_per_centroid.append(distance.euclidean(i, k))
            elif distance == 'manhattan':
                hasil_per_centroid.append(distance.manhattan(i, k))
            elif distance == 'minkowsky':
                hasil_per_centroid.append(distance.minkowsky(i, k))               
        
        cluster_baru.append(hasil_per_centroid.index(min(hasil_per_centroid)))

    return cluster_baru


def cari_centroid_baru(data, cluster, jumlah_cluster):
    dictionary = []
    # untuk menyimpan centroid baru
    centroids = []
    
    for i in range(jumlah_cluster):
        dictionary.append([])
    
    for i in range(len(data)):
        dictionary[cluster[i]].append(data[i])
        
#     for i in range(len(dictionary)):
#         centroids.append(np.array(dictionary[i]).mean(0))

    for i in range(len(dictionary)):
        centroids.append(np.median(dictionary[i], axis=0))
      
    return np.array(centroids)
