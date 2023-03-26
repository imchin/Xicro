1. setup setup_xicro.yaml
    microcontroller:
        idmcu: 1
        namespace: "service_client_add"
        generate_library_Path: "arduino/libraries"  
        connection:
            type: "UART"   # ["UART","UDP"]
            serial_port: "/dev/ttyACM0"  # for UART
            baudrate: 57620  # for UART
            ip_address_mcu: ""  # for UDP 
            udp_port_mcu: 0  # for UDP

    ros: # setup ros is reference from microcontroller example publisher is mean microcontroller publish to ros network
        publisher:  [                           ]
        subscriber: [                           ]
        srv_client: [             [1,"add_two_ints","example_interfaces/AddTwoInts.srv",5.00]              ]
        srv_server: [                           ]
        action_client: [                        ]
        action_server: [                        ]


2. generate node  >>> xicro_node_namespace_ID_xx_mcu_type.py
3. generate library 
4. Open floder Arduino_code in floder contain example arduino_ide code use  for example setup
5. Upload to mcu
6. Open floder scripts in floder contain add_two_ints_server_node for example setup
7. run add_two_ints_server_node to open service server "add_two_ints" to mcu 
8. connect mcu to computer
9. check permission port  
10. ros2 run xicro_node_namespace_ID_xx_mcu_type.py
11. LED is blink depend on test condition on your modify code


Pass test
- Arduino Uno
- Arduino wifi rev2 
- Arduino mega
- esp32 
- esp8266