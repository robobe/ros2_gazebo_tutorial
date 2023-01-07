cmake_minimum_required(VERSION 3.8)
project(ros2_gazebo_tutorial)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(
  DIRECTORY launch worlds models config description
  DESTINATION share/${PROJECT_NAME}
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
    ros2_gazebo_tutorial/entity_state.py
    ros2_gazebo_tutorial/imu_demo.py
    DESTINATION lib/${PROJECT_NAME}
    )

ament_package()
