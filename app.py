from flask import Flask,render_template,jsonify
from pyshark import LiveCapture
import json


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
    capture.sniff(packet_count=10)
    packet_protocols = {}
    packets = []
    for packet in capture:
        packets.append(packet)
        packet_protocols[packet.transport_layer] = packet_protocols.get(packet.transport_layer, 0) + 1
    
    min_time = packets[0].sniff_timestamp
    max_time = packets[-1].sniff_timestamp

    seconds = max_time - min_time

    protocols = []
    for protocol in packet_protocols:
        protocols.append({'protocol': protocol, 'value': packet_protocols[protocol]})
    return render_template('dashboard.html', data=[], protocols=json.dumps(protocols), packets=packets)


@app.route("/team")
def team():
    return render_template('team.html') 


@app.route("/article")
def article():
    return render_template('article.html') 
 

if __name__ == '__main__':
  app.run(debug=False)