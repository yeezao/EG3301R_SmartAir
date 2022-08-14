#include "DFRobot_CCS811.h"
#include <IRremote.h>
#include <dht11.h>
#include <Arduino.h>
dht11 DHT;
DFRobot_CCS811 CCS811;

#define DECODE_NEC
#define DHT11_PIN 2
const int RECV_PIN = 3;
IRrecv irrecv(RECV_PIN);
decode_results results;

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
}

void loop() {
   if (IrReceiver.decode()) {
        Serial.println(results.value, HEX);
        IrReceiver.resume(); // Enable receiving of the next value
  }
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

} else {
        Serial.println("Data is not ready!");
   }
    CCS811.writeBaseLine(0x447B);
    //delay cannot be less than measurement cycle
    delay(2000);
}
