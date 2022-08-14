import paho.mqtt.client as mqtt
import json
import time
from queue import Queue

MQTT_TOPIC_SUB = "sensordata"
MQTT_TOPIC_PUB = "action"
NUM_OF_SENSORS = 1

global client1, client2
sensor_dict = {}

# decode json string into objects and add to sensor_dictionary
def json_serialize_add(client, message):
    dic = json.loads(message)
    sensor_dict[client] = dic
    print(sensor_dict)

# subscribe broker to sensors topic
def subscribe_to_topic():
    client1.subscribe(MQTT_TOPIC_SUB)
    #client2.subscribe(MQTT_TOPIC_SUB)
    client1.on_message = on_sensor_message  
    #client2.on_message = on_sensor_message
    #client1.

# Connect clients to broker
def connect_to_broker(client):
    client.on_connect = on_connect
    print("Connecting to client ", client)
    client.connect("192.168.81.101", 1883)
    #client.loop_start()
    while not client.is_connected:
        time.sleep(1)
        print("Still attempting to connect to ", client)
    #client.loop_end()


# Initialise clients and begin connection
def setup():
    client1 = mqtt.Client("Sensor1")
    #client2 = mqtt.Client("Sensor2")
    connect_to_broker(client1)
    #connect_to_broker(client2)
    subscribe_to_topic()

def process_sensor_data():
    time.sleep(1)
    # TODO: process sensor data here

def main():
    
    setup()

    while(1):
        if (len(sensor_dict) == NUM_OF_SENSORS):
            print("All sensors have transmitted data - beginning processing")
            process_sensor_data()
        else:
            time.sleep(5)

    #client1.loop_forever()
    #client2.loop_forever()
        

if __name__ == "__main__":
    main()

# Callback for when broker receives a message from client
def on_sensor_message(client, userdata, message):
    print("raw binary data received: ", message)
    print("Message received from Sensor", str(message.payload.decode("utf-8")))
    json_serialize_add(client, message)

# Callback to print error if connection fails
def on_connect(client, ret):
    if ret != 0:
        print("Connection failed with error ", client, " - ", ret)
    else:
        client.loop_start()