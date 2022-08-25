import csv
from os.path import exists as file_exists
from datetime import datetime

AQ_CSV_PATH = 'data/aq_readings.csv'
CSV_HEADERS = ['date', 'time', 'temp', 'humidity', 'co2', 'voc']

class CsvReaderWriter:

    def __init__(self):
        pass

    def start_write(self, avg_sensor_dict):
        if not file_exists(AQ_CSV_PATH):
            file = open(AQ_CSV_PATH, 'w')
            self.create_file(file)
        else:
            file = open(AQ_CSV_PATH, 'a')
        self.open_file(file, avg_sensor_dict)
        file.close()

    def create_file(self, file):
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)

    def open_file(self, file, avg_sensor_dict):
        writer = csv.DictWriter(file, CSV_HEADERS)
        datetime_dict = self.get_now()
        avg_sensor_dict.update(datetime_dict)
        writer.writerow(avg_sensor_dict)


    def get_now(self):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
        return {"date": date, "time": time}        

        
