Xicro
=====


* If you are looking for a way to establish some communication between a microcontroller and ROS2 network, you probably came across "micro-ROS". Unlike its predecessor (rosserial), micro-ROS mostly relies on the use of Real-Time Operating System (RTOS), which allows developers to implement concurrent tasks in multi-threading fashion. A software engineer can write an embedded program like a piece of software. However, RTOS requires microcontroller's memeory. Therefore, micro-ROS can be applied to a limited number of microcontrollers with RTOS. You can no longer use a simple microcontroller like Arduino Uno with ROS2 using micro-ROS. (See https://micro.ros.org/docs/overview/hardware/). This seems odd because rosserial in ROS(1) was very versatile and can be applied to any microcontrollers without the complication of RTOS (if configured properly).
* Using the same principle as rosserial, we come up with "xicro" (not to be confused with "xacro"). xicro allows the developers to use the generated libraries for the microcontrollers as well as auto-generated node that intrepreter information from/to the microcontrollers via UART.

.. toctree::
      :maxdepth: 1
      :caption: Getting Started

      abstract.rst
      installation.rst
      setupxicro.rst
      xicrolibraryapi.rst