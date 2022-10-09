from datetime import date, datetime
import os
import logging
import paho.mqtt.client as mqtt
import json
import time
from CsvReaderWriter import CsvReaderWriter
from SensorDataProcessor import SensorDataProcessor
import PrettyPrint
import platform
import program_constants as pc
import program_global_variables as pgv


def json_deserialise(object):
    message = json.dumps(object)
    #logging.debug("Object deserialised into JSON message %s", message)
    return message

def send_filter():
    
    while True:
        print("turning on now")
        client1.publish(pc.MQTT_TOPIC_PUB_FILTER, json_deserialise({pc.FILTER: 1}))
        time.sleep(5)
        print("turning off now")
        client1.publish(pc.MQTT_TOPIC_PUB_FILTER, json_deserialise({pc.FILTER: -1}))
        time.sleep(5)


def connect_to_broker(client):
    #client.on_connect = on_connect
    logging.info("Attempting to connect to broker at IP address %s on port %i", pc.BROKER_IP, pc.MQTT_PORT)
    try:
        client.connect(pc.BROKER_IP, pc.MQTT_PORT)
    except:
        print("Fatal Error - could not connect to MQTT Broker at %s on port %i", pc.BROKER_IP, pc.MQTT_PORT)
        #logging.critical("Fatal Error - could not connect to MQTT Broker at %s on port %i", pc.BROKER_IP, pc.MQTT_PORT)
    client.loop_start()
    time.sleep(5)
    while not client.is_connected:
        time.sleep(1)


def setup():

    global client1
    client1 = mqtt.Client(client_id="pi_data_processor")
    logging.info("MQTT Client instantiated, client object is %s", str(client1))
    #client1.on_message = on_sensor_message
    #client1.on_publish = on_publish
    connect_to_broker(client1)
    PrettyPrint.setup_complete()



setup()
send_filter()
