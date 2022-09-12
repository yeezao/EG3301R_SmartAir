#Mode 1 is averaging, Mode 2 is worst-case
OPR_MODE = 2

FILTER = "filter"

# Using GPIO Pin 5 (29) for Relay 1 and GPIO Pin 6 (31) for Relay 2
RELAY_1 = "relay1"
RELAY_2 = "relay2"
RELAY_1_PIN = 29
RELAY_2_PIN = 31

TIMEBLOCK_PERIOD = 15 # 15sec block period between actions
REBASE_DURATION = 10

MQTT_TOPIC_SUB = "sensordata"
MQTT_TOPIC_PUB = "filter_action"
NUM_OF_SENSORS = 2
BROKER_IP = "192.168.31.149"
MQTT_PORT = 1883

LOG_FILEPATH = 'log/smartair_main.log'

AQ_CSV_PATH = 'data/aq_readings.csv'
CSV_HEADERS = ['date', 'time', 'id', 'Temp', 'Humidity', 'CO2', 'TVOC', 'fan_action', 'filter_action']

VOC_UPPER_BOUND = 1000
VOC_LOWER_BOUND = 800

co2_upper_bound = 1300
co2_lower_bound = 1050

co2_values_rebaseline = []
