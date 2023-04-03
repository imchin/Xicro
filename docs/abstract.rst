Abstract
========

The Robot Operating System (ROS) is a popular open-source framework for developing robotic systems. ROS2, the latest version of the framework, is designed to support real-time, distributed systems, and has become a popular choice for robotics researchers and developers. However, one limitation of ROS2 is that it is designed to run on high-performance computers, which can be expensive and impractical for many robotics applications.

To address this limitation, several middleware solutions have been developed to allow ROS2 to run on microcontrollers with limited resources. One such solution is MicroROS, a middleware that provides a communication layer between microcontrollers and ROS2. However, MicroROS is limited to microcontrollers with 32-bit architecture, and cannot be used with lower-bit architecture such as AVR. This limitation poses a challenge for developers who want to use ROS2 with low-cost, low-power microcontrollers that are widely available in the market.

To overcome this limitation, a software library is needed that allows any-bit architecture microcontroller to connect with ROS2 using UART or UDP. This library should provide a lightweight and efficient communication protocol that is optimized for microcontrollers with limited resources. By enabling low-cost microcontrollers to connect with ROS2, this library can help democratize access to ROS2 and make it more accessible to developers working on low-cost robotics projects.
