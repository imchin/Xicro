#include <Xicro_demo_ID_3.h>     
Xicro xicro;  

void setup() {
Serial.begin(57600);
xicro.begin(&Serial);    // xicro begin
pinMode(11,OUTPUT);
pinMode(13,OUTPUT);
digitalWrite(11,1);
digitalWrite(13,1);
xicro.Service_client_add_two_ints.request.a = 26;
xicro.Service_client_add_two_ints.request.b = 16;
xicro.service_client_call_add_two_ints();
 
}

void loop() {
  xicro.Spin_node();
  if(xicro.Service_client_add_two_ints.state == xicro.service_client_state.get_response_done && xicro.Service_client_add_two_ints.response.sum==42){ // test response correct
    digitalWrite(11,0);
  }
  if(xicro.Service_client_add_two_ints.state == xicro.service_client_state.server_not_response){ // test server not response
    digitalWrite(13,0);
  }
}
