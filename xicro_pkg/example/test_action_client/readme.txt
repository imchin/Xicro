1. setup setup_xicro.yaml
    microcontroller:
        idmcu: 1
        namespace: "action_client"
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
        srv_client: [                           ]
        srv_server: [                           ]
        action_client: [          [1,"toggle_sum","xicro_interfaces/Toggle.action",12.00]              ]
        action_server: [                        ]


2. generate node  >>> xicro_node_namespace_ID_xx_mcu_type.py
3. generate library 
4. Open floder Arduino_code in floder contain example arduino_ide code use  for example setup
5. Upload to mcu
6. Open floder scripts in floder contain action_server_sum_toggle_node.py for example setup
7. run action_server_sum_toggle_node.py to open actoin server "toggle_sum" to mcu 
8. connect mcu to computer
9. check permission port  
10. ros2 run xicro_node_namespace_ID_xx_mcu_type.py
11. LED is blink depend on test condition on your modify code


Pass test
- Arduino Uno
- Arduino wifi rev2 
- Arduino mega
- esp32 
- esp8266s