import paho.mqtt.client as mqtt
import json
import time
import RPi.GPIO as GPIO

from SensorDataProcessor import SensorDataProcessor

MQTT_TOPIC_SUB = "sensordata"
MQTT_TOPIC_PUB = "filter_action"
NUM_OF_SENSORS = 1
BROKER_IP = "192.168.81.101"
MQTT_PORT = 1883


# Using GPIO Pin 5 (29) for Relay 1 and GPIO Pin 6 (31) for Relay 2

FILTER = "filter"
RELAY_1 = "relay1"
RELAY_2 = "relay2"
RELAY_1_PIN = 29
RELAY_2_PIN = 31


global client1  #client with sensor and IR blaster
global client2  #client with sensor and relay
sensor_dict = {}
action_dict = {}

# decode json string into objects and add to sensor_dictionary
def json_serialize_add(client, message):
    print("JSON message is ", message)
    dic = json.loads(message)
    sensor_dict[client] = dic
    print(sensor_dict)


# encode action data to json string
def json_deserialise(object):
    return json.dumps(object)

# subscribe broker to sensors topic
def subscribe_to_topic(client):
    client.subscribe(MQTT_TOPIC_SUB)
    print("subscribed and callback linked")

# Connect clients to broker
def connect_to_broker(client):
    client.on_connect = on_connect
    print("Connecting to client ", client)
    client.connect(BROKER_IP, MQTT_PORT)
    client.loop_start()
    time.sleep(5)
    while not client.is_connected:
        time.sleep(1)
        print("Still attempting to connect to ", client)
    print("conn success")
    #client.loop_end()
    #client.loop_start()

# Initialise clients and begin connection
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RELAY_1_PIN, GPIO.OUT)
    GPIO.setup(RELAY_2_PIN, GPIO.OUT)

    global client1
    client1 = mqtt.Client(client_id="pi_data_processor")
    client1.on_message = on_sensor_message
    client1.on_publish = on_publish
    connect_to_broker(client1)

def process_sensor_data():
    sensor_data_processor = SensorDataProcessor()
    action_dict = sensor_data_processor.process_data(sensor_dict)
    send_actions(action_dict)

def send_actions(action_dict):
    print(action_dict)
    if (action_dict[FILTER]):
        print("sending action ", action_dict[FILTER], " to Arduino")
        client1.publish(MQTT_TOPIC_PUB, json_deserialise({FILTER: action_dict[FILTER]}))
    if (action_dict[RELAY_1] or action_dict[RELAY_2]):
        process_relay_action(action_dict)

def process_relay_action(action_dict):
    print("sending actions ", action_dict[RELAY_1], " ", action_dict[RELAY_2], " to GPIO Pins")
    if action_dict[RELAY_1] == 1:
        GPIO.output(RELAY_1_PIN, GPIO.HIGH)
    elif action_dict[RELAY_1] == -1:
        GPIO.output(RELAY_1_PIN, GPIO.LOW)

    if action_dict[RELAY_2] == 1:
        GPIO.output(RELAY_2_PIN, GPIO.HIGH)
    elif action_dict[RELAY_1] == -1:
        GPIO.output(RELAY_2_PIN, GPIO.LOW)

def main():
    
    setup()

    global data_in_processing
    data_in_processing = False

    while(1):
        print(len(sensor_dict))
        if (len(sensor_dict) == NUM_OF_SENSORS):
            print("All sensors have transmitted data - beginning processing") 
            data_in_processing = True
            process_sensor_data()
            time.sleep(2)
            sensor_dict.clear()
            print("Sensor dict cleared")
            data_in_processing = False
        else:
            print("Not all sensor data received")
            #GPIO.output(RELAY_1_PIN, GPIO.HIGH)
            time.sleep(4)
            #GPIO.output(RELAY_1_PIN, GPIO.LOW)
            time.sleep(4)

# Callback for when broker receives a message from client
def on_sensor_message(client, userdata, message):
    print("raw binary data received: ", message)
    print("Message received from Sensor", str(message.payload.decode("utf-8")))
    json_serialize_add(client, str(message.payload.decode("utf-8")))

# Callback to print error if connection fails
def on_connect(client, userdata, flags, ret):
    if ret != 0:
        print("Connection failed with error ", client, " - ", ret)
    else:
        subscribe_to_topic(client1)
        print("Connection Successful with message ", ret, "from client ", client)
        #client.loop_start()

# Callback after action is sent
def on_publish(client, userdata, result):
    print("Action sent. Result of sending is ", result)

if __name__ == "__main__":
    main()
