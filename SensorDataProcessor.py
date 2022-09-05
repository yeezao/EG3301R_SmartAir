import logging
from CsvReaderWriter import CsvReaderWriter

FILTER = "filter"
RELAY_1 = "relay1"
RELAY_2 = "relay2"

class SensorDataProcessor:

    def __init__(self):
        pass

    def process_data(self, sensor_dict):
        action_dict = {FILTER: 0, RELAY_1: 0, RELAY_2: 0}

        c02_list = []
        voc_list = []
        temp_list = []
        humidity_list = []

        for client_obj, sensor_indiv_dict in sensor_dict.items():
            c02_list.append(sensor_indiv_dict["CO2"])
            voc_list.append(sensor_indiv_dict["TVOC"])
            temp_list.append(sensor_indiv_dict["Temp"])
            humidity_list.append(sensor_indiv_dict["Humidity"])

        avg_c02 = self.avg_list(c02_list)
        avg_voc = self.avg_list(voc_list)
        avg_temp = self.avg_list(temp_list)
        avg_humidity = self.avg_list(humidity_list)
        avg_dict = {"Temp": avg_temp, "Humidity": avg_humidity, "CO2": avg_c02, "TVOC": avg_voc}

        self.determine_action(action_dict, avg_dict)

        action_dict_csv = {"fan_action": action_dict[RELAY_1], "filter_action": action_dict[FILTER]}
        
        crw = CsvReaderWriter()
        crw.start_write({**avg_dict, **action_dict_csv})
        del crw

        action_dict["relay2"] = "test"
        return action_dict

    def determine_action(self, action_dict, avg_dict):
        if avg_dict["CO2"] >= 1300 or avg_dict["TVOC"] > 2000:
            action_dict[RELAY_1] = 1
        elif avg_dict["CO2"] <= 1050 and avg_dict["TVOC"] < 1500:
            action_dict[RELAY_1] = -1

        #if avg_dict["voc"] >= 3:
        #    action_dict[FILTER] = 3
        #elif avg_dict["voc"] >= :
        #    action_dict[FILTER] = 2
        if avg_dict["TVOC"] >= 1000:
            action_dict[FILTER] = 1
        elif avg_dict["TVOC"] < 800:
            action_dict[FILTER] = -1

    def avg_list(self, aqlist):
        return sum(aqlist) / len(aqlist)
        


# time.sleep(1)
