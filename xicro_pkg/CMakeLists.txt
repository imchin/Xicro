cmake_minimum_required(VERSION 3.5)
project(xicro_pkg)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

################ FIND DEPENDENCIES  #################
find_package(ament_cmake REQUIRED)		# cpp (optional)
find_package(rclcpp REQUIRED)			# cpp (optional)
find_package(ament_cmake_python REQUIRED)   	# python (optional)
find_package(rclpy REQUIRED)                	# python (optional)
######################################################

# Install Python Module
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  scripts/gui_xicro.py
#xicro
  scripts/generate_library.py
  scripts/generate_xicro_node.py
  scripts/xicro_node_test_pub_ID_1_stm32.py
  scripts/xicro_node_sub_N_pub_ID_1_stm32.py
#orcix
  DESTINATION lib/${PROJECT_NAME}
)

################ INSTALL LAUNCH, ETC #################
install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME})
ament_package()
