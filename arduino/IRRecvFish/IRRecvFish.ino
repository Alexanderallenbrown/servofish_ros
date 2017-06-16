/*
 * IRremote: IRrecvDemo - demonstrates receiving IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 */

#include <IRremote.h>
#include <Servo.h>

Servo myservo;


int RECV_PIN = 5;

IRrecv irrecv(RECV_PIN);

decode_results results;

unsigned long f=0;
unsigned long amp=0;
unsigned long bias=0;
unsigned long enable=1000;
float leddelay=0.1;
float lastswitchtime=0.0;
boolean ledstate=1;



float floatf=0;
float floatamp=0;
float floatbias=0;

float phi = 0;
float tnow = 0;
float dt = .01;
float oldtime=-1;
float tailangle = 0;

void setup()
{
  //Serial.begin(115200);
  // In case the interrupt driver crashes on setup, give a clue
  // to the user what's going on.
  //Serial.println("Enabling IRin");
  irrecv.enableIRIn(); // Start the receiver
  //Serial.println("Enabled IRin");
  pinMode(5,INPUT);
  myservo.attach(3);
  pinMode(1,OUTPUT);
}

void loop() {
  tnow = millis()/1000.0;
  dt = tnow-oldtime;
  oldtime=tnow;

  if ((tnow-lastswitchtime)>leddelay){
    ledstate=!ledstate;
    lastswitchtime=tnow;
  }
  digitalWrite(1,ledstate);
  
  unsigned long datain=0;
  if (irrecv.decode(&results)) {
    datain=results.value;
    //Serial.println(datain);
    irrecv.resume(); // Receive the next value
    enable=(datain&(0xFF000000))>>24;
    f = (datain&(0x00FF0000))>>16;
    bias = (datain&(0x0000FF00))>>8;
    amp = (datain)&(0x000000FF);
    floatamp = float(amp);
    floatbias=float(bias)-45;//was a positive number... allow negatives.
    floatf = float(f)/10.0;//in radians per second
//    Serial.print(datain);
//    Serial.print("\t");
//    Serial.print(enable);
//    Serial.print("\t");
//    Serial.print(floatf);
//    Serial.print("\t");
//    Serial.print(floatbias);
//    Serial.print("\t");
//    Serial.println(floatamp);
  }
  delay(1);
  if (enable==1){
    leddelay=0.25;
    myservo.attach(3);
    phi += floatf*dt;
    tailangle = floatamp*sin(phi)+floatbias+90;
  myservo.write(int(tailangle));
  }
  else if (enable==0){
    leddelay=1.0;
    myservo.detach();
  }
  
}
