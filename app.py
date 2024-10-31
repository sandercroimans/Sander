from flask import Flask, render_template, jsonify
from paho.mqtt import client as mqtt_client
import time

app = Flask(__name__)

# MQTT settings
mqttBroker = "fcbe9d6b471d4f2fbf6f6d269817368e.s1.eu.hivemq.cloud"
mqttPort = 8883
mqttUser = "Sander"
mqttPassword = "ScHc?!2004"
topic = "football/match/#"

events = []
time_info = ""

# Callback for when a message is received
def on_message(client, userdata, message):
    global events, time_info
    msg = message.payload.decode()
    if message.topic == "football/match/time":
        time_info = msg  # Stel time_info in op het ontvangen bericht



    # Voor elk ontvangen bericht, voeg het toe aan de events lijst
    events.append(f" {msg}")

# Connect and subscribe to the MQTT broker
def connect_mqtt():
    client = mqtt_client.Client()
    client.username_pw_set(mqttUser, mqttPassword)
    client.tls_set()
    client.connect(mqttBroker, mqttPort)
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_start()
    return client

mqtt_client = connect_mqtt()

@app.route('/')
def index():
    return render_template('index.html', events=events, time_info=time_info)

@app.route('/data')
def data():
    return jsonify(time_info=time_info, events=events)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)



