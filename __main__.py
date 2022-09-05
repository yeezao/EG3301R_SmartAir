from datetime import date, datetime
import os
import logging
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish
import json
import time
from CsvReaderWriter import CsvReaderWriter
from SensorDataProcessor import SensorDataProcessor
import PrettyPrint
import RPi.GPIO as GPIO


MQTT_TOPIC_SUB = "sensordata"
MQTT_TOPIC_PUB = "filter_action"
NUM_OF_SENSORS = 3
BROKER_IP = "192.168.31.149"
MQTT_PORT = 1883

LOG_FILEPATH = 'log/smartair_main.log'

# client1 - Pi Client
# Using GPIO Pin 5 (29) for Relay 1 and GPIO Pin 6 (31) for Relay 2

FILTER = "filter"
RELAY_1 = "relay1"
RELAY_2 = "relay2"
RELAY_1_PIN = 29
RELAY_2_PIN = 31
TIMEBLOCK_PERIOD = 15 # 15sec block period between actions


sensor_dict = {}
action_dict = {}

# decode json string into objects and add to sensor_dictionary
def json_serialize_add(client, message):
    dic = json.loads(message)
    sensor_dict[client] = dic
    print("JSON message serialised into ", sensor_dict[client], " for client ", client)
    #print(sensor_dict)

# encode action data to json string
def json_deserialise(object):
    message = json.dumps(object)
    #logging.info("Object deserialised into JSON message ", message)
    return message

# subscribe broker to sensors topic
def subscribe_to_topic(client):
    client.subscribe(MQTT_TOPIC_SUB)
    #logging.info("Subscribed and callback linked to topic ", MQTT_TOPIC_SUB)

# Connect clients to broker
def connect_to_broker(client):
    client.on_connect = on_connect
    #logging.info("Connecting to broker at IP address ", BROKER_IP, " on port ", MQTT_PORT)
    client.connect(BROKER_IP, MQTT_PORT)
    client.loop_start()
    time.sleep(5)
    while not client.is_connected:
        time.sleep(1)
        #logging.warn("Still attempting to connect to broker ", BROKER_IP, " on port ", MQTT_PORT)
    #client.loop_end()
    #client.loop_start()

def setup_logger():
    os.makedirs(os.path.dirname(LOG_FILEPATH), exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, filename=LOG_FILEPATH)
    logging.info("Beginning Logging...")

# Initialise clients and begin connection
def setup():

    setup_logger()

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RELAY_1_PIN, GPIO.OUT)
    GPIO.setup(RELAY_2_PIN, GPIO.OUT)
    #logging.info("GPIO Pins setup complete")

    global client1
    client1 = mqtt.Client(client_id="pi_data_processor")
    #logging.info("MQTT Client instantiated, client object is ", client1)
    client1.on_message = on_sensor_message
    client1.on_publish = on_publish
    connect_to_broker(client1)

# Instantiates a SensorDataProcessor object and sends its output to publish actions
def process_sensor_data():
    sensor_data_processor = SensorDataProcessor()
    action_dict = sensor_data_processor.process_data(sensor_dict)
    #logging.info("action dict is ", action_dict)
    send_actions(action_dict)
    del sensor_data_processor

# Sends actions to GPIO and Arduino
def send_actions(action_dict):
    #print(action_dict)
    if (action_dict[FILTER] != 0):
        #logging.info("sending action ", action_dict[FILTER], " to Arduino")
        PrettyPrint.print_action_data_filter(action_dict)
        client1.publish(MQTT_TOPIC_PUB, json_deserialise({FILTER: action_dict[FILTER]}))
    if (action_dict[RELAY_1] != 0 or action_dict[RELAY_2] != 0):
        PrettyPrint.print_action_data_fan(action_dict)
        process_relay_action(action_dict)

# Sends actions to GPIO
def process_relay_action(action_dict):
    #logging.info("sending actions ", action_dict[RELAY_1], " ", action_dict[RELAY_2], " to GPIO Pins")
    if action_dict[RELAY_1] == 1:
        GPIO.output(RELAY_1_PIN, GPIO.HIGH)
    elif action_dict[RELAY_1] == -1:
        GPIO.output(RELAY_1_PIN, GPIO.LOW)

    if action_dict[RELAY_2] == 1:
        GPIO.output(RELAY_2_PIN, GPIO.HIGH)
    elif action_dict[RELAY_1] == -1:
        GPIO.output(RELAY_2_PIN, GPIO.LOW)

def has_timeblock_expired(timeblock_start):
    timeblock_end = datetime.now()
    duration = timeblock_end - timeblock_start
    print(duration.total_seconds())
    #logging.debug("Timeblock duration is now ", duration.total_seconds())
    if (duration.total_seconds() >= TIMEBLOCK_PERIOD):
        return True
    else:
        return False


def main():
    
    PrettyPrint.setup_message()
    setup()
    PrettyPrint.setup_complete()

    sensor_dict_multipleperiods = {}

    #data_in_processing = False
    timeblock_start = datetime.now()

    while(1):
        if (len(sensor_dict) == NUM_OF_SENSORS and has_timeblock_expired(timeblock_start)):
            logging.info("All sensors have transmitted data and timeblock has expired - beginning processing")
            #PrettyPrint.print_sensor_data(sensor_dict_multipleperiods)
            #data_in_processing = True
            process_sensor_data()
            sensor_dict = sensor_dict.copy()
            sensor_dict.clear()
            #logging.info("Sensor dict cleared")
            #data_in_processing = False
            timeblock_start = datetime.now()
        elif (len(sensor_dict) == NUM_OF_SENSORS):
            #logging.debug("All sensors have transmitted data, but timeblock has not expired - saving sensor data to csv")
            crw = CsvReaderWriter()
            PrettyPrint.print_sensor_data(sensor_dict)
            for sensor_dict_indiv in sensor_dict.values():
                #print(sensor_dict_indiv)
                crw.start_write(sensor_dict_indiv)   
            del crw
            sensor_dict_multipleperiods[datetime.now()] = sensor_dict
            sensor_dict = sensor_dict.copy()
            sensor_dict.clear()
        else:
            #logging.debug("Not all sensor data received, waiting to receive all data. Only ", len(sensor_dict), "sensors have transmitted")
            time.sleep(5)

# Callback for when broker receives a message from client
def on_sensor_message(client, userdata, message):
    #logging.debug("raw binary data received: ", message)
    #logging.info("JSON Message received from Sensor ", str(message.payload.decode("utf-8")))
    json_serialize_add(client, str(message.payload.decode("utf-8")))

# Callback to print error if connection fails
def on_connect(client, userdata, flags, ret):
    if ret != 0:
        pass
        #logging.error("Connection failed with error ", ret, " for ", client)
    else:
        subscribe_to_topic(client1)
        #logging.info("Connection Successful with message ", ret, "from client ", client)
        #client.loop_start()

# Callback after action is sent
def on_publish(client, userdata, result):
    pass

if __name__ == "__main__":
    main()
