#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <WiFi.h>

const char* wifi_ssid = "Xiaomi_ED47";
const char* wifi_pw = "Lyz1999/2";

const char* mqtt_broker_ip = "192.168.31.149";
const char* mqtt_sub_topic = "fan_action";
//const char* mqtt_clientid = "fan_esp_1";
const char* mqtt_port = 1883;

unsigned long start = 0;
unsigned long start_reset = 0;

WiFiClient wificlient;
PubSubClient client(mqtt_broker_ip, 1883, wificlient);

const int RELAY_PIN = 26;

void setup_wifi() {
  WiFi.disconnect();
  WiFi.begin(wifi_ssid, wifi_pw);
  delay(1000);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("connecting to wifi...");
    delay(1000);
    WiFi.disconnect();
    WiFi.begin(wifi_ssid, wifi_pw);
  }
  Serial.println("Wifi Successfully connected");
}

void setup_mqtt() {
  bool ret = client.connect();
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

int decode_json(byte* payload) {
  StaticJsonDocument<200> jsondoc;
  deserializeJson(jsondoc, payload);
  Serial.print("The received fan action is ");
  Serial.println(jsondoc["relay1"].as<int>());
  return jsondoc["relay1"].as<int>();  
}

void on_mqtt_message(char* topic, byte* payload, unsigned int length) {
  Serial.println("Message Received");
  int fan_action = decode_json(payload);
  send_relay_action(fan_action); 
}

void send_relay_action(int fan_action) {
  if (fan_action == 1) {
    relayOn()
  } else if (fan_action == -1) {
    relayOff()
  }

}

void relayOn() {
    digitalWrite(RELAY_PIN, LOW);
}

void relayOff() {
    digitalWrite(RELAY_PIN, HIGH);
}

void setup() {
    pinMode(RELAY_PIN, OUTPUT);
    setup_wifi();
    setup_mqtt();
}

void loop() {
  client.loop();
}
