import json
import random
import time
import paho.mqtt.client as mqtt

# Callback function for successful connection


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")

    # Subscribe to the "devices" topic
    client.subscribe("devices")

    # Start sending data after connection
    send_data(client)

# Callback function for handling incoming MQTT messages


def on_message(client, userdata, msg):
    print(
        f"Received data on topic '{msg.topic}': {msg.payload.decode('utf-8')}")

# Function to send random JSON data every 5 seconds


def send_data(client: mqtt.Client):
    while True:
        # Generate a random humidity value between 0 and 100
        humidity = random.uniform(0, 100)
        # Generate a random temperature value between -50 and 50
        temperature = random.uniform(-50, 50)

        data = {
            "humidity": humidity,
            "temperature": temperature,
            "name": "mock_device"
        }

        json_data = json.dumps(data)  # Convert the data to a JSON string

        # Publish the JSON string to the "data" channel
        client.publish("data_logs", json_data)
        print(f"Sent data: {json_data}")

        time.sleep(5)  # Wait for 5 seconds before sending the next data


# Configure MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Replace with your MQTT broker's IP address and port
mqtt_broker_ip = "localhost"
mqtt_broker_port = 1883

# Connect to the MQTT broker
client.connect(mqtt_broker_ip, mqtt_broker_port, 60)

# Start the MQTT loop
client.loop_forever()
