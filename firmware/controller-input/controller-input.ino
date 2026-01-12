const uint8_t DATA_PINS[8] = {2, 3, 4, 5, 6, 7, 8, 9};
const uint8_t OPCODE_PINS[4] = {10, 11, 12, 13};

const uint8_t LOAD_A_PIN = A0;
const uint8_t LOAD_B_PIN = A1;
const uint8_t LOAD_R_PIN = A2;

void setDataBus(uint8_t value) {
  for (uint8_t bit = 0; bit < 8; ++bit) {
    digitalWrite(DATA_PINS[bit], (value >> bit) & 0x01);
  }
}

void setOpcode(uint8_t opcode) {
  for (uint8_t bit = 0; bit < 4; ++bit) {
    digitalWrite(OPCODE_PINS[bit], (opcode >> bit) & 0x01);
  }
}

void pulseLoad(uint8_t pin) {
  digitalWrite(pin, HIGH);
  delayMicroseconds(20);
  digitalWrite(pin, LOW);
}

long parseValue(const String &token) {
  char buffer[32];
  token.toCharArray(buffer, sizeof(buffer));
  return strtol(buffer, nullptr, 0);
}

void printHelp() {
  Serial.println("Commands:");
  Serial.println("  A <value>   - Load A register with 0-255");
  Serial.println("  B <value>   - Load B register with 0-255");
  Serial.println("  OP <value>  - Set opcode (0-15)");
  Serial.println("  BUS <value> - Drive data bus without pulsing load");
  Serial.println("  EXEC        - Pulse LOAD_R");
  Serial.println("  HELP        - Show this help");
}

void setup() {
  Serial.begin(115200);

  for (uint8_t i = 0; i < 8; ++i) {
    pinMode(DATA_PINS[i], OUTPUT);
    digitalWrite(DATA_PINS[i], LOW);
  }

  for (uint8_t i = 0; i < 4; ++i) {
    pinMode(OPCODE_PINS[i], OUTPUT);
    digitalWrite(OPCODE_PINS[i], LOW);
  }

  pinMode(LOAD_A_PIN, OUTPUT);
  pinMode(LOAD_B_PIN, OUTPUT);
  pinMode(LOAD_R_PIN, OUTPUT);
  digitalWrite(LOAD_A_PIN, LOW);
  digitalWrite(LOAD_B_PIN, LOW);
  digitalWrite(LOAD_R_PIN, LOW);

  Serial.println("Controller Input Ready.");
  printHelp();
}

void loop() {
  if (!Serial.available()) {
    return;
  }

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) {
    return;
  }

  line.toUpperCase();

  if (line == "HELP") {
    printHelp();
    return;
  }

  if (line == "EXEC") {
    pulseLoad(LOAD_R_PIN);
    Serial.println("LOAD_R pulse issued.");
    return;
  }

  int spaceIndex = line.indexOf(' ');
  String command = line;
  String argument = "";
  if (spaceIndex > 0) {
    command = line.substring(0, spaceIndex);
    argument = line.substring(spaceIndex + 1);
    argument.trim();
  }

  if (command == "A") {
    long value = parseValue(argument);
    value = constrain(value, 0, 255);
    setDataBus(static_cast<uint8_t>(value));
    pulseLoad(LOAD_A_PIN);
    Serial.print("Loaded A = ");
    Serial.println(value);
    return;
  }

  if (command == "B") {
    long value = parseValue(argument);
    value = constrain(value, 0, 255);
    setDataBus(static_cast<uint8_t>(value));
    pulseLoad(LOAD_B_PIN);
    Serial.print("Loaded B = ");
    Serial.println(value);
    return;
  }

  if (command == "OP") {
    long value = parseValue(argument);
    value = constrain(value, 0, 15);
    setOpcode(static_cast<uint8_t>(value));
    Serial.print("Opcode set to ");
    Serial.println(value);
    return;
  }

  if (command == "BUS") {
    long value = parseValue(argument);
    value = constrain(value, 0, 255);
    setDataBus(static_cast<uint8_t>(value));
    Serial.print("Data bus set to ");
    Serial.println(value);
    return;
  }

  Serial.println("Unrecognized command. Type HELP for options.");
}
