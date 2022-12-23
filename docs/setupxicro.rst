Setup Xicro
===========


Configured yaml
***************
.. code-block:: sh

    cd ~/xxx_ws/src/Xicro/xicro_pkg/config     # cd to floder contain setup_xicro.yaml
    code setup_xicro.yaml

setup_xicro.yaml is contain 

1. Idmcu : It sets the ID of the MCU for the system Xicro.

    The mcu Id may range from 0 to 15. 
    
2. Namespace : This is the name of the file that will be created.

3. Port : Name open port of MCU

4. generate_library_Path : Is the path for creating .h and .cpp files. Xicro will create a folder with files at the path.

    Path reference from ~/

5. Baudrate : Can config baudrate
    Baudrate affects the data transmission rate. Can use <=2000000
    
    \**Recommended at 115200.



6. Setup_Publisher : Configuration for publishing topic from MCU to ROS2.
    In format : [ [ID_topic,Name_topic,Interface],[ID_topic_2,Name_topic_2,Interface_2],.......]
        1. ID_topic : It sets the ID of the topic_publish for the system Xicro.
            
            The ID_topic Id may range from 0 to 255.
        2. Name_topic : Specify the topic name you want MCU to publish to ROS2.
        3. Interface : variable interfacefile configuration for use in the topic 
            Is contain 2 part in format 

            
             "(The name of the package that contains the interface file)/(Name_of_fileinterface).msg" 

7. Setup_Subscriber : Configuration for subscribe topic from  ROS2 to MCU.
    In format : [ [ID_topic,Name_topic,Interface],[ID_topic_2,Name_topic_2,Interface_2],.......]
  
    1. ID_topic : It sets the ID of the topic_subscribe for the system Xicro.
        
        The ID_topic Id may range from 0 to 255.
    2. Name_topic : Specify the topic name you want MCU subscribe from ROS2.
    3. Interface : variable interfacefile configuration for use in the topic 
        Is contain 2 part in format 

        
            "(The name of the package that contains the interface file)/(Name_of_fileinterface).msg" 

8. Setup_Srv_client : Configuration for service client. 
    In format : [ [ID_service,Name_service,Interface,time_out],[ID_service_2,Name_service_2,Interface_2,time_out_2],.......]
     
    1. ID_service : It sets the ID of the service_client for the system Xicro.
        
        The ID_service Id may range from 0 to 255.
    2. Name_service : Specify the servive name you want MCU service call to ROS2.
    3. Interface : variable interfacefile configuration for use in the service
        Is contain 2 part in format 

        
            "(The name of the package that contains the interface file)/(Name_of_fileinterface).srv" 
    4. time_out : Limit the maximum service usage time. (In type float)

9. Setup_Srv_server : Configuration for service server. 
    In format : [ [ID_service,Name_service,Interface,time_out],[ID_service_2,Name_service_2,Interface_2,time_out_2],.......]
      
    1. ID_service : It sets the ID of the service_server for the system Xicro.
        
        The ID_service Id may range from 0 to 255.
    2. Name_service : Specify the servive name you want  ROS2 service call to MCU.
    3. Interface : variable interfacefile configuration for use in the service
        Is contain 2 part in format 

        
            "(The name of the package that contains the interface file)/(Name_of_fileinterface).srv" 
    4. time_out : Limit the maximum service usage time. (In type float)

10. Setup_Action_client : Configuration for action client. 
    In format : [ [ID_action,Name_action,Interface,time_out],[ID_action_2,Name_action_2,Interface_2,time_out_2],.......]
    
    1. ID_action : It sets the ID of the action_client for the system Xicro
   
         The ID_action Id may range from 0 to 255.
    2. Name_action : Specify the action name you want MCU action send_goal to ROS2.
    3. Interface : variable interfacefile configuration for use in the action
        Is contain 2 part in format 

        
            "(The name of the package that contains the interface file)/(Name_of_fileinterface).action" 
    4. time_out : Limit the maximum action usage time. (In type float)        
      
11. Setup_Action_server : Configuration for action server. 
    In format : [ [ID_action,Name_action,Interface,time_out],[ID_action_2,Name_action_2,Interface_2,time_out_2],.......]
    
    1. ID_action : It sets the ID of the action_server for the system Xicro
   
         The ID_action Id may range from 0 to 255.
    2. Name_action : Specify the action name you want ROS2 action send_goal to MCU.
    3. Interface : variable interfacefile configuration for use in the action
        Is contain 2 part in format 

        
            "(The name of the package that contains the interface file)/(Name_of_fileinterface).action" 
    4. time_out : Limit the maximum action usage time. (In type float)        
      
When setting up the system as desired, run colcon build.

.. code-block:: sh

  cd ~/xxx_ws          # cd to your workspace
  colcon build


Generate Xicro node 
*******************

The node will be generated based on setup_xicro.yaml

.. code-block:: sh

    cd ~/xxx_ws          # cd to your workspace
    colcon build
    ros2 run xicro_pkg generate_xicro_node.py argv1  // Xicro node will be created at path ~xxx_ws/scr/Xicro/xicro_pkg/scripts
   
  
argv1 : This is the mcu family that you want to use, Can be [arduino , esp , stm32]

.. code-block:: sh

    cd ~/xxx_ws          # cd to your workspace
    colcon build

After generate xicro node automatically is added entry point. 

     In format : "xicro_node\_"+namespace+"_ID\_"+setup_id+"_"+mcu_family+".py"

The xicro node will have the following capabilities: setup_xicro.yaml only

.. code-block:: sh

  cd ~/xxx_ws          # cd to your workspace
  colcon build

Generate library for microcontroller
************************************
The library will be generated based on setup_xicro.yaml
   
.. code-block:: sh

    cd ~/xxx_ws          # cd to your workspace
    colcon build
    ros2 run xicro_pkg generate_library.py argv1 argv2 // Xicro library .h , .cpp will be created at $generate_library_Path in setup_xicro.yaml
    
argv1 : This is the mcu family that you want to use.

    
argv2  : HAL library
    Ignore it if you don't use the stm2 family. 

    .. code-block:: sh

        ros2 run xicro_pkg generate_library.py stm32 stm32l0xx_hal.h  // Exmaple generate for stm32L0xx
        ros2 run xicro_pkg generate_library.py arduino  // Exmaple generate for arduino family.
        ros2 run xicro_pkg generate_library.py esp  // Exmaple generate for esp family.

