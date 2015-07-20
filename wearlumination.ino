/*
 * wear lumination 
 * Created by t.uehara and a_ono / sweet electronics
 * https://github.com/usopyon/wearlumination
 */

// ピン配置

static int in1 = 1;
static int in2 = 2;

// その他

int delay_time = 200;//200ms
int debug_count = 0;

void setup(){
  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop() 
{
  int val1 = analogRead(in1); 
  int val2 = analogRead(in2);   

  analogWrite(13, val1/4);

  Serial.print(val1);
  //Serial.print(debug_count);
  Serial.print(",");
  Serial.print(val2);
  Serial.println();

  debug_count = debug_count % 1024 + 100;

  delay(delay_time);
}


