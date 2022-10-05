#include <Seeed_HM330X.h>
#include "Air_Quality_Sensor.h"
#include <Adafruit_SCD30.h>
#include <IRremote.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <IRremote.h>
#include <Arduino.h>

const char* wifi_ssid = "Xiaomi_ED47";
const char* wifi_pw = "Lyz1999/2";

const char* mqtt_broker_ip = "192.168.31.149";
const char* mqtt_pub_topic = "sensordata";
const char* mqtt_sub_topic = "filter_action";
const char* mqtt_clientid = "sensor_3";
const char* mqtt_port = 1883;

unsigned long start = 0;
unsigned long start_reset = 0;

WiFiClient wificlient;
PubSubClient client(mqtt_broker_ip, 1883, wificlient);

#define DECODE_NEC
//#define 
#define RECV_PIN 3
#define IR_TX_PIN 13
#define GROVE_PIN A0

#define SENSOR_DELAY 10000

#define IR_ON_OFF 0xFD02FF00
#define IR_CHANGE_SPEED 0xF609FF00
#define IR_CHANGE_TIMER 0xF708FF00
#define IR_RESET 0xFF00FF00

#define FILTER_OFF 0
#define FILTER_SPEED_1 1
#define FILTER_SPEED_2 2
#define FILTER_SPEED_3 3

int filter_state = FILTER_OFF;

IRrecv irrecv(RECV_PIN);
decode_results results;

Adafruit_SCD30 scd30;
AirQualitySensor grove_aq(A0);
HM330X grove_pm;

uint8_t buf[30];
const char* str[] = {"sensor num: ", "PM1.0 concentration(CF=1,Standard particulate matter,unit:ug/m3): ",
                     "PM2.5 concentration(CF=1,Standard particulate matter,unit:ug/m3): ",
                     "PM10 concentration(CF=1,Standard particulate matter,unit:ug/m3): ",
                     "PM1.0 concentration(Atmospheric environment,unit:ug/m3): ",
                     "PM2.5 concentration(Atmospheric environment,unit:ug/m3): ",
                     "PM10 concentration(Atmospheric environment,unit:ug/m3): ",
                    };


struct pmData {
  int pm1;
  int pm25;
  int pm10;
} pmDataInstance;
uint8_t pmDataArray[3];

void transmit_data() {

  String json = encode_json();
  int ret = client.publish(mqtt_pub_topic, json.c_str());
  delay(500);
  Serial.println(ret);
  while (!ret) {
    Serial.print("Sending failed.");
    setup_wifi();
    setup_mqtt();
    ret = client.publish(mqtt_pub_topic, json.c_str());
    Serial.println(ret);
  }
}

String encode_json() {
  StaticJsonDocument<200> jsondoc;
  jsondoc["id"] = "5";
  jsondoc["CO2"] = scd30.CO2;
  jsondoc["TVOC"] = grove_aq.getValue();
  jsondoc["Humidity"] = scd30.relative_humidity;
  jsondoc["Temp"] = scd30.temperature;
  jsondoc["PM1"] = pmDataArray[0];
  jsondoc["PM2.5"] = pmDataArray[1];
  jsondoc["PM10"] = pmDataArray[2];
  String output;
  serializeJson(jsondoc, output);
  //Serial.print(output);
  return output;
}

int decode_json(byte* payload) {
  StaticJsonDocument<200> jsondoc;
  deserializeJson(jsondoc, payload);
  Serial.print("The received filter action is ");
  Serial.println(jsondoc["filter"].as<int>());
  return jsondoc["filter"].as<int>();  
}

/*parse buf with 29 uint8_t-data*/
HM330XErrorCode parse_result(uint8_t* data) {
    uint16_t value = 0;
    if (NULL == data) {
        return ERROR_PARAM;
    }
    for (int i = 5; i < 8; i++) {
        value = (uint16_t) data[i * 2] << 8 | data[i * 2 + 1];
        pmDataArray[i - 5] = value;
        print_result(str[i - 5], value);

    }

    return NO_ERROR;
}

