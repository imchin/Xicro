#include <Xicro_demo_ID_3.h>
Xicro xicro;


float ax, ay, az;  
float gx, gy, gz;  

#include <Arduino_LSM6DS3.h>

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(57600);
  xicro.begin(&Serial);
  
  //Set timer
  TCB0.CTRLB = TCB_CNTMODE_INT_gc; 
  TCB0.CCMP  = 12500;   //20 Hz.
//  TCB0.CCMP  = 25000;   //10 Hz.
  TCB0.INTCTRL = TCB_CAPT_bm; 
  TCB0.CTRLA = TCB_CLKSEL_CLKTCA_gc | TCB_ENABLE_bm;
  //end of set timer
  
  IMU.begin();

  pinMode(A0,INPUT); // button
  pinMode(A1,INPUT); // button
  pinMode(A2,INPUT); // button
  pinMode(A3,INPUT); // button

  pinMode(3,OUTPUT); // buzzer

  pinMode(13,OUTPUT); // LED
  pinMode(12,OUTPUT); // LED
  pinMode(11,OUTPUT); // LED
}

void loop() {
  // put your main code here, to run repeatedly:
  xicro.Spin_node();
  
}

void buzzer_update(){
    if(xicro.Sub_output_arduino.message.buzzer.value==0){
      digitalWrite(3,1);
    }else{
      analogWrite(3,(uint8_t)~( xicro.Sub_output_arduino.message.buzzer.value));
    }
    
}
void led_update(){
 
    digitalWrite(13,!xicro.Sub_output_arduino.message.led_array.states[0]);
    digitalWrite(12,!xicro.Sub_output_arduino.message.led_array.states[1]);
    digitalWrite(11,!xicro.Sub_output_arduino.message.led_array.states[2]);
  
}

void update_value(){
  
    buzzer_update();
    led_update();
   
}


void read_value_Sendros2(){
    xicro.Publisher_input_arduino.message.potentiometer.value=(float)(analogRead(A0)/1023.00)*5.00;
    xicro.Publisher_input_arduino.message.button.states[0]=!digitalRead(A1);
    xicro.Publisher_input_arduino.message.button.states[1]=!digitalRead(A2);
    xicro.Publisher_input_arduino.message.button.states[2]=!digitalRead(A3);
    xicro.publish_input_arduino();
}



void read_imu_Sendros2(){
  if(IMU.readAcceleration(ax, ay, az) && IMU.readGyroscope(gx, gy, gz))
  {
      xicro.Publisher_imu_arduino.message.angular_velocity[0]=gx*(3.141592/180.00);
      xicro.Publisher_imu_arduino.message.angular_velocity[1]=gy*(3.141592/180.00);
      xicro.Publisher_imu_arduino.message.angular_velocity[2]=gz*(3.141592/180.00);
      xicro.Publisher_imu_arduino.message.specific_force[0]=ax*(9.80665);
      xicro.Publisher_imu_arduino.message.specific_force[1]=ay*(9.80665);
      xicro.Publisher_imu_arduino.message.specific_force[2]=az*(-9.80665);
      xicro.publish_imu_arduino();
  }

}








ISR(TCB0_INT_vect)
{
  read_imu_Sendros2();
  read_value_Sendros2();
  update_value();
  TCB0.INTFLAGS = TCB_CAPT_bm; 
}
