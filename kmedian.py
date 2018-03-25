import numpy as np
import math
import distance as dt

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
                hasil_per_centroid.append(dt.euclidean(i, k))
            elif distance == 'manhattan':
                hasil_per_centroid.append(dt.manhattan(i, k))
            elif distance == 'minkowsky':
                hasil_per_centroid.append(dt.minkowsky(i, k))               
        
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
        
    # for i in range(len(dictionary)):
    #     centroids.append(np.array(dictionary[i]).mean(0))

    for i in range(len(dictionary)):
        centroids.append(np.median(dictionary[i], axis=0))
      
    return np.array(centroids)

def kmedian(dataset, jumlah_cluster, centroid, distance):
    temp_centroid_akhir = centroid
    centroid_akhir = []
    cluster = []
    i = 0 

    # k-median dengan euclidean
    while np.array_equal(temp_centroid_akhir, centroid_akhir) == False:
        centroid_akhir = temp_centroid_akhir
        cluster = clustering(centroid_akhir, dataset, distance)
        temp_centroid_akhir = cari_centroid_baru(dataset, cluster, jumlah_cluster)
        i += 1

    return {
        'cluster_baru' : cluster,
        'centroid_akhir' : np.array(temp_centroid_akhir).tolist(),
        'iterasi' : i
    }
