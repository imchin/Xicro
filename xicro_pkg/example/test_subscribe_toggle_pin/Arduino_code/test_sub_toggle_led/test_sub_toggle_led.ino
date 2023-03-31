
#include <Xicro_toggle_led_ID_1.h>
Xicro xicro;


void setup() {
  Serial.begin(57600);
  xicro.begin(&Serial);   // Xicro begin
  pinMode(LED_BUILTIN,OUTPUT);    // test on led builtin

}
void loop(){
  
  xicro.Spin_node();   // spin_node 
  digitalWrite(LED_BUILTIN,xicro.Subscription_toggle.message.data); 
     
}
