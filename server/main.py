import paho.mqtt.client as client
import json
import pymongo
import arrow


database = pymongo.MongoClient('mongodb://localhost:27017/')
db = database["default"]
collection = db["data"]

# Set up the connection parameters
mqtt_host = "localhost"  # Replace with your MQTT broker's IP address or hostname
mqtt_port = 1883  # Replace with your MQTT broker's port
mqtt_topic = "data"  # Replace with your MQTT topic


def clientcb(client, userdata, msg):
    data = json.loads(msg.payload)
    print(data)
    data["timestamp"] = arrow.utcnow().isoformat().replace("+00:00", "Z")
    collection.insert_one(data)


client = client.Client()
client.on_message = clientcb

client.connect(mqtt_host, mqtt_port)
client.subscribe(mqtt_topic)
client.loop_forever()

# down here there should be code to
# watch the database for changes in the devices collection
# by default it should send a json object to the device
# with the key "state" followed by the device's state and the name of the device
# for a simple light that should just be true or false (on or off)
# for more complex devices this can be an object

# for example:
# {
#   "state": true,
#   "name": "light"
# }
# see the gdoc for more info
