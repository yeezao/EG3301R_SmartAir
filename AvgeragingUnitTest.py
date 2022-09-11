from audioop import avg
from datetime import datetime
import re
import time
import unittest
from SensorDataProcessor import SensorDataProcessor

class TestAvgeraging(unittest.TestCase):

    def test_single_avg(self):

        sensor_dict = {}
        sensor_dict[1] = {"id": 1, "Temp": 25, "Humidity": 80, "CO2": 600, "TVOC": 10}
        sensor_dict[2] = {"id": 1, "Temp": 24, "Humidity": 81, "CO2": 500, "TVOC": 5}
        sensor_dict[3] = {"id": 1, "Temp": 26, "Humidity": 79, "CO2": 700, "TVOC": 15}
    
        sdp = SensorDataProcessor()
        return_dict = sdp.append_and_find(sensor_dict)
        self.assertEqual(return_dict["Temp"], 25)
        self.assertEqual(return_dict["Humidity"], 80)
        self.assertEqual(return_dict["CO2"], 600)
        self.assertEqual(return_dict["TVOC"], 10)


    def test_multiple_avg(self):

        sensor_dict_multipleperiods = {}
        sensor_dict = {}
        avg_dict = {}

        #expected avgs: 24, 79, 700, 15
        sensor_dict[1] = {"id": 1, "Temp": 22, "Humidity": 77, "CO2": 900, "TVOC": 25}
        sensor_dict[2] = {"id": 1, "Temp": 24, "Humidity": 81, "CO2": 500, "TVOC": 5}
        sensor_dict[3] = {"id": 1, "Temp": 26, "Humidity": 79, "CO2": 700, "TVOC": 15}

        print(datetime.now())
        sensor_dict_multipleperiods[datetime.now()] = sensor_dict
        time.sleep(1)       
        sensor_dict = sensor_dict.copy()

        #expected avgs: 22, 80, 700, 30
        sensor_dict[1] = {"id": 1, "Temp": 20, "Humidity": 80, "CO2": 700, "TVOC": 30}
        sensor_dict[2] = {"id": 1, "Temp": 22, "Humidity": 80, "CO2": 700, "TVOC": 30}
        sensor_dict[3] = {"id": 1, "Temp": 24, "Humidity": 80, "CO2": 700, "TVOC": 30}   

        print(datetime.now())
        sensor_dict_multipleperiods[datetime.now()] = sensor_dict
        time.sleep(1)   
        sensor_dict = sensor_dict.copy()

        #expected avgs: 20, 81, 1000, 45
        sensor_dict[1] = {"id": 1, "Temp": 20, "Humidity": 81, "CO2": 500, "TVOC": 0}
        sensor_dict[2] = {"id": 1, "Temp": 0, "Humidity": 91, "CO2": 1000, "TVOC": 45}
        sensor_dict[3] = {"id": 1, "Temp": 40, "Humidity": 71, "CO2": 1500, "TVOC": 90}   

        print(datetime.now())
        sensor_dict_multipleperiods[datetime.now()] = sensor_dict
        time.sleep(1)    
        sensor_dict = sensor_dict.copy()

        sdp = SensorDataProcessor()

        for record_time, sensor_dict_singletime in sensor_dict_multipleperiods.items():
            avg_dict[record_time] = sdp.append_and_find(sensor_dict_singletime)
            print(avg_dict[record_time])

        total_avg_dict = sdp.append_and_find(avg_dict)

        #expected final avgs: 22, 81, 800, 30
        self.assertEqual(total_avg_dict["Temp"], 22)
        self.assertEqual(total_avg_dict["Humidity"], 80)
        self.assertEqual(total_avg_dict["CO2"], 800)
        self.assertEqual(total_avg_dict["TVOC"], 30)


if __name__ == '__main__':
    unittest.main()