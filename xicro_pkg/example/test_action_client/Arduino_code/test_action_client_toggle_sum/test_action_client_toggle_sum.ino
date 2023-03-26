
#include <Xicro_action_client_ID_1.h>
Xicro xicro;


void setup() {
  Serial.begin(57600);
  xicro.begin(&Serial);
  pinMode(LED_BUILTIN,OUTPUT);    // test on led builtin
  
  xicro.Action_client_toggle_sum.request.a= 5;  // set data request
  xicro.action_client_call_toggle_sum();  // Send_goal
  
}

void loop() {
  xicro.Spin_node();

  // flag incoming feedback data
//  if(xicro.Action_client_toggle_sum.state == xicro.action_client_state.incoming_feedback){
//    digitalWrite(LED_BUILTIN,1);   
//  }
  

  digitalWrite(LED_BUILTIN,xicro.Action_client_toggle_sum.feedback.flag);   //  feedback data

 // test correct result 
//  if(xicro.Action_client_toggle.result.sum == 15){
//    digitalWrite(LED_BUILTIN,1);   //  result correct
//
//  }

// test server not response  
//  if(xicro.Action_client_toggle.state==xicro.action_client_state.server_not_response){  
//    digitalWrite(13,0);
//  }


// test timeout
//  if(xicro.Action_client_toggle.state==xicro.action_client_state.time_out){ 
//    digitalWrite(10,0);
//  }


}
