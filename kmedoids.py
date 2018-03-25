import numpy as np
import dataset
import math
import distance as dt

def randomCentroid(dataset, jumlah_cluster):
    temp = []
    
    for i in range(jumlah_cluster):
        rand = np.random.randint(len(dataset))
        
        while (temp.count(rand) > 0):
            rand = np.random.randint(len(dataset))
            
        temp.append(rand)
        
    return dataset[temp,:]

def defineCentroid(dataset, jumlah_cluster, ex_centroid = []):
    rand = randomCentroid(dataset, jumlah_cluster)
    
    return rand

def clustering(dataset, centroid, distance = 'euclidean'):
    cluster = []
    biaya = 0
    
    for i in dataset:
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
        
        minim = min(hasil_per_centroid)
        index = hasil_per_centroid.index(minim)
        biaya += minim
        cluster.append(index)
        
    return {'cluster_baru': cluster, 'biaya': biaya}

def kmedoids(dataset, jumlah_cluster, distance, threshold, centroid_awal):
    centroid = centroid_awal
    biaya_terkecil = 10000
    cluster = {}
    i = 0

    while biaya_terkecil > threshold and i < 500:

        hasil = clustering(dataset, centroid, distance)
        biaya = hasil['biaya']
        
        if i == 0 or biaya < biaya_terkecil:
            biaya_terkecil = biaya
            cluster = hasil

        if biaya_terkecil > threshold:
            centroid = defineCentroid(dataset, jumlah_cluster)

        i += 1

    cluster['centroid_akhir'] = np.array(centroid).tolist()
    cluster['iterasi'] = i

    return cluster