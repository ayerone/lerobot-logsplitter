
const int switch1Pin = 2;
const int switch2Pin = 3;

const unsigned long BAUD = 115200;

int currentState = 0; // Default state

void setup() {
  Serial.begin(BAUD);

  pinMode(switch1Pin, INPUT_PULLUP);
  pinMode(switch2Pin, INPUT_PULLUP);
  
  Serial.println("Logsplitter Leader Uno is READY.");
}

void loop() {
  // 1) Handle Incoming Serial Data
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any stray carriage returns or spaces

    if (command.equalsIgnoreCase("READ")) {
      // Serial.print("Current State: ");
      Serial.println(currentState);
    } else {
      // Serial.print("Received Command: ");
      Serial.println(command);
    }
  }

  // 2) Read the 2 switches
  // Using !digitalRead because INPUT_PULLUP makes a pressed switch LOW
  bool s1Active = (digitalRead(switch1Pin) == LOW);
  bool s2Active = (digitalRead(switch2Pin) == LOW);

  // 3) State Logic
  // a) Switch 1 active, Switch 2 inactive
  if (s1Active && !s2Active) {
    currentState = -50;
  }
  // b) Switch 2 active, Switch 1 inactive
  else if (s2Active && !s1Active) {
    currentState = 50;
  }
  // c) Both inactive
  else if (!s1Active && !s2Active) {
    currentState = 0;
  }
}
