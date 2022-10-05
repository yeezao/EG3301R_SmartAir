import os
import time
import paho.mqtt.client as mqtt
import program_constants as pc
import json


client1 = mqtt.Client(client_id="sim_sensor_1")
client2 = mqtt.Client(client_id="sim_sensor_2")
client1.connect(pc.BROKER_IP, pc.MQTT_PORT)
client1.loop_start()
client2.connect(pc.BROKER_IP, pc.MQTT_PORT)
client2.loop_start()

while True:
    client1.publish(pc.MQTT_TOPIC_SUB, json.dumps({"id": 1, "Temp": 25, "Humidity": 80, "CO2":600,"TVOC":10}))
    time.sleep(0.1)
    client2.publish(pc.MQTT_TOPIC_SUB, json.dumps({"id": 2, "Temp": 27, "Humidity": 60, "CO2":1000,"TVOC":11}))
    print("complete 1 round")
    time.sleep(2)
