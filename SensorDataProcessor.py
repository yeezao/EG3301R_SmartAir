from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE
import time

FILTER = "filter"
RELAY_1 = "relay1"
RELAY_2 = "relay2"

class SensorDataProcessor:

    global sensor_dict

    def __init__(self, sensor_dict):
        self.sensor_dict = sensor_dict
        pass

    def process_data():
        action_dict = {FILTER: 0, RELAY_1: 0, RELAY_2: 0}

        co2_value = sensor_dict["Sensor1"]["CO2"]
        if (co2_value) >= 400:
            action_dict[RELAY_1] = 1
        elif (co2_value) <= 300:
            action_dict[RELAY_1] = -1

        action_dict["filter"] = "test"
        action_dict["relay2"] = "test"
        return action_dict

# time.sleep(1)