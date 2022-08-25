import time

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

        for client_obj, sensor_indiv_dict in sensor_dict.items():
            temp_dict = sensor_indiv_dict
            c02_list.append(sensor_indiv_dict["CO2"])
            voc_list.append(sensor_indiv_dict["TVOC"])

        avg_c02 = self.avg_list(c02_list)
        avg_voc = self.avg_list(voc_list)

        if avg_c02 >= 1300:
            action_dict[RELAY_1] = 1
        elif avg_c02 <= 600:
            action_dict[RELAY_1] = -1

        if avg_voc >= 3:
            action_dict[FILTER] = 3
        elif avg_voc >= 2:
            action_dict[FILTER] = 2
        elif avg_voc >= 1:
            action_dict[FILTER] = 1


        action_dict["relay2"] = "test"
        print(action_dict)
        return action_dict

    def avg_list(self, aqlist):
        return sum(aqlist) / len(aqlist)
        


# time.sleep(1)
