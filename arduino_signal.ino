void setup() 
{
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);
  Serial.begin(9600);

  Serial.println("Hi!, I am Arduino");
}

void loop() 
{
  if(Serial.read() == 'M'){
	digitalWrite(12, HIGH);
      	digitalWrite(13, LOW);
      	delay(1000);
	digitalWrite(12, LOW);}
  else if(Serial.read() == 'K'){
      	digitalWrite(13, HIGH);
      	digitalWrite(12, LOW);
      	delay(1000);
	digitalWrite(13, LOW);}
}
