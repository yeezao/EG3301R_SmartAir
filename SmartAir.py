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

if "Linux" in platform.system():
    import RPi.GPIO as GPIO

sensor_dict = {}
action_dict = {}
sensor_dict_multipleperiods = {}

# decode json string into objects and add to sensor_dictionary
def json_serialize_add(client, message):
    dic = json_serialize(message)
    sensor_dict[dic["id"]] = dic
    logging.debug("JSON message serialised into %s for client %s", message, sensor_dict[dic["id"]])
    print(sensor_dict)

def json_serialize(message):
    return json.loads(message)

# encode action data to json string
def json_deserialise(object):
    message = json.dumps(object)
    logging.debug("Object deserialised into JSON message %s", message)
    return message

# subscribe broker to sensors topic
def subscribe_to_topic(client):
    client.subscribe(pc.MQTT_TOPIC_SUB)
    client.subscribe(pc.MQTT_TOPIC_SUB_CO2_AMB)
    logging.info("Subscribed and callback linked to topic %s and %s", pc.MQTT_TOPIC_SUB, pc.MQTT_TOPIC_SUB_CO2_AMB)

# Connect clients to broker
def connect_to_broker(client):
    client.on_connect = on_connect
    logging.info("Attempting to connect to broker at IP address %s on port %i", pc.BROKER_IP, pc.MQTT_PORT)
    try:
        client.connect(pc.BROKER_IP, pc.MQTT_PORT)
    except:
        print("Fatal Error - could not connect to MQTT Broker at %s on port %i", pc.BROKER_IP, pc.MQTT_PORT)
        logging.critical("Fatal Error - could not connect to MQTT Broker at %s on port %i", pc.BROKER_IP, pc.MQTT_PORT)
    client.loop_start()
    time.sleep(5)
    while not client.is_connected:
        time.sleep(1)
    #client.loop_end()
    #client.loop_start()

def setup_logger():
    os.makedirs(os.path.dirname(pc.LOG_FILEPATH), exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, filename=pc.LOG_FILEPATH, format="%(asctime)s - %(name)s - %(levelname)8s - %(message)s")
    logging.info("Logger setup completed, beginning Logging...")

def check_os_for_log():
    if "Linux" not in platform.system():
        logging.warning("Currently running on %s - all GPIO functionailty will be disabled", platform.system())

# Initialise clients and begin connection
def setup():

    PrettyPrint.setup_message()
    setup_logger()
    check_os_for_log()

    if "Linux" in platform.system():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pc.RELAY_1_PIN, GPIO.OUT)
        GPIO.setup(pc.RELAY_2_PIN, GPIO.OUT)
        # logging.info("GPIO Pins setup complete")
    else:
        logging.warning("GPIO Pins setup skipped - RPi.GPIO requires Linux but program is being run on %s", platform.system())
        pass

    global client1
    client1 = mqtt.Client(client_id="pi_data_processor")
    logging.info("MQTT Client instantiated, client object is %s", str(client1))
    client1.on_message = on_sensor_message
    client1.on_publish = on_publish
    connect_to_broker(client1)

    PrettyPrint.setup_complete()

# Instantiates a SensorDataProcessor object and sends its output to publish actions
def process_sensor_data():
    sensor_data_processor = SensorDataProcessor()
    action_dict = sensor_data_processor.process_data(sensor_dict_multipleperiods)
    logging.info("action dict is %s", str(action_dict))
    send_actions(action_dict)
    del sensor_data_processor

# Sends actions to GPIO and Arduino
def send_actions(action_dict):
    #print(action_dict)
    if (action_dict[pc.FILTER] != 0):
        logging.info("sending filter action %s to Arduino(s)", action_dict[pc.FILTER])
        PrettyPrint.print_action_data_filter(action_dict)
        client1.publish(pc.MQTT_TOPIC_PUB_FILTER, json_deserialise({pc.FILTER: action_dict[pc.FILTER]}))
    if (action_dict[pc.RELAY_1] != 0 or action_dict[pc.RELAY_2] != 0):
        PrettyPrint.print_action_data_fan(action_dict)
        logging.info("sending fan action %s to Arduino(s)", action_dict[pc.RELAY_1])
        client1.publish(pc.MQTT_TOPIC_PUB_FAN, json_deserialise({pc.RELAY_1: action_dict[pc.RELAY_1]}))
        # if "Linux" in platform.system():
        #     process_relay_action(action_dict)
        # else:
        #     logging.warning("No actions sent to GPIO - RPi.GPIO requires Linux but program is being run on %s ", platform.system())
        #     pass

