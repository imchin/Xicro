
#include <Xicro_demo_ID_3.h>
Xicro xicro;


void setup() {
  // put your setup code here, to run once:
  pinMode(10,OUTPUT); // LED timeout
  pinMode(11,OUTPUT); // LED Feedback
  pinMode(13,OUTPUT); // LED server not response
  digitalWrite(10,1);
  digitalWrite(11,1);
  digitalWrite(13,1);
  Serial.begin(57600);
  xicro.begin(&Serial);
  
  xicro.Action_client_toggle.request.a= 10;
  xicro.action_client_call_toggle();
  
}

void loop() {
  // put your main code here, to run repeatedly:
  xicro.Spin_node();
  digitalWrite(11,!xicro.Action_client_toggle.feedback.flag);
  if(xicro.Action_client_toggle.state==xicro.action_client_state.server_not_response){  // test server not response
    digitalWrite(13,0);
  }
  if(xicro.Action_client_toggle.state==xicro.action_client_state.time_out){ // test timeout
    digitalWrite(10,0);
  }
}
