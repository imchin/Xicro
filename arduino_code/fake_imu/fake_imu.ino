#include <Xicro_sub_N_pub_ID_3.h>
Xicro xicro;

uint32_t timestamp = 0;

float linear_acceleration_covariance[9]={1,0,0,0,1,0,0,0,1};
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  xicro.begin(&Serial);
}

void loop() {
  // put your main code here, to run repeatedly:
      xicro.Spin_node();
      if (micros() - timestamp >= 100000) {
        timestamp = micros();
        xicro.publish_fake_Imu_arduino((int32_t)micros() / 1000000.00, (uint32_t)micros() / 1000000.00, "from arduino" , xicro.Sub_fake_Imu.orientation.x, xicro.Sub_fake_Imu.orientation.y , xicro.Sub_fake_Imu.orientation.z , xicro.Sub_fake_Imu.orientation.w , xicro.Sub_fake_Imu.orientation_covariance , xicro.Sub_fake_Imu.angular_velocity.x , xicro.Sub_fake_Imu.angular_velocity.y , xicro.Sub_fake_Imu.angular_velocity.z , xicro.Sub_fake_Imu.angular_velocity_covariance , (float)26.42 , (float)26.42, (float)26.42 , linear_acceleration_covariance);
      }
}
