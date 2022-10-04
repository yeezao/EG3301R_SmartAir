from datetime import datetime
import logging
from CsvReaderWriter import CsvReaderWriter
import program_constants as pc
import program_global_variables as pgv

class SensorDataProcessor:

    def __init__(self):
        pass

    def process_data(self, sensor_dict_multipleperiods):
        action_dict = {pc.FILTER: 0, pc.RELAY_1: 0, pc.RELAY_2: 0}
        print(sensor_dict_multipleperiods)

        #self.rebase_co2_thresholds()
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
        pm1_list = []
        pm25_list = []
        pm10_list = []
        
        for item in dict.values():
            c02_list.append(item["CO2"])
            voc_list.append(item["TVOC"])
            temp_list.append(item["Temp"])
            humidity_list.append(item["Humidity"])
            pm1_list.append(item["PM1"])
            pm25_list.append(item["PM2.5"])
            pm10_list.append(item["PM10"])
        
        return_dic = {}

        return_dic["Temp"] = self.find_list_mode(c02_list)
        return_dic["TVOC"] = self.find_list_mode(voc_list)
        return_dic["Temp"] = self.find_list_mode(temp_list)
        return_dic["Humidity"] = self.find_list_mode(humidity_list)
        return_dic["PM1"] = self.find_list_mode(pm1_list)
        return_dic["PM2.5"] = self.find_list_mode(pm25_list)
        return_dic["PM10"] = self.find_list_mode(pm10_list)

        return return_dic

    def determine_action(self, action_dict, avg_dict):
        if avg_dict["CO2"] >= pgv.co2_upper_bound or avg_dict["TVOC"] > 2000:
            action_dict[pc.RELAY_1] = 1
        elif avg_dict["CO2"] <= pgv.co2_lower_bound and avg_dict["TVOC"] < 1500:
            action_dict[pc.RELAY_1] = -1

        #if avg_dict["voc"] >= 3:
        #    action_dict[FILTER] = 3
        #elif avg_dict["voc"] >= :
        #    action_dict[FILTER] = 2
        if avg_dict["TVOC"] >= 1000:
            action_dict[pc.FILTER] = 1
        elif avg_dict["TVOC"] < 800:
            action_dict[pc.FILTER] = -1

    def rebase_co2_thresholds(self):
        if (len(pgv.co2_values_rebaseline) == 0):
            return
        else:
            pgv.co2_upper_bound = self.avg_list(pgv.co2_values_rebaseline) + 700
            pgv.co2_lower_bound = pgv.co2_upper_bound * 0.8

    def find_list_mode(self, aqlist):
        if pgv.prog_mode == pgv.ProgMode.AVG_CASE:
            return self.avg_list(aqlist)
        if pgv.prog_mode == pgv.ProgMode.WORST_CASE:
            return self.worst_case_list(aqlist)

    def avg_list(self, aqlist):
        return sum(aqlist) / len(aqlist)

    def worst_case_list(self, aqlist):
        try:
            return max(aqlist)
        except:
            return 0


# time.sleep(1)
