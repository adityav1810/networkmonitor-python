from flask import Flask,render_template,jsonify
from pyshark import LiveCapture
import json
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLO WORLD'
app.config['NETWORK_INTERFACE'] = 'wlo1'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/dashboard")
def dashboard():
    capture = LiveCapture(interface=app.config['NETWORK_INTERFACE'])
    capture.sniff(packet_count=100)
    packet_protocols = {}
    packets = []

    packet_sizes = []

    for packet in capture:
        try:
            assert packet.ip
            packets.append(packet)
            packet_protocols[packet.highest_layer] = packet_protocols.get(packet.highest_layer, 0) + 1
            packet_sizes.append(int(packet.length))
        except:
            pass
    packet_size_bin = [0, 100, 250, 500, 1000]

    packet_sizes = np.array(packet_sizes)
    packet_size_bins = np.array(packet_size_bin)

    packet_sizes_indexes = np.digitize(packet_sizes, packet_size_bins)
    packet_size_bin.append('1000+')
    colors = ["#552586", "#6A359C", "#804FB3", "#9969C7", "#B589D6"]

    packet_size_counts = {}

    unique, counts = np.unique(packet_sizes_indexes, return_counts=True)
    packet_bin_counts = dict(zip(unique, counts))
    packet_sizes_final = []
    for index, count in enumerate(packet_bin_counts):
        packet_sizes_final.append({'label': f'{packet_size_bin[count-1]}-{packet_size_bin[count]} bytes', 'value': int(packet_bin_counts[count]), 'color': colors[index]})
    
    #print(packet_sizes, packet_sizes_final)

    min_time = int(packets[0].sniff_timestamp.split('.')[0])
    max_time = int(packets[-1].sniff_timestamp.split('.')[0]) + 1

    run_time_seconds = max_time - min_time

    time_based_array = [{'count': x, 'value': 0} for x in range(run_time_seconds)]
    ip_based_array = [set() for x in range(run_time_seconds)]

    for packet in packets:
        try:
            packet_time = int(packet.sniff_timestamp.split('.')[0])
            seconds_delta = packet_time - min_time
            time_based_array[seconds_delta]['value'] += 1
            ip_based_array[seconds_delta].add(packet.ip.dst)
        except:
            pass

    ip_based_array = [{'count': x, 'value': len(a)} for x, a in enumerate(ip_based_array)]

    #print(ip_based_array)
    #print(time_based_array)
    
    protocols = []
    for protocol in packet_protocols:
        protocols.append({'protocol': protocol, 'value': packet_protocols[protocol]})
    
    #print(protocols)
    #print(packet_sizes_final)
    return render_template('dashboard.html', data=[], protocols=json.dumps(protocols), time_based_array=json.dumps(time_based_array), ip_based_array=json.dumps(ip_based_array), packet_sizes=json.dumps(packet_sizes_final), packets=packets)


@app.route("/team")
def team():
    return render_template('team.html') 


@app.route("/article")
def article():
    return render_template('article.html') 
 

if __name__ == '__main__':
  app.run(debug=False)