import json
import os

import arrow
import paho.mqtt.client as mqtt
import pymongo

# mongodb connection info
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "default")

# Set up the connection parameters
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_DATA_TOPIC = os.getenv("MQTT_DATA_TOPIC", "data_logs")
MQTT_DEVICES_TOPIC = os.getenv("MQTT_DEVICES_TOPIC", "devices")

database = pymongo.MongoClient(MONGO_URI)
db = database[MONGO_DB]
data_collection = db["data"]
devices_collection = db["devices"]


def on_message(client, userdata, msg):
    '''Callback for when a message is received'''
    data = json.loads(msg.payload)
    print(data)
    data["timestamp"] = arrow.utcnow().isoformat().replace("+00:00", "Z")
    data_collection.insert_one(data)
    # check to see if the device is in the
    device = devices_collection.find_one({"name": data["name"]})
    if device is None:
        # add the device to the database
        devices_collection.insert_one({
            "name": data["name"],
            "display_name": data["name"],
            "state": None,
            "description": "A device",
            "updated_at": arrow.utcnow().isoformat().replace("+00:00", "Z"),
        })


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_DATA_TOPIC)

mqtt_client.loop_start()


def device_list_to_dict(devices):
    data = {}
    for device in devices:
        data[device["name"]] = device
    return data


devices = {}
last_device_update = 0

# change stream is not implemented for ferretdb, so we'll just have to poll
try:
    while True:
        if arrow.now().timestamp() - last_device_update > 1:
            d = devices_collection.find()
            new_devices = device_list_to_dict(d)
            # check for changes in the existing devices
            for device in devices:
                if devices[device]['state'] != new_devices[device]['state']:
                    print(f"Device {device} changed state")
                    # push the new state to the device
                    mqtt_client.publish(json.dumps(new_devices[device]))
            devices = new_devices
            last_device_update = arrow.now().timestamp()

except KeyboardInterrupt:
    print("Exiting...")

mqtt_client.loop_stop()
