#include "Arduino.h"
#include <SoftwareSerial.h>

SoftwareSerial mySerial(11, 10); // RX, TX
#define AEncoderInterrupt 0 
#define BEncoderInterrupt 1
#define EncoderPinA 2   // enkoder 2 ve 3 numaralı pine bağlanacak
#define EncoderPinB 3
volatile bool EncoderBSet;
volatile bool EncoderASet;
long pozisyon = 0;

void setup() {
  Serial.begin(115200);
  pinMode(EncoderPinA, INPUT);      // sets pin A as input
//  digitalWrite(EncoderPinA, HIGH);  // turn on pullup resistors
  pinMode(EncoderPinB, INPUT);      // sets pin B as input
 // digitalWrite(EncoderPinB, HIGH);  // turn on pullup resistors
  attachInterrupt(AEncoderInterrupt, HandleMotorInterruptA, CHANGE);
  attachInterrupt(BEncoderInterrupt, HandleMotorInterruptB, CHANGE);

  mySerial.begin(57600);
 // mySerial.println("Hello, world?");
  delay(500 );
}

void loop() {
  Serial.print("!");
  Serial.print(pozisyon);
  Serial.println("#");
  mySerial.print("poz: ");
  mySerial.println(pozisyon);
  delay(10);
}

void HandleMotorInterruptA()
{

  if (digitalRead(EncoderPinB) == digitalRead(EncoderPinA))
  {
	if(pozisyon == 0) pozisyon = 1024;
    	else pozisyon--;
  }
  else
  {	
    	if(pozisyon == 1024) pozisyon = 0;
	else pozisyon++;
  }
}

void HandleMotorInterruptB()
{
  if (digitalRead(EncoderPinB) == digitalRead(EncoderPinA))
  {
    	if(pozisyon == 1024) pozisyon = 0;
	else pozisyon++;
  }
  else
  {
    	if(pozisyon == 0) pozisyon = 1024;
    	else pozisyon--;
  }
}
