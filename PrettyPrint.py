import time

FILTER = "filter"
RELAY_1 = "relay1"
RELAY_2 = "relay2"

@staticmethod
def print_sensor_data(sensor_dict):
    print("The following data was received from the sensor:")
    i = 0
    for indiv_sensor_dict in sensor_dict.values():
        print("Sensor No. ", i)
        print("Temperature: ", indiv_sensor_dict["Temp"])
        print("Humidity: ", indiv_sensor_dict["Humidity"])
        print("CO2: ", indiv_sensor_dict["CO2"])
        print("VOC: ", indiv_sensor_dict["TVOC"])
        print("\n")

@staticmethod
def print_action_data_fan(action_dict):
    print("Exhaust Fan turning: ", "OFF" if action_dict[RELAY_1] < 0 else "ON")

@staticmethod
def print_action_data_filter(action_dict):
    print("Air Purifier turning: ", "OFF" if action_dict[FILTER] < 0 else "ON")

@staticmethod
def setup_message():
    print("Welcome to SmartAir!")
    time.sleep(2)
    print("Setting up now, one moment please...")

@staticmethod
def setup_complete():
    print("Setup Complete. Starting data collection now...")