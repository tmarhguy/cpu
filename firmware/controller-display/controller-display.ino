const uint8_t DATA_PINS[8] = {2, 3, 4, 5, 6, 7, 8, 9};
const uint8_t LOAD_R_PIN = A0;

uint8_t readDataBus() {
  uint8_t value = 0;
  for (uint8_t bit = 0; bit < 8; ++bit) {
    if (digitalRead(DATA_PINS[bit])) {
      value |= (1 << bit);
    }
  }
  return value;
}

void printValue(uint8_t value) {
  Serial.print("R = 0x");
  if (value < 16) {
    Serial.print('0');
  }
  Serial.print(value, HEX);
  Serial.print(" (dec ");
  Serial.print(value);
  Serial.print(", bin ");
  for (int bit = 7; bit >= 0; --bit) {
    Serial.print((value >> bit) & 0x01);
  }
  Serial.println(')');
}

void setup() {
  Serial.begin(115200);

  for (uint8_t i = 0; i < 8; ++i) {
    pinMode(DATA_PINS[i], INPUT);
  }
  pinMode(LOAD_R_PIN, INPUT);

  Serial.println("Controller Display Ready.");
  Serial.println("Waiting for LOAD_R pulses...");
}

void loop() {
  static int lastStrobe = LOW;
  static uint8_t lastValue = 0;
  static unsigned long lastReport = 0;

  int strobe = digitalRead(LOAD_R_PIN);
  bool risingEdge = (strobe == HIGH && lastStrobe == LOW);
  lastStrobe = strobe;

  uint8_t value = readDataBus();
  unsigned long now = millis();

  if (risingEdge || (value != lastValue && now - lastReport > 250)) {
    printValue(value);
    lastValue = value;
    lastReport = now;
  }
}
