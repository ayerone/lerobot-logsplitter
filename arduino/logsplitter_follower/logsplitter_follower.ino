
const int motor_a = 2;
const int motor_b = 3;

String command;
float last_setting;

const unsigned long BAUD = 115200;

void setup() {
  Serial.begin(BAUD);

  pinMode(motor_a, OUTPUT);
  pinMode(motor_b, OUTPUT);
  
  Serial.println("Logsplitter Follower Uno is READY.");

  command.reserve(20);
  last_setting = 0;

  return;
}

void readCommand() {
  command = Serial.readStringUntil('\n');
  command.trim(); // Remove any stray carriage returns or spaces

  return;
}

void setMotor(float setting) {
  digitalWrite(motor_a, setting > 40); 
  digitalWrite(motor_b, setting < -40);

  return;
}

void handleCommand() {
  if ( command.equalsIgnoreCase("READ") ) {
    // Serial.print("Current State: ");
    Serial.println(last_setting);
  } else {
    // Serial.print("Received Command: ");
    last_setting = command.toFloat();

    setMotor(last_setting);
    
    Serial.println(last_setting);
  }
  return;
}

void loop() {
  if (Serial.available() > 0) {
    readCommand();
    handleCommand();
  }
  return;
}
