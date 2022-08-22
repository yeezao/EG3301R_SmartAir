import time

FILTER = "filter"
RELAY_1 = "relay1"
RELAY_2 = "relay2"

class SensorDataProcessor:

    def __init__(self):
        pass

    def process_data(self, sensor_dict):
        action_dict = {FILTER: 0, RELAY_1: 0, RELAY_2: 0}

        co2_value = sensor_dict["Sensor1"]["CO2"]
        voc_value = sensor_dict["Sensor1"]["TVOC"]

        if co2_value >= 400:
            action_dict[RELAY_1] = 1
        elif co2_value <= 300:
            action_dict[RELAY_1] = -1

        if voc_value >= 100:
            action_dict[FILTER] = 3
        elif voc_value >= 75:
            action_dict[FILTER] = 2
        elif voc_value >= 50:
            action_dict[FILTER] = 1


        action_dict["relay2"] = "test"
        return action_dict

# time.sleep(1)
