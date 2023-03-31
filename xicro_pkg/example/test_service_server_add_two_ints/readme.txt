1. setup setup_xicro.yaml
    example setup:
        microcontroller:
            idmcu: 1
            namespace: "service_server_add"
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
            srv_server: [             [1,"add_two_ints","example_interfaces/AddTwoInts.srv",5.00]              ]
            action_client: [                        ]
            action_server: [                        ]

2. generate node  >>> xicro_node_namespace_ID_xx_mcu_type.py
3. generate library 
4. Open floder Arduino_code in floder contain example arduino_ide code use  for example setup
5. Upload to mcu
6. connect mcu to computer
7. check permission port 
8. run xicro_node_namespace_ID_xx_mcu_type.py
9. check ros2 service list
    test service server 
    call from terminal
        ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 26,b: 16}"

Pass test
- Arduino Uno
- Arduino wifi rev2 
- Arduino mega
- esp32 
- esp8266