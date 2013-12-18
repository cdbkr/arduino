/**
 *	@file		temp-duino.ino
 *	@version	1.0
 *
 *	@author		Francesco Vitullo
 *	@note		Temperature Email Alarm with Arduino
 */

int sensorPin = A0;    //Insert sensor pin
int sensorValue = 0;  //Sensor value

//Initialize communication
void setup() {
  Serial.begin(9600);
}

//Loop code communicating values
void loop() {
  sensorValue = analogRead(sensorPin);     
  Serial.println((sensorValue*0.2222)- 61.111);  
}
