
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

## setup_xicro.yaml is contain : (Idmcu,Namespace,Port,generate_library_Path,Baudrate,Setup_Publisher,Setup_Subscriber)


 - ### Idmcu : It sets the ID of the MCU for the system Xicro.

    The mcu Id may range from 0 to 15. 
  
 - ### Namespace : This is the name of the file that will be created.
  

 - ### Port : Name open port MCU
   

 - ### generate_library_Path : Is the path for creating .h and .cpp files.
    Xicro will create a folder with files at the path.

 - ### Baudrate : Can config baudrate
    Baudrate affects the data transmission rate.
    
    **Recommended at 115200.

 
  - ### Setup_Publisher : Configuration for publishing topic from MCU to ROS2
    Informat : [ [ID_topic,Name_topic,Interface],[ID_topic_2,Name_topic_2,Interface_2],.......]
    
    Setup_Publisher is contain 3 part  [ID_topic,Name_topic,interfacefile]
    - #### ID_topic : It sets the ID of the topic_publish for the system Xicro.
        The ID_topic Id may range from 0 to 255.
    
    - #### Name_topic : Specify the topic name you want MCU to publish to ROS2.
    
    - #### Interface : variable interfacefile configuration for use in the topic 
        Is contain 2 part in format "(The name of the package that contains the interface file)/(Name_of_fileinterface_).msg" 



  - ### Setup_Subscriber : Configuration for subscribe topic from  ROS2 to MCU.
    Informat : [ [ID_topic,Name_topic,Interface],[ID_topic_2,Name_topic_2,Interface_2],.......]
    
    Setup_Subscriber is contain 3 part  [ID_topic,Name_topic,interfacefile]
    - #### ID_topic : It sets the ID of the topic_subscribe for the system Xicro.
        The ID_topic Id may range from 0 to 255.
    
    - #### Name_topic : Specify the topic name you want MCU subscribe from ROS2.
    
    - #### Interface : Variable interfacefile configuration for use in the topic 
        Is contain 2 part in format "(The name of the package that contains the interface file)/(Name_of_fileinterface_).msg" 


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

    ### After running the command, VScode will display the node that was created.

    Delete line 11  "!Delete this line to verify the code." and save it 
  The entry point is add auto by command.

 

## Step to use
- Create xicro library

- Create xicro node

- Upload code contain xicro_library to MCU

- Connect MCU to computer

- check permission port open 
  ```bash
  chown $USERNAME /port     #Changing permissions port 
  ```
- run xicro node

# Now STM32 support Only STM32F411RE
