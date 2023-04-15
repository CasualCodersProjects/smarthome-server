# This file seems a little complete. Definitely needs cleaned up.

import paho.mqtt.client as client
import json
import pymongo
import arrow

# Database Information and Config
DATABASE_ADDRESS = "mongodb://localhost:27017/"         # Database IP Address
DATABASE_NAME = "smarthome"                             # Database Name
DATABASE_COLLECTION = "data_logs"                       # Collection Name

# MQTT Information and config
MQTT_HOST = "localhost"                                 # MQTT Broker's IP
MQTT_PORT = 1883                                        # MQTT broker's port
# MQTT_TOPIC = "config"         # This will need to change, still a little nebulous. Need many topics likely.

# Configure Database Structure
mongo_database = pymongo.MongoClient(DATABASE_ADDRESS)
mongo_db = mongo_database[DATABASE_NAME]
mongo_collection = mongo_db[DATABASE_COLLECTION]

# MQTT Callback for 
def mqtt_log_callback (client, userdata, msg):
        # Extract log data from the MQTT Announcement
        log_data = json.loads(msg.payload)
        print(log_data)
        
        # Adding a mongoDB supported timestamp through Arrow
        log_data["timestamp"] = arrow.utcnow().isoformat()
        
        # Data inserted into database collection.
        mongo_collection.insert_one(log_data)

# Define the MQTT Client
mqtt_client = client.Client()

# Callback to handle datalog
mqtt_client.on_message = mqtt_log_callback

# MQTT Connection
mqtt_client.connect(MQTT_HOST, MQTT_PORT)

# MQTT Topic Subscription. Again, this will need to change depending on final network structure.
mqtt_client.subscribe("test")

# Loop forever
mqtt_client.loop_forever()