import paho.mqtt.client as mqtt
import json
import time


def do_stuff():
    time.sleep(1)

'''Callback to print error if connection fails'''
def on_connect(client, ret):
    if ret != 0:
        print("Connection failed with error", ret)

'''Connect clients to broker'''
def connect_to_broker(client):
    client.on_connect = on_connect
    client.connect("pi")
    client.loop_start()
    while not client.is_connected:
        time.sleep(1)
    client.loop_end()


'''Initialise clients and begin connection'''
def setup():

    global client1, client2
    client1 = mqtt.Client("Sensor1")
    client2 = mqtt.Client("Sensor2")
    connect_to_broker(client1)
    connect_to_broker(client2)


def main():
    
    setup()

    while(1):
        do_stuff()
        




if __name__ == "__main__":
    main()