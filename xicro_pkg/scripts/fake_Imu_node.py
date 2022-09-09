#!/usr/bin/python3
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu

from std_msgs.msg import Float32
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Imu, 'fake_Imu', 10)
        timer_period = 0.033  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Imu()
        msg.header.frame_id="fake_Imu"

        msg.angular_velocity.x=3.14
        msg.angular_velocity.y=-3.14
        msg.angular_velocity.z=3.14

        msg.orientation.x=3.264
        msg.orientation.y=42.14
        msg.orientation.z=26.14
        msg.orientation.w=3.14
        msg.angular_velocity_covariance=[1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0]

        msg.header.stamp.nanosec=133
        # msg=Float32()
        # msg.data=0.2642+self.i

        self.publisher_.publish(msg)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()