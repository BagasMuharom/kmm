from flask import Flask, make_response, render_template, jsonify, session, request, json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import io
import kmedian
import kmedoids
import numpy as np
import dataset

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', datasets = dataset.sampledata, datasetskasus = dataset.dataset)

@app.route('/plot/kmedian')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = dataset.sampledata[:,0]
    ys = dataset.sampledata[:,1]

    color = ['red', 'green', 'blue', 'orange', 'cyan', 'violet']

    for i in range(len(xs)):
        if request.args.get('distance') == 'euclidean':
            # centroid_akhir = np.array(session['centroid_akhir_euclidean'])
            axis.scatter(xs[i], ys[i], color = color[session['cluster_euclidean'][i]])
            # axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')            
        elif request.args.get('distance') == 'manhattan':
            # centroid_akhir = np.array(session['centroid_akhir_manhattan'])            
            axis.scatter(xs[i], ys[i], color = color[session['cluster_manhattan'][i]])
            # axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')                        
        elif request.args.get('distance') == 'minkowsky':
            # centroid_akhir = np.array(session['centroid_akhir_minkowsky'])            
            axis.scatter(xs[i], ys[i], color = color[session['cluster_minkowsky'][i]])
            # axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')                        
            
    # centroid_awal = np.array(session['centroid_awal'])
    # axis.scatter(centroid_awal[:,0],centroid_awal[:,1], color = 'black')

    axis.grid()
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/cluster/sample/kmedian')
def cluster_umum():
    kcluster = 6
    cluster_euclidean = []
    centroid = kmedian.centroidAwal(dataset.sampledata, kcluster)
    centroid_akhir_euclidean = []
    temp_centroid_akhir = centroid

    # k-median dengan euclidean
    while np.array_equal(temp_centroid_akhir, centroid_akhir_euclidean) == False:
        centroid_akhir_euclidean = temp_centroid_akhir
        cluster_euclidean = kmedian.clustering(centroid_akhir_euclidean, dataset.sampledata)
        temp_centroid_akhir = kmedian.cari_centroid_baru(dataset.sampledata, cluster_euclidean, kcluster)
    
    # k-median dengan manhattan
    temp_centroid_akhir = centroid
    centroid_akhir_manhattan = []
    cluster_manhattan = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_manhattan) == False:
        centroid_akhir_manhattan = temp_centroid_akhir
        cluster_manhattan = kmedian.clustering(centroid_akhir_manhattan, dataset.sampledata, 'manhattan')
        temp_centroid_akhir = kmedian.cari_centroid_baru(dataset.sampledata, cluster_manhattan, kcluster)
    
    # k-median dengan minkowsky
    temp_centroid_akhir = centroid
    centroid_akhir_minkowsky = []
    cluster_minkowsky = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_minkowsky) == False:
        centroid_akhir_minkowsky = temp_centroid_akhir
        cluster_minkowsky = kmedian.clustering(centroid_akhir_minkowsky, dataset.sampledata, 'minkowsky')
        temp_centroid_akhir = kmedian.cari_centroid_baru(dataset.sampledata, cluster_minkowsky, kcluster)
    
    session['cluster_euclidean'] = cluster_euclidean
    session['cluster_manhattan'] = cluster_manhattan
    session['cluster_minkowsky'] = cluster_minkowsky
    session['centroid_awal'] = np.array(centroid).tolist()
    session['centroid_akhir_euclidean'] = np.array(centroid_akhir_euclidean).tolist()
    session['centroid_akhir_manhattan'] = np.array(centroid_akhir_manhattan).tolist()
    session['centroid_akhir_minkowsky'] = np.array(centroid_akhir_minkowsky).tolist()

    return jsonify(
        euclidean = cluster_euclidean, 
        manhattan = cluster_manhattan, 
        minkowsky = cluster_minkowsky)

