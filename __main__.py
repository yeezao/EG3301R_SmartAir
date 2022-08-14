import paho.mqtt.client as mqtt
import json
import time

import SensorDataProcessor

BROKER_IP = "192.168.81.101"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "sensordata"
MQTT_TOPIC_PUB = "action"
NUM_OF_SENSORS = 1

data_in_processing = False;

# global client1  #client with sensor and IR blaster
# global client2  #client with sensor and relay
sensor_dict = {}
action_dict = {}

# decode json string into objects and add to sensor_dictionary
def json_serialize_add(client, message):
    dic = json.loads(message)
    sensor_dict[client] = dic
    print(sensor_dict)

# encode action data to json string
def json_deserialise(object):
    pass

# subscribe broker to sensors topic
def subscribe_to_topic(client):
    client.subscribe(MQTT_TOPIC_SUB)
    client.on_message = on_sensor_message
    client.on_publish = on_publish

# Connect clients to broker
def connect_to_broker(client):
    client.on_connect = on_connect
    print("Connecting to client ", client)
    client.connect(BROKER_IP, MQTT_PORT)
    #client.loop_start()
    time.sleep(5)
    while not client.is_connected:
        time.sleep(1)
        print("Still attempting to connect to ", client)
    print("conn success")
    #client.loop_end()


# Initialise clients and begin connection
def setup():
    global client1
    client1 = mqtt.Client("Sensor1")
    #client2 = mqtt.Client("Sensor2")
    connect_to_broker(client1)
    #connect_to_broker(client2)
    subscribe_to_topic(client1)

#
def process_sensor_data():
    sensor_data_processor = SensorDataProcessor(sensor_dict)
    action_dict = sensor_data_processor.process_data()
    send_actions(action_dict)

def send_actions(action_dict):
    if (action_dict["filter"]):
        client1.publish("action", action_dict["filter"])
    if (action_dict["relay1"]):
        pass
    if (action_dict["relay2"]):
        pass

# Callback for when broker receives a message from client
def on_sensor_message(client, userdata, message):
    print("raw binary data received: ", message)
    print("Message received from Sensor", str(message.payload.decode("utf-8")))
    json_serialize_add(client, message)

# Callback after action is sent
def on_publish(client, userdata, result):
    print("Action sent. Result of sending is ", result)


# Callback to print error if connection fails
def on_connect(client, ret):
    if ret != 0:
        print("Connection failed with error ", client, " - ", ret)
    else:
        print("Connection Successful with message ", ret, "from client ", client)
        client.loop_start()

def main():

    setup()

    while(1):
        if (len(sensor_dict) == NUM_OF_SENSORS and data_in_processing == False):
            print("All sensors have transmitted data - beginning processing")
            process_sensor_data()
            data_in_processing = True
        elif (data_in_processing == True):
            print("Data is currently being processed...")
        else:
            print("Not all sensor data received")
            time.sleep(5)

    #client1.loop_forever()
    #client2.loop_forever()

if __name__ == "__main__":
    main()