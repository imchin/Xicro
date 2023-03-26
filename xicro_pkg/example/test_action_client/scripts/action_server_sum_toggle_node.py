#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
import time
from xicro_interfaces.action import Toggle

class Toggleactionserver(Node):

    def __init__(self):
        super().__init__('toggleactionserver_node')
        self.action_server = ActionServer(self,Toggle,'toggle_sum',self.execute_callback)
        
       
    def execute_callback(self, goal_handle):
        feedback_msg = Toggle.Feedback()
        
        count=0
        sum=0
        while(count!= goal_handle.request.a):
            if(count%2==0):
                feedback_msg.flag = True
            else:
                feedback_msg.flag = False
            goal_handle.publish_feedback(feedback_msg)
            count=count+1
            sum=sum+count
            time.sleep(0.5)

        goal_handle.succeed()
        result = Toggle.Result()
        result.sum = sum
        self.get_logger().info("Done task.")
        return result


    

def main(args=None):
    rclpy.init(args=args)
    try:
        toggle_action_server = Toggleactionserver()
        executor = MultiThreadedExecutor(num_threads=6)
        executor.add_node(toggle_action_server)
        try:
            executor.spin()
        finally:
            executor.shutdown()
           
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()