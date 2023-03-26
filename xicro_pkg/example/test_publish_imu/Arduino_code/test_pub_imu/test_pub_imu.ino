#include <Xicro_imu_ID_1.h>    
Xicro xicro;

uint32_t timestamp=0;
void setup() {
  Serial.begin(57600);
  xicro.begin(&Serial);
 
}

void loop() {
   xicro.Spin_node();   // spin_node 
   
//   // Esp32 wemos D1 mini
//   if(millis()-timestamp>=100){
//      timestamp=millis();
//      xicro.Publisher_test_fakeimu.message.header.stamp.sec= (int32_t)timestamp/1000;
//      xicro.Publisher_test_fakeimu.message.orientation.x=3.14;
//      xicro.Publisher_test_fakeimu.message.header.frame_id="Esp32 wemos D1 mini";
//      xicro.publish_test_fakeimu();
//   }

//   // Esp32 TTGo mini V:1.3
   if(millis()-timestamp>=100){
      timestamp=millis();
      xicro.Publisher_imu_arduino.message.header.stamp.sec= (int32_t)timestamp/1000;
      xicro.Publisher_imu_arduino.message.orientation.x=3.14;
      xicro.Publisher_imu_arduino.message.header.frame_id="Esp32 TTGo mini V:1.3";
      xicro.publish_imu_arduino();
   }

   // Arduino Uno wifi rev2
//   if(millis()-timestamp>=100){
//      timestamp=millis();
//      xicro.Publisher_test_fakeimu.message.header.stamp.sec= (int32_t)timestamp/1000;
//      xicro.Publisher_test_fakeimu.message.orientation.x=3.14;
//      xicro.Publisher_test_fakeimu.message.header.frame_id="Arduino Uno wifi rev2";
//      xicro.publish_test_fakeimu();
//   }


   
}
