import time
import program_constants as pc

def print_sensor_data(sensor_dict):
    print("The following data was received from the sensor:")
    i = 1
    for indiv_sensor_dict in sensor_dict.values():
        print("Sensor No. ", i)
        print("Temperature: ", indiv_sensor_dict["Temp"])
        print("Humidity: ", indiv_sensor_dict["Humidity"])
        print("CO2: ", indiv_sensor_dict["CO2"])
        print("VOC: ", indiv_sensor_dict["TVOC"])
        print("\n")
        i += 1 

def print_action_data_fan(action_dict):
    print("Exhaust Fan turning: ", "OFF" if action_dict[pc.RELAY_1] < 0 else "ON")

def print_action_data_filter(action_dict):
    print("Air Purifier turning: ", "OFF" if action_dict[pc.FILTER] < 0 else "ON")

def setup_message():
    print("Welcome to SmartAir!")
    time.sleep(2)
    print("Setting up now, one moment please...")

def setup_complete():
    print("Setup Complete. Starting data collection now...")
    print("\n")
