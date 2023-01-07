#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from rclpy.qos import qos_profile_sensor_data

TOPIC_RANGE = "/ultrasonic_sensor_1"

class MyNode(Node):
    def __init__(self):
        node_name="ultrasonic_demo"
        super().__init__(node_name)
        self.create_subscription(Range, TOPIC_RANGE, self.__range_handler, qos_profile=qos_profile_sensor_data)
        self.get_logger().info("Hello ultrasonic")

    def __range_handler(self, msg: Range):
        self.get_logger().info(str(msg.range))

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()