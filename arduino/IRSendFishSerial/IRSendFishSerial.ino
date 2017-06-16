/*
 * IRremote: IRsendRawDemo - demonstrates sending IR codes with sendRaw
 * An IR LED must be connected to Arduino PWM pin 3.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 *
 * IRsendRawDemo - added by AnalysIR (via www.AnalysIR.com), 24 August 2015
 *
 * This example shows how to send a RAW signal using the IRremote library.
 * The example signal is actually a 32 bit NEC signal.
 * Remote Control button: LGTV Power On/Off. 
 * Hex Value: 0x20DF10EF, 32 bits
 * 
 * It is more efficient to use the sendNEC function to send NEC signals. 
 * Use of sendRaw here, serves only as an example of using the function.
 * 
 */


#include <IRremote.h>
unsigned long IRSignal = 0;
IRsend irsend;


//define variables needed to justify a sine wave and square wave
unsigned long bias = 0;  //bias
unsigned long enable; // 1 will allow voltage to flow from the batteries to the board/sma wires, 0 will close off flow to system
unsigned long f=0; // freq in TENS OF RAD/S
unsigned long amp = 0;//amplitude in DEGREES



void setup()
{
  pinMode(3,OUTPUT);
  Serial.begin(115200);

}

void loop() {
while(Serial.available()>0){//if we have serial data
if(Serial.read()=='!'){//if we have our start character
  enable=Serial.parseInt();//read first number
  f=Serial.parseInt();//read third number separated by space or comma
  bias=Serial.parseInt();//read bias angle in units of counts (-128->128)
  amp = Serial.parseInt();
  while(Serial.available()>0){
    byte junk = Serial.read();
  }
  //f = constrain(f,0,18);//rad/s
bias = constrain(bias,0,90);//
amp = constrain(amp,0,90);//

IRSignal = (enable<<24)+(f<<16)+(bias<<8)+amp;

Serial.print(enable);
    Serial.print("\t");
    Serial.print(f);
    Serial.print("\t");
    Serial.print(bias);
    Serial.print("\t");
    Serial.print(amp);
    Serial.print("\t");
Serial.println(IRSignal);


irsend.sendNEC(IRSignal,32); //

  }
  }


  delay(1); //In this example, the signal will be repeated every 5 seconds, approximately.
}
