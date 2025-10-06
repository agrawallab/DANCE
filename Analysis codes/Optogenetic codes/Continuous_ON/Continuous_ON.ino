// Fixed Frequency Script
// Continuous stimulation

// Arduino should be reset in sync with camera record start.

void setup() {
  pinMode(8, OUTPUT); // GREEN LED positive pin on 8, negative pin on GND
  pinMode(13, OUTPUT); // Indicator LED on Board
}

void loop() {

  digitalWrite(8, HIGH); // LED glows
  digitalWrite(13, HIGH); // LED glows
}
