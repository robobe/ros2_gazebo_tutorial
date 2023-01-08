import os
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import xacro

PACKAGE_NAME = "ros2_gazebo_tutorial"
WORLD = "camera.world"
MODEL = "lidar"
SDF = "model.sdf"

def generate_launch_description():
    pkg = get_package_share_directory(PACKAGE_NAME)
    gazebo_pkg = get_package_share_directory('gazebo_ros')
    model_sdf_full_path = os.path.join(pkg, "models", MODEL, "model.sdf")

    sim_time = LaunchConfiguration("sim_time")
    arg_sim_time = DeclareLaunchArgument("sim_time", default_value="true")

    verbose = LaunchConfiguration("verbose")
    arg_verbose = DeclareLaunchArgument("verbose", default_value="true")

    resources = [
        os.path.join(pkg, "worlds")    
    ]

    resource_env = AppendEnvironmentVariable(name="GAZEBO_RESOURCE_PATH", value=":".join(resources))

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    gazebo_pkg, 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'verbose': verbose, "world": WORLD}.items()
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

    spawn_entity_cmd = Node(
        package="gazebo_ros", 
        executable="spawn_entity.py",
        arguments=['-entity', "robot_name_in_model", 
        '-file', model_sdf_full_path,
        '-x', "0",
        '-y', "0",
        '-z', "0.05"],
        output='screen')

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(pkg, "config", "ultrasonic.rviz")],
    )

    link_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name="link2world",
        arguments = ["0", "0", "0.05", "0", "0", "0", "world", "link"]
    )

    ld = LaunchDescription()
    ld.add_action(arg_verbose)
    ld.add_action(arg_sim_time)
    ld.add_action(resource_env)
    ld.add_action(gazebo)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_entity_cmd)
    ld.add_action(rviz)
    ld.add_action(link_tf)
    return ld
