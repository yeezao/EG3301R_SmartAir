import logging
import csv
from os.path import exists as file_exists
import os
from datetime import datetime
import program_constants as pc


class CsvReaderWriter:

    def __init__(self):
        pass

    def start_write(self, dict):
        logging.debug("starting write for ", dict)
        if not file_exists(pc.AQ_CSV_PATH):
            os.makedirs(os.path.dirname(pc.AQ_CSV_PATH), exist_ok=True)
            file = open(pc.AQ_CSV_PATH, 'a')
            self.create_file(file)
        else:
            file = open(pc.AQ_CSV_PATH, 'a')
        self.open_file(file, dict)
        file.close()

    def create_file(self, file):
        writer = csv.writer(file)
        writer.writerow(pc.CSV_HEADERS)

    def open_file(self, file, dict):
        writer = csv.DictWriter(file, pc.CSV_HEADERS)
        datetime_dict = self.get_now()
        writer.writerow({**dict, **datetime_dict})

    def get_now(self):
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        return {"date": date, "time": time}        

        
