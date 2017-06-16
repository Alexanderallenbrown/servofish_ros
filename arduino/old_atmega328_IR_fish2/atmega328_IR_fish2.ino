#include <IRremote.h>


#include <Servo.h>
//#include <IRremote.h>

float freq = 2*PI;//initial frequency in rad/s
float theta = 0;//phase angle of tail
unsigned long tnow = millis();//time
unsigned long told = tnow-1;
float dt = (tnow-told)*.001;
//float fpos = 0;//position of tail
int pos = 0;//int(fpos);//position of tail
int bias = 90;//bias angle of tail (deg);
int amplitude = 20;//tail amplitude (deg);
boolean smove = HIGH;//whether fish should move

int IRpin = 5;
IRrecv irrecv(IRpin);
decode_results results;

Servo servo;

void setup()
{ 
  irrecv.enableIRIn(); // Start the receiver
  servo.attach(3);
  //pinMode(0,OUTPUT);
  pinMode(13,OUTPUT);
  Serial.begin(9600);
  }

void loop() {
   //deal with timing
  tnow = millis();
  dt = (tnow-told)*.001;
  told = tnow;

  //read vals from IR
  if (irrecv.decode(&results)) 
    {
      //Serial.println(results.value,DEC);
      if(results.value==16753245){
        smove=!smove;
      }
      else if(results.value==16736925){
        amplitude+=5;
        constrain(amplitude,0,90);
      }
      else if(results.value==16754775){
        amplitude-=5;
        constrain(amplitude,0,90);
      }
      else if(results.value==16761405){
        bias+=5;
        constrain(bias,-45,45);
      }
      else if(results.value==16720605){
        bias-=5;
        constrain(bias,-45,45);
      }
      else if(results.value==16748655){
        freq+=1;
        constrain(freq,0,20*PI);
      }
      else if(results.value==16769055){
        freq-=1;
        constrain(freq,0,20*PI);
      }
      irrecv.resume();   // Receive the next value
    }
  
  //compute new phase angle for tail
  if(smove){
  theta += freq*dt;//increase by phase
  pos = amplitude*sin(theta)+bias;
  //pos = int(fpos);

  digitalWrite(13,HIGH);
}
else if (!smove){
  digitalWrite(13,LOW);
}
}

Serial.print(smove);
Serial.print(",");
Serial.print(pos);
Serial.print(",");
Serial.print(amplitude);
Serial.print(",");
Serial.print(bias);
Serial.print(",");
Serial.println(freq);

servo.write(pos);
delay(10);
//if(smove){
//SoftwareServo::refresh();//This row....
//}
}
