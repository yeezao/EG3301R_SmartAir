import os
import time

while True:
    os.system('mosquitto_pub -h 192.168.229.101 -t sensordata -m "{"id": 1, "Temp": 25, "Humidity": 80, "CO2":600,"TVOC":10}"')
    time.sleep(0.1)
    os.system('mosquitto_pub -h 192.168.229.101 -t sensordata -m "{"id": 2, "Temp": 27, "Humidity": 60, "CO2":1000,"TVOC":11}"')
    time.sleep(2)
