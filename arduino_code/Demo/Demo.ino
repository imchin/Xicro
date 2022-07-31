#include <Xicro_Demo_ID_1.h>
Xicro xicro;


#include <Servo.h>
Servo myservo; 

#include <Arduino_LSM6DS3.h>
float ax, ay, az;  
float gx, gy, gz;  

float orientation[4]={0};
float orientation_covariance[9]={1,0,0,0,1,0,0,0,1};
float angular_velocity[3]={0};
float angular_velocity_covariance[9]={1,0,0,0,1,0,0,0,1};
float linear_acceleration[3]={0};
float linear_acceleration_covariance[9]={1,0,0,0,1,0,0,0,1};






bool buttonstate[3]={0};
float poten=0;
uint32_t timestamp=0;


void setup() {
  // put your setup code here, to run once:
Serial.begin(57600);
xicro.begin(&Serial);

pinMode(A0,INPUT);  //poten
pinMode(A1,INPUT);  //buttonS1
pinMode(A2,INPUT);  //buttonS2
pinMode(A3,INPUT);  //buttonS3



IMU.begin();
//Set timer
  TCB0.CTRLB = TCB_CNTMODE_INT_gc; 
  TCB0.CCMP  = 12500;   //20 Hz.
  TCB0.INTCTRL = TCB_CAPT_bm; 
  TCB0.CTRLA = TCB_CLKSEL_CLKTCA_gc | TCB_ENABLE_bm;
//end of set timer

pinMode(3,OUTPUT);   //buzzer
pinMode(10,OUTPUT);  //led
pinMode(11,OUTPUT);  //led
pinMode(12,OUTPUT);  //led
pinMode(13,OUTPUT);  //led
pinMode(5,OUTPUT);   //servo
myservo.attach(5); 

}

void loop() {
  // put your main code here, to run repeatedly:
xicro.Spin_node();

if(micros()-timestamp>=100000){
  timestamp=micros();
  Buzzer();
  ser_vo();
  LED();
}

  
}

void read_imu_Sendros2(){
  if(IMU.readAcceleration(gx, gy, gz) && IMU.readGyroscope(ax, ay, az)){
      angular_velocity[0]=ax*(3.141592/180.00);
      angular_velocity[1]=ay*(3.141592/180.00);
      angular_velocity[2]=az*(3.141592/180.0);
      linear_acceleration[0]=gx*(9.80665);
      linear_acceleration[1]=gy*(9.80665);
      linear_acceleration[2]=gz*(-9.80665);
      xicro.publish_Imu_arduino(orientation ,orientation_covariance ,angular_velocity ,angular_velocity_covariance ,linear_acceleration ,linear_acceleration_covariance );
  
  }

}
void DemoInput_Sendros2(){
  buttonstate[0]=!digitalRead(A1);
  buttonstate[1]=!digitalRead(A2);
  buttonstate[2]=!digitalRead(A3);
  poten=(analogRead(A0)/1024.00)*5.00;
  xicro.publish_DemoInput(buttonstate,poten);
}
void Buzzer(){
    if(xicro.Sub_DemoOutput.buzzer==0){
      digitalWrite(3,1);
    }else{
      analogWrite(3,(uint8_t)~(xicro.Sub_DemoOutput.buzzer));
    }
    
}
void LED(){
  digitalWrite(13,!xicro.Sub_DemoOutput.led[0]);
  digitalWrite(12,!xicro.Sub_DemoOutput.led[1]);
  digitalWrite(11,!xicro.Sub_DemoOutput.led[2]);
  digitalWrite(10,!xicro.Sub_DemoOutput.led[3]);
}


void ser_vo(){
  myservo.write(((xicro.Sub_DemoOutput.servo/255.00)*180.00)); 
}



ISR(TCB0_INT_vect)
{
  
  DemoInput_Sendros2();
  read_imu_Sendros2();

  
  
  TCB0.INTFLAGS = TCB_CAPT_bm; 
}
