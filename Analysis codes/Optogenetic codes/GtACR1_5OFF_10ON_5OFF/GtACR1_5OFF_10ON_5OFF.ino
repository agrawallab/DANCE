// Fixed Frequency Script
// 5 mins No-stimulation, 10 min 5Hz Green light stimulation, 5 min No-stimulation
// Delay time can be modified according to experiment requirement based on below calculation

// delay is given in milliseconds (1 sec = 1000 ms)
// 5 min = 300 sec = 300000 ms

// LOW = LED OFF, HIGH = LED ON
// Arduino should be reset in sync with camera record start.

void setup() {
  pinMode(8, OUTPUT); // GREEN LED positive pin on 8, negative pin on GND
  pinMode(13, OUTPUT); // Indicator LED on Board
}

void loop() {

  digitalWrite(8, LOW);
  digitalWrite(13, LOW);
  delay(300000); // 5min LEDs OFF
  digitalWrite(8, HIGH);
  digitalWrite(13, HIGH);
  delay(300000); // 5min LEDs ON
  digitalWrite(8, HIGH);
  digitalWrite(13, HIGH);
  delay(300000); // 5min LEDs ON
  digitalWrite(8, LOW);
  digitalWrite(13, LOW);
  delay(300000); // 5min LEDs OFF

// Precautionary LEDs off until next set of experiment starts 
  delay(300000); // 5min OFF
  delay(300000); // 5min OFF
  delay(300000); // 5min OFF
  delay(300000); // 5min OFF
  delay(300000); // 5min OFF

}
