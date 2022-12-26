
#include <Xicro_demo_ID_3.h>
Xicro xicro;

void Action_server_callback(){
//  digitalWrite(11,0);
  for(int i=0;i<xicro.Action_server_toggle_arduino.request.a;i++){
    xicro.Action_server_toggle_arduino.feedback.ap=xicro.Action_server_toggle_arduino.feedback.ap+i;
    xicro.Action_server_toggle_arduino.result.sum=xicro.Action_server_toggle_arduino.result.sum+xicro.Action_server_toggle_arduino.feedback.ap;
    xicro.action_server_send_feedback_toggle_arduino();
    delay(100);
  }
  xicro.action_server_send_result_toggle_arduino();
}

void setup() {
  // put your setup code here, to run once:
   Serial.begin(57600);
   xicro.begin(&Serial);
//   pinMode(11,OUTPUT);
//   digitalWrite(11,1);
   xicro.begin_action_server((void *)&Action_server_callback);
}

void loop() {
  // put your main code here, to run repeatedly:
xicro.Spin_node();
}
