#include <Xicro_imu_ID_1.h>    
Xicro xicro;

uint32_t timestamp=0;
void setup() {
  Serial.begin(57600);
  xicro.begin(&Serial);
 
}

void loop() {
   xicro.Spin_node();   // spin_node 

   if(millis()-timestamp>=100){
      timestamp=millis();
      xicro.Publisher_imu.message.header.stamp.sec= (int32_t)timestamp/1000;
      xicro.Publisher_imu.message.orientation.x=3.14;
      xicro.Publisher_imu.message.header.frame_id="Esp32 TTGo mini V:1.3";
      xicro.publish_imu();
   }


   
}
