/*
 * wear lumination 
 * Created by t.uehara and a_ono / sweet electronics
 * https://github.com/usopyon/wearlumination
 */

#include <wiring_private.h>

// ピン配置

static int out1 = 3;//PWM
static int out2 = 5;//PWM
static int in1 = 1;
static int in2 = 2;

// その他

char buff[8];
int delay_time = 200;//200ms
unsigned long cmd_time = 0UL;
unsigned long wait_time = 10UL * 1000UL; //10秒

void setup(){
  pinMode(out1, OUTPUT);
  pinMode(out2, OUTPUT);
  Serial.begin(9600);
  Serial.println("ready");

}

void loop() 
{
  serial_read();
  
  int val1 = analogRead(in1); 
  int val2 = analogRead(in2); 

  // 直近にコマンドを実行してから10秒以上経過したらセンサの値を扱う
  if( millis() - cmd_time > wait_time ){
    analogWrite(out1, val1/8);
    analogWrite(out2, val2/8);    
  }

  delay(delay_time);
}

void serial_read(){
  int pin = 0;
  int val = 0;
  int c = 0;
  while( Serial.available() ){
    buff[c] = Serial.read();
    c++;
  }
  //Serial.flush();
  Serial.print(buff);

  switch(buff[0]){
    case 114: //r
      Serial.print(" red");
      pin = out1;
      break;
    case 103: //g
      Serial.print(" green");
      pin = out2;
      break;
  }

  if( buff[1] ){
    val = (int)(buff[1]-48)*27;// r9で255付近になるよう調整
    Serial.println(val);
    analogWrite(pin, val);
    cmd_time = millis();
  }

  for(int i = 0; i < 8; i++ ){
    buff[i] = NULL;
  }
  
}


