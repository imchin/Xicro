#include <Xicro_service_client_add_ID_1.h>     
Xicro xicro;  

void setup() {
  Serial.begin(57600);
  xicro.begin(&Serial);    // xicro begin
  pinMode(LED_BUILTIN,OUTPUT);    // test on led builtin
  
  xicro.Service_client_add_two_ints.request.a = 26;   // set data to request
  xicro.Service_client_add_two_ints.request.b = 16;  // set data to request
  xicro.service_client_call_add_two_ints(); 

}

void loop() {
  xicro.Spin_node();

  // for test correctans and xicro service client state
  if(xicro.Service_client_add_two_ints.state == xicro.service_client_state.get_response_done && xicro.Service_client_add_two_ints.response.sum==42){ // test response correct
    digitalWrite(LED_BUILTIN,1);
  }

//  // for test server on ros2 is not available
//  if(xicro.Service_client_add_two_ints.state == xicro.service_client_state.server_not_response){ // test server not response
//    digitalWrite(LED_BUILTIN,1);
//  }
}
