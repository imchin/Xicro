1. setup setup_xicro.yaml
    example setup:
        microcontroller:
            idmcu: 1
            namespace: "toggle_led"
            generate_library_Path: "arduino/libraries"  
            connection:
                type: "UART"   # ["UART","UDP"]
                serial_port: "/dev/ttyACM0"  # for UART
                baudrate: 57620  # for UART
                ip_address_mcu: ""  # for UDP 
                udp_port_mcu: 0  # for UDP

            ros: # setup ros is reference from microcontroller example publisher is mean microcontroller publish to ros network
                publisher:  [                           ]
                subscriber: [            [1,"toggle","std_msgs/Bool.msg"]               ]
                srv_client: [                           ]
                srv_server: [                           ]
                action_client: [                        ]
                action_server: [                        ]

2. generate node  >>> xicro_node_namespace_ID_xx_mcu_type.py
3. generate library 
4. Open floder Arduino_code in floder contain example arduino_ide code use  for example setup
5. Upload to mcu
6. Open floder scripts in floder contain toggle_node.py for example setup
7. run toggle_node.py to publish topic "toggle" to mcu 
8. connect mcu to computer
9. check permission port  
10. ros2 run xicro_node_namespace_ID_xx_mcu_type.py
11. LED on mcu LED flashing at a same constant frequency (toggle_node.py)


Pass test
- Arduino Uno
- Arduino wifi rev2 
- Arduino mega
- esp32 
- esp8266