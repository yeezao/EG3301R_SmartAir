#include <IRremote.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#include "DFRobot_CCS811.h"
#include <IRremote.h>
#include <dht11.h>
#include <DFRobot_DHT11.h>
#include <Arduino.h>
dht11 DHT;
//dht11 DHT;
DFRobot_CCS811 CCS811;

const char* wifi_ssid = "Xiaomi_ED47";
const char* wifi_pw = "Lyz1999/2";

const char* mqtt_broker_ip = "192.168.31.149";
const char* mqtt_pub_topic = "sensordata";
const char* mqtt_sub_topic = "filter_action";
const char* mqtt_clientid = "sensor";
const char* mqtt_port = 1883;

unsigned long start = 0;

WiFiClient wificlient;
PubSubClient client(mqtt_broker_ip, 1883, wificlient);

#define DECODE_NEC
#define DHT11_PIN 12
#define RECV_PIN 3
#define IR_TX_PIN 13

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


void transmit_data(DFRobot_CCS811 CCS811, dht11 DHT) {

  String json = encode_json(CCS811, DHT);
  int ret = client.publish(mqtt_pub_topic, json.c_str());
  Serial.println(ret);
  if (!ret) {
    Serial.print("Sending failed.");
    setup_wifi();
    setup_mqtt();
    int ret = client.publish(mqtt_pub_topic, json.c_str());
    Serial.println(ret);
  }
}

String encode_json(DFRobot_CCS811 CCS811, dht11 DHT11) {
  StaticJsonDocument<200> jsondoc;
  jsondoc["CO2"] = CCS811.getCO2PPM();
  jsondoc["TVOC"] = CCS811.getTVOCPPB();
  jsondoc["Humidity"] = DHT11.humidity;
  jsondoc["Temp"] = DHT11.temperature-2;
  String output;
  serializeJson(jsondoc, output);
  Serial.print(output);
  return output;
}

int decode_json(byte* payload) {
  StaticJsonDocument<200> jsondoc;
  deserializeJson(jsondoc, payload);
  Serial.print("The received filter action is ");
  Serial.println(jsondoc["filter"].as<int>());
  return jsondoc["filter"].as<int>();  
}

void read_aq_data() {
  int chk;
  Serial.print("DHT11: ");
  
  chk = DHT.read(DHT11_PIN);    // READ DATA
  switch (chk){
    case DHTLIB_OK:
                Serial.print("OK,\t");
                break;
    case DHTLIB_ERROR_CHECKSUM:
                Serial.print("Checksum error,\t");
                break;
    case DHTLIB_ERROR_TIMEOUT:
                Serial.print("Time out error,\t");
                break;
    default:
                Serial.print("Unknown error,\t");
                break;
  }
  
  // DISPLAY DATA
  
  Serial.print("Humidity: ");
  Serial.print(DHT.humidity,1);
  Serial.print(",\t");
  Serial.print("Temperature: ");
  Serial.println(DHT.temperature-2,1); // Zero temperature data
  
  
  if(CCS811.checkDataReady() == true){
      Serial.print("CO2: ");
      Serial.print(CCS811.getCO2PPM());
      Serial.print("ppm, TVOC: ");
      Serial.print(CCS811.getTVOCPPB());
      Serial.println("ppb");

      transmit_data(CCS811, DHT);

} else {
        Serial.println("Data is not ready!");
   }
    CCS811.writeBaseLine(0x447B);
    //delay cannot be less than measurement cycle
    delay(2000);
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
//  WiFi.disconnect();
//  WiFi.begin(wifi_ssid, wifi_pw);
  while (WiFi.status() != WL_CONNECTED) {
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
    /*Wait for the chip to be initialized completely, and then exit*/
    irrecv.enableIRIn();
    irrecv.blink13(true);
    while(CCS811.begin() != 0){
        Serial.println("failed to init chip, please check if the chip connection is fine");
        delay(1000);
    }
    
    setup_wifi();
    setup_mqtt();
    IrSender.begin(IR_TX_PIN);
}

void loop() {

  client.loop();
  
   if (IrReceiver.decode()) {
        Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
        IrReceiver.resume(); // Enable receiving of the next value
  }

  if (millis() - start >= 1000) {
    Serial.print("starting sensor reads");
    read_aq_data();
    start = millis();
  }
  
}
