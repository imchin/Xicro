
import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt8
import time
import multiprocessing as mp
class Count(Node):

    def __init__(self,count):
        super().__init__('count_subscriber')
        self.subscription = self.create_subscription(UInt8,'publish_from_Stm32',self.listener_callback,10)
        self.subscription  
        self.Count=count
        self.timestamp=0
    
    def listener_callback(self, msg):
        self.Count.value=self.Count.value+1  
       
        
def spin(rclpy,count): 
    q=Count(count)
    rclpy.spin(q)

def result(count):
    timestamp=0
    while(1):
        if(time.time_ns()-timestamp>=1000000000):
            timestamp=time.time_ns()
            print(" 1 Second recive : ",count.value, "Topic(s).")
            count.value=0


def main(args=None):
    rclpy.init()
    try:


        
       
        count = mp.Value('i',0)    
        p = mp.Process(target=spin,args=(rclpy,count,))
        p2 = mp.Process(target=result,args=(count,))
        p.start()
        p2.start()
   
        while(1):
            1
    except KeyboardInterrupt:
        p.terminate()
        p2.terminate()

    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()