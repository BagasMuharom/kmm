from flask import Flask, make_response, render_template, jsonify, session, request, json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import io
import clustering
import numpy as np

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', datasets = clustering.sampledata, datasetskasus = clustering.dataset)

@app.route('/plot')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = clustering.sampledata[:,0]
    ys = clustering.sampledata[:,1]

    color = ['red', 'green', 'blue', 'orange']

    for i in range(len(xs)):
        if request.args.get('distance') == 'euclidean':
            centroid_akhir = np.array(session['centroid_akhir_euclidean'])
            axis.scatter(xs[i], ys[i], color = color[session['cluster_euclidean'][i]])
            axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')            
        elif request.args.get('distance') == 'manhattan':
            centroid_akhir = np.array(session['centroid_akhir_manhattan'])            
            axis.scatter(xs[i], ys[i], color = color[session['cluster_manhattan'][i]])
            axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')                        
        elif request.args.get('distance') == 'minkowsky':
            centroid_akhir = np.array(session['centroid_akhir_minkowsky'])            
            axis.scatter(xs[i], ys[i], color = color[session['cluster_minkowsky'][i]])
            axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')                        
            
    centroid_awal = np.array(session['centroid_awal'])
    axis.scatter(centroid_awal[:,0],centroid_awal[:,1], color = 'black')

    axis.grid()
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/cluster_umum')
def cluster_umum():
    kcluster = 4
    cluster_euclidean = []
    centroid = clustering.centroidAwal(clustering.sampledata, kcluster)
    centroid_akhir_euclidean = []
    temp_centroid_akhir = centroid

    # k-median dengan euclidean
    while np.array_equal(temp_centroid_akhir, centroid_akhir_euclidean) == False:
        centroid_akhir_euclidean = temp_centroid_akhir
        cluster_euclidean = clustering.clustering(centroid_akhir_euclidean, clustering.sampledata)
        temp_centroid_akhir = clustering.cari_centroid_baru(clustering.sampledata, cluster_euclidean, kcluster)
    
    # k-median dengan manhattan
    temp_centroid_akhir = centroid
    centroid_akhir_manhattan = []
    cluster_manhattan = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_manhattan) == False:
        centroid_akhir_manhattan = temp_centroid_akhir
        cluster_manhattan = clustering.clustering(centroid_akhir_manhattan, clustering.sampledata, 'manhattan')
        temp_centroid_akhir = clustering.cari_centroid_baru(clustering.sampledata, cluster_manhattan, kcluster)
    
    # k-median dengan minkowsky
    temp_centroid_akhir = centroid
    centroid_akhir_minkowsky = []
    cluster_minkowsky = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_minkowsky) == False:
        centroid_akhir_minkowsky = temp_centroid_akhir
        cluster_minkowsky = clustering.clustering(centroid_akhir_minkowsky, clustering.sampledata, 'minkowsky')
        temp_centroid_akhir = clustering.cari_centroid_baru(clustering.sampledata, cluster_minkowsky, kcluster)
    
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

@app.route('/cluster_kasus')
def kasus():
    kcluster = 4
    cluster_euclidean = []
    centroid = clustering.centroidAwal(clustering.dataset, kcluster)
    centroid_akhir_euclidean = []
    temp_centroid_akhir = centroid

    # k-median dengan euclidean
    while np.array_equal(temp_centroid_akhir, centroid_akhir_euclidean) == False:
        centroid_akhir_euclidean = temp_centroid_akhir
        cluster_euclidean = clustering.clustering(centroid_akhir_euclidean, clustering.dataset)
        temp_centroid_akhir = clustering.cari_centroid_baru(clustering.dataset, cluster_euclidean, kcluster)
    
    # k-median dengan manhattan
    temp_centroid_akhir = centroid
    centroid_akhir_manhattan = []
    cluster_manhattan = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_manhattan) == False:
        centroid_akhir_manhattan = temp_centroid_akhir
        cluster_manhattan = clustering.clustering(centroid_akhir_manhattan, clustering.dataset, 'manhattan')
        temp_centroid_akhir = clustering.cari_centroid_baru(clustering.dataset, cluster_manhattan, kcluster)
    
    # k-median dengan minkowsky
    temp_centroid_akhir = centroid
    centroid_akhir_minkowsky = []
    cluster_minkowsky = []
    while np.array_equal(temp_centroid_akhir, centroid_akhir_minkowsky) == False:
        centroid_akhir_minkowsky = temp_centroid_akhir
        cluster_minkowsky = clustering.clustering(centroid_akhir_minkowsky, clustering.dataset, 'minkowsky')
        temp_centroid_akhir = clustering.cari_centroid_baru(clustering.dataset, cluster_minkowsky, kcluster)
    
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