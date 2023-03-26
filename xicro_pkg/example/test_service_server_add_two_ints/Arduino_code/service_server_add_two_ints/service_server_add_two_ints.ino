#include <Xicro_service_server_add_ID_1.h>
Xicro xicro;

void add_two_ints(){
  xicro.Service_server_add_two_ints.response.sum = xicro.Service_server_add_two_ints.request.a + xicro.Service_server_add_two_ints.request.b;
  xicro.service_server_response_add_two_ints();
}
void setup() {
  Serial.begin(57600);
  xicro.begin(&Serial);  // Xicro begin
  xicro.begin_service_server((void*)&add_two_ints);  // Setup service server
  

}

void loop() {
  // put your main code here, to run repeatedly:
xicro.Spin_node();
}
