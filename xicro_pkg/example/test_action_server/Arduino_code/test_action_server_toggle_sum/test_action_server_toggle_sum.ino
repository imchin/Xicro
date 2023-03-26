
#include <Xicro_action_server_ID_1.h>
Xicro xicro;

void Action_server_callback(){
  xicro.Action_server_toggle_sum.result.sum = 0;   // set value
  xicro.Action_server_toggle_sum.feedback.flag= 0 ; // set value
  int count=0;
  uint64_t sum = 0;
  while(count!=xicro.Action_server_toggle_sum.request.a){
    if(count%2 ==0){
      xicro.Action_server_toggle_sum.feedback.flag= 1 ;
    }else{
      xicro.Action_server_toggle_sum.feedback.flag= 0 ;
    }
    xicro.action_server_send_feedback_toggle_sum();  // send feedback
    count=count+1;
    xicro.Action_server_toggle_sum.result.sum=xicro.Action_server_toggle_sum.result.sum+count;
    delay(500);
  }

  xicro.action_server_send_result_toggle_sum();   // send result
}

void setup() {
   Serial.begin(57600);
   xicro.begin(&Serial);
   xicro.begin_action_server((void *)&Action_server_callback); // setup_action_server
}

void loop() {
  xicro.Spin_node();
}
