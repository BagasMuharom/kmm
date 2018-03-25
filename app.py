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
            axis.scatter(xs[i], ys[i], color = color[session['cluster_euclidean']['cluster_baru'][i]])
            # axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')            
        elif request.args.get('distance') == 'manhattan':
            # centroid_akhir = np.array(session['centroid_akhir_manhattan'])            
            axis.scatter(xs[i], ys[i], color = color[session['cluster_manhattan']['cluster_baru'][i]])
            # axis.scatter(centroid_akhir[:,0],centroid_akhir[:,1], color = '#ff00ff')                        
        elif request.args.get('distance') == 'minkowsky':
            # centroid_akhir = np.array(session['centroid_akhir_minkowsky'])            
            axis.scatter(xs[i], ys[i], color = color[session['cluster_minkowsky']['cluster_baru'][i]])
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
    centroid = kmedian.centroidAwal(dataset.sampledata, kcluster)
    
    cluster_euclidean = kmedian.kmedian(dataset.sampledata, kcluster, centroid, 'euclidean')
    cluster_manhattan = kmedian.kmedian(dataset.sampledata, kcluster, centroid, 'manhattan')
    cluster_minkowsky = kmedian.kmedian(dataset.sampledata, kcluster, centroid, 'minkowsky')
    
    session['cluster_euclidean'] = cluster_euclidean
    session['cluster_manhattan'] = cluster_manhattan
    session['cluster_minkowsky'] = cluster_minkowsky

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

@app.route('/cluster_kasus/kmedian')
def kasus():
    kcluster = 4
    centroid = kmedian.centroidAwal(dataset.dataset, kcluster)
    
    cluster_euclidean = kmedian.kmedian(dataset.dataset, kcluster, centroid, 'euclidean')
    cluster_manhattan = kmedian.kmedian(dataset.dataset, kcluster, centroid, 'manhattan')
    cluster_minkowsky = kmedian.kmedian(dataset.dataset, kcluster, centroid, 'minkowsky')

    return jsonify(
        euclidean = cluster_euclidean, 
        manhattan = cluster_manhattan, 
        minkowsky = cluster_minkowsky)

@app.route('/cluster_kasus/kmedoids/euclidean')
def cluster_kasus_kmedoids():
    jumlah_cluster = 4
    threshold = 6
    centroid_awal = kmedoids.defineCentroid(dataset.dataset, jumlah_cluster)
    hasil_euclidean = kmedoids.kmedoids(dataset.dataset, jumlah_cluster, 'euclidean', threshold, centroid_awal)

    return jsonify(
        euclidean = hasil_euclidean
    )

@app.route('/cluster_kasus/kmedoids/manhattan')
def cluster_kasus_kmedoids_manhattan():
    jumlah_cluster = 4
    threshold = 6
    centroid_awal = kmedoids.defineCentroid(dataset.dataset, jumlah_cluster)
    hasil_manhattan = kmedoids.kmedoids(dataset.dataset, jumlah_cluster, 'manhattan', threshold, centroid_awal)

    return jsonify(
        manhattan = hasil_manhattan
    )

@app.route('/cluster_kasus/kmedoids/minkowsky')
def cluster_kasus_kmedoids_minkowsky():
    jumlah_cluster = 4
    threshold = 6
    centroid_awal = kmedoids.defineCentroid(dataset.dataset, jumlah_cluster)
    hasil_minkowsky = kmedoids.kmedoids(dataset.dataset, jumlah_cluster, 'minkowsky', threshold, centroid_awal)

    return jsonify(
        minkowsky = hasil_minkowsky
    )

if __name__ == '__main__':
    app.secret_key = 'clustering'
    app.run(debug=True)