#include <Xicro_demo_ID_3.h>
Xicro xicro;

void add_two_ints(){
//  digitalWrite(11,0);
  xicro.Service_server_add_two_ints_arduino.response.sum = xicro.Service_server_add_two_ints_arduino.request.a + xicro.Service_server_add_two_ints_arduino.request.b;
  xicro.service_server_response_add_two_ints_arduino();
}
void setup() {
  // put your setup code here, to run once:
//  pinMode(11,OUTPUT); // LED
//  digitalWrite(11,1);
  Serial.begin(57600);
  xicro.begin(&Serial);
  xicro.begin_service_server((void*)&add_two_ints);

}

void loop() {
  // put your main code here, to run repeatedly:
xicro.Spin_node();
}
