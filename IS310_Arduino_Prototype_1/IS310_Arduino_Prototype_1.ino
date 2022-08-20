#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#include "DFRobot_CCS811.h"
#include <IRremote.h>
#include <dht11.h>
#include <DFRobot_DHT11.h>
#include <Arduino.h>
//dht11 DHT;
dht11 DHT;
DFRobot_CCS811 CCS811;

const char* wifi_ssid = "Redmi Note 9S_1993";
const char* wifi_pw = "password123";

const char* mqtt_broker_ip = "192.168.81.101";
const char* mqtt_pub_topic = "sensordata";
const char* mqtt_sub_topic = "filter_action"
const char* mqtt_clientid = "sensor";
const char* mqtt_port = 1883;

WiFiClient wificlient;
PubSubClient client(mqtt_broker_ip, 1883, wificlient);

#define DECODE_NEC
#define DHT11_PIN 2
const int RECV_PIN = 3;
IRrecv irrecv(RECV_PIN);
decode_results results;

void transmit_data(DFRobot_CCS811 CCS811) {

  String json = encode_json(CCS811);

  ret = client.publish(mqtt_pub_topic, json.c_str());
  if (!ret) {
    Serial.print("Sending failed.");
  }
}

String encode_json(DFRobot_CCS811 CCS811) {
  StaticJsonDocument<200> jsondoc;
  jsondoc["CO2"] = CCS811.getCO2PPM();
  jsondoc["TVOC"] = CCS811.getTVOCPPB();
  String output;
  serializeJson(jsondoc, output);
  Serial.print(output);
  return output;
}

int decode_json(byte* payload) {
  StaticJsonDocument<200> jsondoc;
  deserializeJson(jsonDoc, payload);
  Serial.print("The received filter action is ");
  Serial.println(jsondoc["filter"]);
  return jsondoc["filter"];  
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

      transmit_data(CCS811);

} else {
        Serial.println("Data is not ready!");
   }
    CCS811.writeBaseLine(0x447B);
    //delay cannot be less than measurement cycle
    delay(2000);
}

void on_mqtt_message(char* topic, byte* payload, unsigned int length) {
  int filter_action = decode_json(payload);
  send_ir(filter_action); 
}

void send_ir(int action) {
  
}

void setup_wifi_mqtt() {
  WiFi.begin(wifi_ssid, wifi_pw);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
  }
  Serial.println("Wifi Successfully connected");
  bool ret = client.connect(mqtt_clientid);
  delay(100);
  if (!ret) {
    Serial.print("Could not connect to MQTT broker.");
  }
  client.setServer(mqtt_broker_ip, mqtt_port);
  client.subscribe(mqtt_sub_topic);
  client.setCallback(on_mqtt_message);
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
    
    setup_wifi_mqtt();
}

void loop() {

  client.poll();
  
   if (IrReceiver.decode()) {
        Serial.println(results.value, HEX);
        IrReceiver.resume(); // Enable receiving of the next value
  }

  read_aq_data();
  
}
