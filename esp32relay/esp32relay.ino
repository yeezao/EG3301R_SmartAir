const int relay = 26;

void setup() {
  pinMode(relay, OUTPUT);
}
void relayOn() {
    digitalWrite(relay, LOW);
}

void relayOff() {
    digitalWrite(relay, HIGH);
}
void loop() {
}
