int termPin1 = 0;
int termPin2 = 1;
int termPin3 = 2;

void setup() {
  // put your setup code here, to run once:
pinMode(termPin1,INPUT);
pinMode(termPin2, INPUT);
pinMode(termPin3, INPUT);

Serial.begin(9600);
}

void loop() 
{
  // put your main code here, to run repeatedly:
int sensorReading1 = analogRead(termPin1);
int sensorReading2 = analogRead(termPin2);
int sensorReading3 = analogRead(termPin3);
//int thisPitch = map(sensorReading, 0, 1023, 4500, 10000);
Serial.println(sensorReading1);
Serial.println(sensorReading2);
Serial.println(sensorReading3);
Serial.println("q");
delay(500);
}