@app.route('/cluster/sample/kmedoids')
def cluster_sample_kmedoids():
    jumlah_cluster = 6
    threshold = 6
    centroid_awal = kmedoids.defineCentroid(dataset.sampledata, jumlah_cluster)
    hasil_euclidean = kmedoids.kmedoids(dataset.sampledata, jumlah_cluster, 'euclidean', threshold, centroid_awal)
    hasil_manhattan = kmedoids.kmedoids(dataset.sampledata, jumlah_cluster, 'manhattan', 20, centroid_awal)
    hasil_minkowsky = kmedoids.kmedoids(dataset.sampledata, jumlah_cluster, 'minkowsky', 20, centroid_awal)

    session['sample_kmedoids_euclidean'] = hasil_euclidean
    session['sample_kmedoids_manhattan'] = hasil_manhattan
    session['sample_kmedoids_minkowsky'] = hasil_minkowsky

    return jsonify(
        euclidean = hasil_euclidean,
        manhattan = hasil_manhattan,
        minkowsky = hasil_minkowsky
    )
            

@app.route('/plot/sample/kmedoids')
def plot_sample_kmedoids():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = dataset.sampledata[:,0]
    ys = dataset.sampledata[:,1]

    color = ['red', 'green', 'blue', 'orange', 'cyan', 'violet']

    for i in range(len(xs)):
        if request.args.get('distance') == 'euclidean':
            axis.scatter(xs[i], ys[i], color = color[session['sample_kmedoids_euclidean']['cluster_baru'][i]])
        elif request.args.get('distance') == 'manhattan':          
            axis.scatter(xs[i], ys[i], color = color[session['sample_kmedoids_manhattan']['cluster_baru'][i]]) 
        elif request.args.get('distance') == 'minkowsky':         
            axis.scatter(xs[i], ys[i], color = color[session['sample_kmedoids_minkowsky']['cluster_baru'][i]])                     
    axis.grid()
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/cluster_kasus')
def kasus():
    kcluster = 4
    cluster_euclidean = []
    centroid = kmedian.centroidAwal(dataset.dataset, kcluster)
    centroid_akhir_euclidean = []
    temp_centroid_akhir = centroid

    # k-median dengan euclidean
    while np.array_equal(temp_centroid_akhir, centroid_akhir_euclidean) == False:
        centroid_akhir_euclidean = temp_centroid_akhir
        cluster_euclidean = kmedian.clustering(centroid_akhir_euclidean, dataset.dataset)
        temp_centroid_akhir = kmedian.cari_centroid_baru(dataset.dataset, cluster_euclidean, kcluster)
    
    # k-median dengan manhattan
    temp_centroid_akhir = centroid
    centroid_akhir_manhattan = []
    cluster_manhattan = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_manhattan) == False:
        centroid_akhir_manhattan = temp_centroid_akhir
        cluster_manhattan = kmedian.clustering(centroid_akhir_manhattan, dataset.dataset, 'manhattan')
        temp_centroid_akhir = kmedian.cari_centroid_baru(dataset.dataset, cluster_manhattan, kcluster)
    
    # k-median dengan minkowsky
    temp_centroid_akhir = centroid
    centroid_akhir_minkowsky = []
    cluster_minkowsky = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_minkowsky) == False:
        centroid_akhir_minkowsky = temp_centroid_akhir
        cluster_minkowsky = kmedian.clustering(centroid_akhir_minkowsky, dataset.dataset, 'minkowsky')
        temp_centroid_akhir = kmedian.cari_centroid_baru(dataset.dataset, cluster_minkowsky, kcluster)
    
    session['cluster_euclidean'] = cluster_euclidean
    session['cluster_manhattan'] = cluster_manhattan
    session['cluster_minkowsky'] = cluster_minkowsky
    session['centroid_awal'] = np.array(centroid).tolist()
    session['centroid_akhir_euclidean'] = np.array(centroid_akhir_euclidean).tolist()
    session['centroid_akhir_manhattan'] = np.array(centroid_akhir_manhattan).tolist()
    session['centroid_akhir_minkowsky'] = np.array(centroid_akhir_minkowsky).tolist()

    return jsonify(
        euclidean = cluster_euclidean, 
        manhattan = cluster_manhattan, 
        minkowsky = cluster_minkowsky)

if __name__ == '__main__':
    app.secret_key = 'clustering'
    app.run(debug=True)