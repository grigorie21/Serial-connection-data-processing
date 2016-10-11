int ledPin = 3;
int soundPin = 2;
int potPin = 3;

int ledState = LOW;
long previousMillis = 0;
long interval = 1000;

void setup() {
  // initialize serial communications:
  Serial.begin(9600);
  pinMode (soundPin, OUTPUT);
  pinMode (ledPin, OUTPUT);
}

void loop() {
  // read the sensor:
  int sensorReading = analogRead(potPin);
  // print the sensor reading
  Serial.println(sensorReading);
  
  int thisPitch = map(sensorReading, 0, 1023, 4500, 10000);

  // play
  tone(soundPin, thisPitch, 10);
  //delay(1);        // delay in between reads for stability
  
unsigned long currentMillis = millis();

if (currentMillis - previousMillis > interval) {
  previousMillis = currentMillis;

   if (ledState == LOW) 
    ledState = HIGH;
    else
    ledState = LOW;
    digitalWrite(ledPin, ledState);  
    }
}

    







