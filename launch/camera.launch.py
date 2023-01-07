from launch import LaunchDescription
import os
from math import pi
from ament_index_python.packages import get_package_share_directory
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

PACKAGE = "ros2_gazebo_tutorial"
WORLD = "camera.world"
MODEL="camera2"
SDF="model.sdf"

def generate_launch_description():
    ld = LaunchDescription()

    pkg = get_package_share_directory(PACKAGE)
    gazebo_pkg = get_package_share_directory('gazebo_ros')
    
    verbose = LaunchConfiguration("verbose")
    arg_gazebo_verbose = DeclareLaunchArgument("verbose", default_value="true")
    world = LaunchConfiguration("world")
    arg_gazebo_world = DeclareLaunchArgument("world", default_value=WORLD)
    sim_time = LaunchConfiguration("sim_time")
    arg_sim_time = DeclareLaunchArgument("sim_time", default_value="true")

    resources = [os.path.join(pkg, "worlds")]

    resource_env = AppendEnvironmentVariable(
        name="GAZEBO_RESOURCE_PATH", value=":".join(resources)
    )

    models = [os.path.join(pkg, "models")]

    models_env = AppendEnvironmentVariable(
        name="GAZEBO_MODEL_PATH", value=":".join(models)
    )

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    gazebo_pkg, 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'verbose': verbose, "world": world}.items()
             )

    robot_description_path = os.path.join(pkg, "models", MODEL, SDF)
    doc = xacro.parse(open(robot_description_path))
    xacro.process_doc(doc)

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'use_sim_time': sim_time, 
                'robot_description': doc.toxml()
            }
        ]
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", "demo", "-topic", "robot_description", "-z", "0.5"],
        output="screen",
    )

    tf = Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            output="screen",
            arguments=["0","0","0","0","0","0","world","camera_link"]
            
        )

    tf_camera_optical = Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            output="screen",
            arguments=["0.05","0","0",str(-pi/2),"0",str(-pi/2),"camera_link","camera_optical"]
        )

    rviz_node = Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=['-d' + os.path.join(pkg, 'config', 'camera.rviz')]
    )

    ld.add_action(models_env)
    ld.add_action(resource_env)
    ld.add_action(arg_gazebo_verbose)
    ld.add_action(arg_gazebo_world)
    ld.add_action(arg_sim_time)
    ld.add_action(gazebo)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_entity)
    ld.add_action(tf)
    ld.add_action(tf_camera_optical)
    ld.add_action(rviz_node)
    return ld