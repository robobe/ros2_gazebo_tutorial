#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu
import tf_transformations
from math import degrees
TOPIC_IMU = "/imu/data"

class MyNode(Node):
    def __init__(self):
        node_name="minimal"
        super().__init__(node_name)
        self.create_subscription(Imu, TOPIC_IMU, self.__imu_handler, qos_profile=qos_profile_sensor_data)
        self.get_logger().info("Hello ROS2")

    def __imu_handler(self, msg: Imu):
        euler = tf_transformations.euler_from_quaternion([
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w
        ])
        deg_euler = [degrees(r) for r in euler]
        self.get_logger().info(f"{deg_euler}")

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()