int out1 = 3;//PWM
int out2 = 5;//PWM
int in1 = 1;
int in2 = 2;

void setup(){
  pinMode(out1, OUTPUT);
  pinMode(out2, OUTPUT);
}

void loop() 
{
  int val1 = analogRead(in1); 
  int val2 = analogRead(in2); 
  
  analogWrite(out1, val1/4);
  analogWrite(out2, val2/4);
}
