# This file seems a little complete. Definitely needs cleaned up.

import paho.mqtt.client as client
import json
import pymongo
import arrow


database = pymongo.MongoClient('mongodb://localhost:27017/')
db = database["mydatabase"]
collection = db["mycollection"]

# Set up the connection parameters
mqtt_host = "localhost"  # Replace with your MQTT broker's IP address or hostname
mqtt_port = 1883  # Replace with your MQTT broker's port
mqtt_topic = "test"  # Replace with your MQTT topic

def clientcb (client, userdata, msg):
        data = json.loads(msg.payload)
        print(data)
        data["timestamp"] = arrow.utcnow().isoformat()
        collection.insert_one(data)

client = client.Client()
client.on_message = clientcb

client.connect(mqtt_host, mqtt_port)
client.subscribe(mqtt_topic)
client.loop_forever()