
# xicro: ROS2 package for microcontroller interface

## Rationale behind "xicro":
If you are looking for a way to establish some communication between a microcontroller and ROS2 network, you probably came across "micro-ROS". Unlike its predecessor (rosserial), micro-ROS mostly relies on the use of Real-Time Operating System (RTOS), which allows developers to implement concurrent tasks in multi-threading fashion. A software engineer can write an embedded program like a piece of software. However, RTOS requires microcontroller's memeory. Therefore, micro-ROS can be applied to a limited number of microcontrollers with RTOS. You can no longer use a simple microcontroller like Arduino Uno with ROS2 using micro-ROS. (See https://micro.ros.org/docs/overview/hardware/). This seems odd because rosserial in ROS(1) was very versatile and can be applied to any microcontrollers without the complication of RTOS (if configured properly).

Using the same principle as rosserial, we come up with "xicro" (not to be confused with "xacro"). xicro allows the developers to use the generated libraries for the microcontrollers as well as auto-generated node that intrepreter information from/to the microcontrollers via UART.

## General features of "xicro":
* xicro auto-generates a library for a microcontroller (.h file)
* xicro auto-generates a node that communicates with UART
* xicro (should) supports all Arduino, ESP32, ESP8266 and STM32 families.

"xicro" is a part of an ongoing project of CoXsys Robotics under GPL license. 




## Installation
#### Xicro requires metapackage

  - ### install metapackage
    xxx_ws is your workspace
  ```bash
    cd ~/xxx_ws/src      #cd to your workspace
    mkdir Xicro          #create metapackage
    cd Xicro             #cd to metapackage
    git clone https://github.com/imchin/Xicro .
    cd ~/xxx_ws
    colcon build
    source ~/xxx_ws/install/setup.bash
  ```
  - ### install python library
    ```bash
    pip3 uninstall serial
    pip3 install pyserial
    pip3 install numpy
    ```

## Setup parameter in yaml
    cd ~/xxx_ws/src/Xicro/xicro_pkg/config      
    code setup_xicro.yaml

