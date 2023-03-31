#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class TogglePublisher(Node):

    def __init__(self):
        super().__init__('toggle_publisher')
        self.publisher_ = self.create_publisher(Bool, 'toggle', 10)
        timer_period = 0.25  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.msg = Bool()
        self.msg.data = False

    def timer_callback(self):
        self.msg.data = not self.msg.data
        self.publisher_.publish(self.msg)
      

def main(args=None):
    rclpy.init(args=args)
    toggle_publisher = TogglePublisher()
    rclpy.spin(toggle_publisher)
    toggle_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
