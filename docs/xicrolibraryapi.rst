Xicro library API
=================
After making settings in the file setup_xicro.yaml
and successfully generated a Xicro node and Xicro library.
We will need to deploy the Xicro library to the microcontroller.




* To use the generated Xicro library, you must use the Xicro node file created with the configuration file. Only setup_xicro.yaml is the same. 


Initialize Xicro library
************************
The xicro library has to be set up.

1. Declare the object xicro before calling Void Setup(). 

    .. image:: pic/declare.png
        :width: 420
        :height: 120
        :alt: Alternative text
        :align: center

2. Setup Xicro uart

    .. image:: pic/setuart.png
        :width: 320
        :height: 100
        :alt: Alternative text
        :align: center

    1. Set the communication baudrate to match the setting in the file. setup_xicro.yaml.
    
    2. Enter the address of the UART to register the xicro library. (function begin())
    
3. Execute xicro process

    .. image:: pic/spin.png
        :width: 300
        :height: 80
        :alt: Alternative text
        :align: center

    Xicro process requires computation It is therefore defined that the function Spin_node() must always be in While(1).

    Warning!! 

        For maximum efficiency when programming embedded systems, you should not do anything that consumes too many resources or computation time. in while(1)
    
    

Publish
*******

    .. image:: tutorial_pic/step1.jpg
    :width: 500
    :height: 350
    :alt: Alternative text
    :align: center

Subscribe
*********

Service client
**************

Service server
**************

Action client
*************

Action server
*************