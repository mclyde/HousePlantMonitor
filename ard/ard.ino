const int ledPin = 13;    // digital pin
const int buttonPin = 3;  // digital pin
const int tempPin = 0;    // analog pin
const int soilPin = 1;    // analog pin
const int lightPin = -1;  // analog pin

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  bool buttonVal = buttonCheck();   // sends 'on' to Python at interval if button held down
  String tempVal = tempCheck();     // sends F temp to Python at interval
  String soilVal = soilCheck();     // sends reading from soil monitor
  
  String writeVal = "{\'temp\':\'" + tempVal + "\', \'soil\':\'" + soilVal + "\'}";
  char cBuffer[writeVal.length() + 1];
  writeVal.toCharArray(cBuffer, writeVal.length() + 1);
  Serial.write(cBuffer);
  delay(5000);                      // Repeat every 5 seconds
}

void ledRun() {
  digitalWrite(ledPin, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
  delay(500);
}

bool buttonCheck() {
  int buttonState = digitalRead(buttonPin);
  bool buttonOn = false;
  if (buttonState == LOW) {
    buttonOn = true;
  }
  return buttonOn;
}

String tempCheck() {
  float voltage = getVoltage(tempPin);
  float degC = (voltage - 0.5) * 100.0;
  float degF = degC * (9.0/5.0) + 32.0;

  char x [7];
  return String(dtostrf(degF, 5, 2, x));
}

String soilCheck() {
  int soilVal = analogRead(soilPin);
  
  char x [7];
  return String(dtostrf(soilVal, 5, 2, x));
}

float getVoltage(int pin) {
  return (analogRead(pin) * 0.004882814);  // converts 0 to 1023 into 0.0 to 5.0
}

