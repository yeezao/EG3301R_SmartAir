FILTER = "filter"
RELAY_1 = "relay1"
RELAY_2 = "relay2"
RELAY_1_PIN = 29
RELAY_2_PIN = 31
TIMEBLOCK_PERIOD = 15 # 15sec block period between actions

MQTT_TOPIC_SUB = "sensordata"
MQTT_TOPIC_PUB = "filter_action"
NUM_OF_SENSORS = 3
BROKER_IP = "192.168.31.149"
MQTT_PORT = 1883

LOG_FILEPATH = 'log/smartair_main.log'

AQ_CSV_PATH = 'data/aq_readings.csv'
CSV_HEADERS = ['date', 'time', 'Temp', 'Humidity', 'CO2', 'TVOC', 'fan_action', 'filter_action']