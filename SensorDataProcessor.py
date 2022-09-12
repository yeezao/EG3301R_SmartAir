from datetime import datetime
import logging
from CsvReaderWriter import CsvReaderWriter
import program_constants as pc

class SensorDataProcessor:

    def __init__(self):
        pass

    def process_data(self, sensor_dict_multipleperiods):
        action_dict = {pc.FILTER: 0, pc.RELAY_1: 0, pc.RELAY_2: 0}
        print(sensor_dict_multipleperiods)

        avg_dict = {}

        for record_time, sensor_dict_singletime in sensor_dict_multipleperiods.items():
            avg_dict[record_time] = self.append_and_find(sensor_dict_singletime, True)

        total_avg_dict = self.append_and_find(avg_dict, False)

        self.determine_action(action_dict, total_avg_dict)

        action_dict_csv = {"fan_action": action_dict[pc.RELAY_1], "filter_action": action_dict[pc.FILTER]}
        
        crw = CsvReaderWriter()
        crw.start_write({**total_avg_dict, **action_dict_csv})
        del crw

        action_dict["relay2"] = "test"
        return action_dict

    def append_and_find(self, dict, add_to_rebaseline):

        c02_list = []
        voc_list = []
        temp_list = []
        humidity_list = []
        
        for item in dict.values():
            c02_list.append(item["CO2"])
            voc_list.append(item["TVOC"])
            temp_list.append(item["Temp"])
            humidity_list.append(item["Humidity"])
        
        if pc.OPR_MODE == 1:
            return_co2 = self.avg_list(c02_list)
            return_voc = self.avg_list(voc_list)
            return_temp = self.avg_list(temp_list)
            return_humidity = self.avg_list(humidity_list)
        elif pc.OPR_MODE == 2:
            return_co2 = self.worst_case_list(c02_list)
            return_voc = self.worst_case_list(voc_list)
            return_temp = self.worst_case_list(temp_list)
            return_humidity = self.worst_case_list(humidity_list)

        # if add_to_rebaseline:
        #     pc.co2_values_rebaseline.append(return_co2)
        #     if (len(pc.co2_values_rebaseline) >= pc.NUM_OF_SENSORS * pc.REBASE_DURATION):
        #         pass

        return {"Temp": return_temp, "Humidity": return_humidity, "CO2": return_co2, "TVOC": return_voc}

    def determine_action(self, action_dict, avg_dict):
        if avg_dict["CO2"] >= pc.co2_upper_bound or avg_dict["TVOC"] > 2000:
            action_dict[pc.RELAY_1] = 1
        elif avg_dict["CO2"] <= pc.co2_lower_bound and avg_dict["TVOC"] < 1500:
            action_dict[pc.RELAY_1] = -1

        #if avg_dict["voc"] >= 3:
        #    action_dict[FILTER] = 3
        #elif avg_dict["voc"] >= :
        #    action_dict[FILTER] = 2
        if avg_dict["TVOC"] >= 1000:
            action_dict[pc.FILTER] = 1
        elif avg_dict["TVOC"] < 800:
            action_dict[pc.FILTER] = -1

    def avg_list(self, aqlist):
        return sum(aqlist) / len(aqlist)

    def worst_case_list(self, aqlist):
        return max(aqlist)
        


# time.sleep(1)
