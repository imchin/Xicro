#!/usr/bin/python3
import rclpy
from rclpy.node import Node
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sys
import threading
from xicro_interfaces.msg import DemoInput,DemoOutput
from std_msgs.msg import UInt8
class GUI(Node):
    def __init__(self):
        super().__init__('gui')
        self.publisher_ = self.create_publisher(DemoOutput,'DemoOutput',10)
        self.publisher_2 = self.create_publisher(UInt8,'DemoOutput2',10)
        self.subscriber_button = self.create_subscription(DemoInput,'DemoInput',self.demoinput_callback,10)
        timer_period = 0.05
        self.timer = self.create_timer(timer_period,self.timer_callback)
        
        #Initial screen
        screen_width = 1280
        screen_height = 720
        self.root = Tk()
        self.root.title('GUI   XICRO')
        self.TFont = ("Cordia new", 15)
        self.TFont2 = ("Cordia new", 8 )
        self.TFont3 = ("Cordia new", 35)
        self.w = screen_width
        self.h = screen_height
        self.current_servo = tk.DoubleVar()
        self.current_buzzer = tk.DoubleVar()
        self.sum_counter =0
        self.l1_open=0
        self.l2_open=0
        self.l3_open=0
        self.l4_open=0
        self.buzzer_val = 0
        self.servo_val = 0
        self.d1,self.d2,self.d3,self.d4 = False,False,False,False
        self.bool = [False,False,False]

        self.preS =[False,False,False]
        
        ##scrren info
        LED1=Button(self.root, text="LED1",bg='bisque4',fg='white',command=self.s1_click,height= 5, width=10).place(x=self.w/60 +75 ,y=self.h/13)
        LED2=Button(self.root, text="LED2",bg='salmon3',fg='white',command=self.s2_click,height= 5, width=10).place(x=self.w/60 +75 ,y=self.h/13 +150)
        LED3=Button(self.root, text="LED3",bg='RosyBrown3',fg='white',command=self.s3_click,height= 5, width=10).place(x=self.w/60 +75 ,y=self.h/13 +150 +150)
        LED4=Button(self.root, text="LED4",bg='DarkSlateGray4',fg='white',command=self.s4_click,height= 5, width=10).place(x=self.w/60 +75 ,y=self.h/13 +150 +150+150)
        Buzzer_slider = Scale(self.root, from_=0, to=255, orient=VERTICAL,length=580,tickinterval=15,variable=self.current_buzzer,command=self.get_buzzer_value).place(x=self.w/3.5 ,y=self.h/13 )

        Servo_slider = Scale(self.root, from_=0, to=180, orient=VERTICAL,length=500,tickinterval=10,variable=self.current_servo,command=self.get_servo_value).place(x=self.w/3.5 + 300 ,y=self.h/13 )


        Label(text ="BUZZER",fg="black",font=self.TFont).place(x=self.w/3.5,y=self.h/13 +150 +150+150 +80+70)
        Label(text ="SERVO",fg="black",font=self.TFont).place(x=self.w/3.5+300,y=self.h/13 +150 +150+150 +80)
        # Label(text=,fg="black",font=self.TFont3).place(x=self.w/1.2,y=self.h/13 +150)
        Label(text =" Press S1 to +1\n Press S2 to -1\n   Press S3 to reset",fg="black",font=self.TFont).place(x=self.w/1.3,y=self.h/13 +150 +150)      

        #screen visualize
        self.root.geometry(str(screen_width)+'x'+str(screen_height))
        self.root.eval('tk::PlaceWindow . center')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # self.root.mainloop()
  
    def counter_value(self,S1,S2,S3):
        if S1 and not self.preS[0]:
            if self.sum_counter<=999:
                self.sum_counter+=1
            else:
                self.sum_counter=0
        if S2 and not self.preS[1]:
            if self.sum_counter>0:
                self.sum_counter-=1
            else:
                self.sum_counter=0
        if S3 and not self.preS[2]:
            self.sum_counter=0
        self.preS[0]=S1
        self.preS[1]=S2
        self.preS[2]=S3
        return str(self.sum_counter)

    def s1_click(self):
        self.l1_open+=1
        if self.l1_open==1:
            # print('LED1 on')
            self.d1 = True
            return self.d1
        if self.l1_open>1:
            self.l1_open=0
            # print('LED1 off')
            self.d1 = False
            return self.d1

        # print('LED1 Clicked',self.l1_open)
    
    def s2_click(self):
        self.l2_open+=1
        if self.l2_open==1:
            self.d2 = True
            # print('LED2 on')
            return self.d2
        if self.l2_open>1:
            self.l2_open=0
            self.d2 = False
            # print('LED2 off')
            return self.d2
        # print('LED2 Clicked')

    def s3_click(self):
        self.l3_open+=1
        if self.l3_open==1:
            self.d3  = True
            # print('LED3 on')
            return self.d3
        if self.l3_open>1:
            self.l3_open=0
            self.d3 = False
            # print('LED3 off')
            return self.d3
        # print('LED3 Clicked')
    
    def s4_click(self):
        self.l4_open+=1
        if self.l4_open==1:
            self.d4 = True
            # print('LED4 on')
            return self.d4
        if self.l4_open>1:
            self.l4_open=0
            self.d4 = False
            # print('LED4 off')
            return self.d4
        # print('LED4 Clicked')
    
    def get_buzzer_value(self,event):
        if event ==None or event==0 or event=='0':
            event=0
            self.buzzer_val=0
        self.buzzer_val = int(event)
        # print('Send Buzzer = ',self.buzzer_val)   #event = buzzer slider value
        return self.buzzer_val


    def get_servo_value(self,event):
        if event ==None or event==0 or event=='0':
            event=0
            self.servo_val=0
        self.servo_val = round(int(event)*255/180)
        # print('Send servo = ',self.servo_val)  #event = servo slider value
        return self.servo_val
    
    def demoinput_callback(self,msg):
        
        self.bool = msg.buttonstate
        
        # return 1

    
    def timer_callback(self):
        msg = DemoOutput()
        a = self.counter_value(self.bool[0],self.bool[1],self.bool[2])
        Label(text=str(a),fg="black",font=self.TFont3).place(x=self.w/1.2,y=self.h/13 +150)
        # print(a)
        msg.buzzer = self.buzzer_val
        msg.servo = self.servo_val
        msg.led = [self.d1,self.d2,self.d3,self.d4]
        self.publisher_.publish(msg)
        self.root.update()
        # msg2 = UInt8()
        # msg2.data = 199
        # self.publisher_2.publish(msg2)
        
    
    def on_closing(self):
        self.root.destroy()
        sys.exit()
        

def main(args=None):
    rclpy.init(args=args)
    gui = GUI()
    # gui.root.after(10,gui.timer_callback)
    # print('aaaaaa')
    rclpy.spin(gui)

    gui.destroy_node()
    rclpy.shutdown()


    

if __name__ == '__main__':

    main()