## setup_xicro.yaml is contain 
  - 1\. Idmcu : It sets the ID of the MCU for the system Xicro.

    The mcu Id may range from 0 to 15. 
    
  - 2\. Namespace : This is the name of the file that will be created.

  - 3\. Port : Name open port of MCU

  - 4\. generate_library_Path : Is the path for creating .h and .cpp files. Xicro will create a folder with files at the path.

    Path reference from ~/

  - 5\. Baudrate : Can config baudrate
    Baudrate affects the data transmission rate. Can use <=2000000
    
    \**Recommended at 115200.



  - 6\. Setup_Publisher : Configuration for publishing topic from MCU to ROS2.
    
    - In format : [ [ID_topic,Name_topic,Interface],[ID_topic_2,Name_topic_2,Interface_2],.......]
        - 1\. ID_topic : It sets the ID of the topic_publish for the system Xicro.
            
            The ID_topic Id may range from 0 to 255.
        - 2\. Name_topic : Specify the topic name you want MCU to publish to ROS2.
        - 3\. Interface : variable interfacefile configuration for use in the topic 

            Is contain 2 part in format 

            
             "(The name of the package that contains the interface file)/(Name_of_fileinterface).msg" 

  - 7\. Setup_Subscriber : Configuration for subscribe topic from  ROS2 to MCU.
    
    - In format : [ [ID_topic,Name_topic,Interface],[ID_topic_2,Name_topic_2,Interface_2],.......]
  
        - 1\. ID_topic : It sets the ID of the topic_subscribe for the system Xicro.
        
          The ID_topic Id may range from 0 to 255.
        - 2\. Name_topic : Specify the topic name you want MCU subscribe from ROS2.
        - 3\. Interface : variable interfacefile configuration for use in the topic 
          
          Is contain 2 part in format 

        
            "(The name of the package that contains the interface file)/(Name_of_fileinterface).msg" 

  - 8\. Setup_Srv_client : Configuration for service client. 
        
    - In format : [ [ID_service,Name_service,Interface,time_out],[ID_service_2,Name_service_2,Interface_2,time_out_2],.......]
     
        - 1\. ID_service : It sets the ID of the service_client for the system Xicro.
        
          The ID_service Id may range from 0 to 255.
        - 2\. Name_service : Specify the servive name you want MCU service call to ROS2.
        - 3\. Interface : variable interfacefile configuration for use in the service
        
            Is contain 2 part in format 

        
            "(The name of the package that contains the interface file)/(Name_of_fileinterface).srv" 
        - 4\. time_out : Limit the maximum service usage time. (In type float)

  - 9\. Setup_Srv_server : Configuration for service server. 
        
    - In format : [ [ID_service,Name_service,Interface,time_out],[ID_service_2,Name_service_2,Interface_2,time_out_2],.......]
      
        - 1\. ID_service : It sets the ID of the service_server for the system Xicro.
        
        The ID_service Id may range from 0 to 255.
        - 2\. Name_service : Specify the servive name you want  ROS2 service call to MCU.
        - 3\. Interface : variable interfacefile configuration for use in the service
          Is contain 2 part in format 

        
           "(The name of the package that contains the interface file)/(Name_of_fileinterface).srv" 
        - 4\. time_out : Limit the maximum service usage time. (In type float)

  - 10\. Setup_Action_client : Configuration for action client. 
        
    - In format : [ [ID_action,Name_action,Interface,time_out],[ID_action_2,Name_action_2,Interface_2,time_out_2],.......]
    
        - 1\. ID_action : It sets the ID of the action_client for the system Xicro
   
         The ID_action Id may range from 0 to 255.
        - 2\. Name_action : Specify the action name you want MCU action send_goal to ROS2.
        - 3\. Interface : variable interfacefile configuration for use in the action
        
          Is contain 2 part in format 

        
          "(The name of the package that contains the interface file)/(Name_of_fileinterface).action" 
        - 4\. time_out : Limit the maximum action usage time. (In type float)        
      
  - 11\. Setup_Action_server : Configuration for action server. 
    - In format : [ [ID_action,Name_action,Interface,time_out],[ID_action_2,Name_action_2,Interface_2,time_out_2],.......]
    
        - 1\. ID_action : It sets the ID of the action_server for the system Xicro
   
         The ID_action Id may range from 0 to 255.
        - 2\. Name_action : Specify the action name you want ROS2 action send_goal to MCU.
        - 3\. Interface : variable interfacefile configuration for use in the action
          Is contain 2 part in format 

        
          "(The name of the package that contains the interface file)/(Name_of_fileinterface).action" 
        - 4\. time_out : Limit the maximum action usage time. (In type float)        
      

## Create xicro library
The library will be generated based on setup_xicro.yaml
```bash
  cd ~/xxx_ws/src      #cd to your workspace
  colcon build
  ros2 run xicro_pkg generate_library.py argv1 argv2
```
 - argv1 : This is the mcu family that you want to use.

    Canbe [arduino , esp , stm32]


 - argv2 : HAL library
    
    Igone it if you use [arduino , esp]. 
    ### Example 
    In case use arduino family.
    ```bash
        ros2 run xicro_pkg generate_library.py arduino
    ```
    In case use esp family.
    ```bash
        ros2 run xicro_pkg generate_library.py esp
    ```
    In case use STM32F411RE
    ```bash
        ros2 run xicro_pkg generate_library.py stm32 stm32f4xx_hal.h
    ```
## Create xicro node
The node will be generated based on setup_xicro.yaml

```bash 
    ros2 run xicro_pkg generate_xicro_node.py argv1
```
 - argv1 : This is the mcu family that you want to use.

    Canbe [arduino , esp , stm32]

  The entry point is add auto by command.

 

## Step to use
- Create xicro library

- Create xicro node

- Upload code contain xicro_library to MCU

- Connect MCU to computer

- check port open 

- run xicro node
