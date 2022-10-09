# DEPRECATED: Mode 1 is averaging, Mode 2 is worst-case
OPR_MODE = 2

FILTER = "filter"

# Using GPIO Pin 5 (29) for Relay 1 and GPIO Pin 6 (31) for Relay 2
RELAY_1 = "relay1"
RELAY_2 = "relay2"
RELAY_1_PIN = 7
RELAY_2_PIN = 13
RELAY_3_PIN = 15

TIMEBLOCK_PERIOD = 30 # 15sec block period between actions
REBASE_DURATION = 10

MQTT_TOPIC_SUB = "sensordata"
MQTT_TOPIC_SUB_CO2_AMB = "co2_ambient"
MQTT_TOPIC_PUB_FILTER = "filter_action"
MQTT_TOPIC_PUB_FAN = "fan_action"
NUM_OF_SENSORS = 1
BROKER_IP = "192.168.31.149"
MQTT_PORT = 1883

LOG_FILEPATH = 'log/smartair_main.log'

AQ_CSV_PATH = 'data/aq_readings.csv'
CSV_HEADERS = ['date', 'time', 'id', 'Temp', 'Humidity', 'CO2', 'TVOC', 'PM1', 'PM2.5', 'PM10', 'fan_action', 'filter_action']

VOC_UPPER_BOUND = 1000
VOC_LOWER_BOUND = 800