# DEPRECATED Sends actions to GPIO
def process_relay_action(action_dict):
    logging.info("sending actions %i %i to GPIO Pins", action_dict[pc.RELAY_1], action_dict[pc.RELAY_2])
    if action_dict[pc.RELAY_1] == 1:
        GPIO.output(pc.RELAY_1_PIN, GPIO.HIGH)
    elif action_dict[pc.RELAY_1] == -1:
        GPIO.output(pc.RELAY_1_PIN, GPIO.LOW)

    if action_dict[pc.RELAY_2] == 1:
        GPIO.output(pc.RELAY_2_PIN, GPIO.HIGH)
    elif action_dict[pc.RELAY_1] == -1:
        GPIO.output(pc.RELAY_2_PIN, GPIO.LOW)

def has_timeblock_expired(timeblock_start):
    timeblock_end = datetime.now()
    duration = timeblock_end - timeblock_start
    print(duration.total_seconds())
    logging.debug("Timeblock duration is now %f", duration.total_seconds())
    if (duration.total_seconds() >= pc.TIMEBLOCK_PERIOD):
        return True
    else:
        return False

def write_to_csv(): 
    crw = CsvReaderWriter()
    PrettyPrint.print_sensor_data(sensor_dict)
    for sensor_dict_indiv in sensor_dict.values():
        #print(sensor_dict_indiv)
        crw.start_write(sensor_dict_indiv)   
    del crw

def main():
    
    setup()    
    timeblock_start = datetime.now()

    while(1):
        if (len(sensor_dict) == pc.NUM_OF_SENSORS and has_timeblock_expired(timeblock_start)):
            logging.info("All sensors have transmitted data and timeblock has expired - beginning processing")
            #PrettyPrint.print_sensor_data(sensor_dict_multipleperiods)
            write_to_csv()
            process_sensor_data()
            sensor_dict.clear()
            sensor_dict_multipleperiods.clear()
            logging.info("sensor_dict and sensor_dict_multipleperiods cleared")
            timeblock_start = datetime.now()
        elif (len(sensor_dict) == pc.NUM_OF_SENSORS):
            logging.debug("All sensors have transmitted data, but timeblock has not expired - saving sensor data to csv")
            write_to_csv()
            sensor_dict_multipleperiods[datetime.now()] = sensor_dict.copy()
            print(sensor_dict_multipleperiods)
            sensor_dict.clear()
        else:
            logging.debug("Not all sensor data received, waiting to receive all data. Only %i sensors have transmitted", len(sensor_dict))
            # print("Not all sensor data received, waiting to receive all data. Only ", len(sensor_dict), "sensors have transmitted")
            time.sleep(5)

# Callback for when broker receives a message from client
def on_sensor_message(client, userdata, message):
    logging.debug("raw binary data received: %s", str(message))
    logging.info("JSON Message received from Sensor: %s ", str(message.payload.decode("utf-8")))
    add_co2_amb = True if message.topic == pc.MQTT_TOPIC_SUB_CO2_AMB else False       
    if (add_co2_amb): # for outdoor ambient CO2 sensor
        dic = json_serialize(str(message.payload.decode("utf-8")))
        pgv.co2_values_rebaseline.append(dic["CO2"])
    else: # for indoor data sensors
        json_serialize_add(client, str(message.payload.decode("utf-8")))        

# Callback to print error if connection fails
def on_connect(client, userdata, flags, ret):
    if ret != 0:
        pass
        logging.critical("Connection failed with error %i for %s", ret, str(client))
    else:
        subscribe_to_topic(client1)
        logging.info("Connection Successful with message %i from client %s", ret, str(client))
        #client.loop_start()

# Callback after action is sent
def on_publish(client, userdata, result):
    pass

if __name__ == "__main__":
    main()