HM330XErrorCode parse_result_value(uint8_t* data) {
    if (NULL == data) {
        return ERROR_PARAM;
    }
    for (int i = 0; i < 28; i++) {
        Serial.print(data[i], HEX);
        Serial.print("  ");
        if ((0 == (i) % 5) || (0 == i)) {
            Serial.println("");
        }
    }
    uint8_t sum = 0;
    for (int i = 0; i < 28; i++) {
        sum += data[i];
    }
    if (sum != data[28]) {
        Serial.println("wrong checkSum!!");
    }
    Serial.println("");
    return NO_ERROR;
}

HM330XErrorCode print_result(const char* str, uint16_t value) {
    if (NULL == str) {
        return ERROR_PARAM;
    }
    Serial.print(str);
    Serial.println(value);
    return NO_ERROR;
}

void read_aq_data() {

    if (scd30.dataReady()) {
    
      if (!scd30.read()){ 
        Serial.println("Error reading sensor data"); 
        return; 
      }
  
      Serial.print("Temperature: ");
      Serial.print(scd30.temperature);
      Serial.println(" degrees C");
      
      Serial.print("Relative Humidity: ");
      Serial.print(scd30.relative_humidity);
      Serial.println(" %");
      
      Serial.print("CO2: ");
      Serial.print(scd30.CO2, 3);
      Serial.println(" ppm");
      Serial.println("");
    }

    int voc_value = grove_aq.getValue();
    Serial.print("VOC is: ");
    Serial.println(voc_value);

    if (grove_pm.read_sensor_value(buf, 29)) {
        Serial.println("HM330X read result failed!!");
    }
    parse_result_value(buf);
    parse_result(buf);
    transmit_data();
    
}

void on_mqtt_message(char* topic, byte* payload, unsigned int length) {
  Serial.println("Message Received");
  int filter_action = decode_json(payload);
  send_ir(filter_action); 
}

void send_ir(int action) {
  if (action > 0 && filter_state <= FILTER_OFF) {
    Serial.println("Turning filter ON");
    IrSender.sendNEC(0xAF51, 0x8, true, 0);
    filter_state = action;
  } else if (action <= FILTER_OFF) {
    Serial.println("Turning filter OFF");
    IrSender.sendNEC(0xAF51, 0x0, true, 0);
    filter_state = action;
  }
}

void setup_wifi() {
 WiFi.disconnect();
 WiFi.begin(wifi_ssid, wifi_pw);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("connecting to wifi...");
    delay(1000);
    WiFi.disconnect();
    WiFi.begin(wifi_ssid, wifi_pw);
  }
  Serial.println("Wifi Successfully connected");
}

void setup_mqtt() {
  bool ret = client.connect(mqtt_clientid);
  delay(1000);
  if (!ret) {
    Serial.print("Could not connect to MQTT broker.");
    setup_wifi();
  }
  client.setServer(mqtt_broker_ip, mqtt_port);
  client.subscribe(mqtt_sub_topic);
  client.setCallback(on_mqtt_message);
  Serial.println("mqtt connected and subscribed");
}


void setup(void)
{
    Serial.begin(111111);

    delay(500);
    
    while (grove_pm.init()) {
      Serial.println("Re-init grove_pm");
      delay(1000);
    }
    Serial.println("grove_pm init successful");
    delay(1000);
    while (!grove_aq.init()) {
      Serial.println("Re-init grove_aq");
      delay(1000);
    }
    Serial.println("grove_aq init successful");
    delay(1000);

    /*Wait for the chip to be initialized completely, and then exit*/
    irrecv.enableIRIn();
    irrecv.blink13(true);

    if (!scd30.begin()) {
      Serial.println("Failed to find SCD30 chip");
      while (1) { delay(10); }
    }
    Serial.println("SCD30 Found!");
    Serial.print("Measurement Interval: "); 
    Serial.print(scd30.getMeasurementInterval()); 
    Serial.println(" seconds");
    //scd30.forceRecalibrationWithReference(630);

    delay(100);

    setup_wifi();
    setup_mqtt();
    IrSender.begin(IR_TX_PIN);

    delay(1000);
    
}

void loop() {

  client.loop();
  
  /*
  if (IrReceiver.decode()) {
        Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
        IrReceiver.resume(); // Enable receiving of the next value
  }
  */

  if (millis() - start >= 2000) {
    Serial.print("starting sensor reads");
    read_aq_data();
    start = millis();
  }

}
