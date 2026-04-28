"""Safety node for constraining drive commands."""

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

from two_wheel.control import clamp_twist


class SafetyNode(Node):
    """Clamp incoming drive commands before they reach the motors."""

    def __init__(self) -> None:
        """Create the safety pipeline between nav and actuator topics."""
        super().__init__('safety_node')

        input_topic = (
            self.declare_parameter('input_topic', '/cmd_vel_nav')
            .get_parameter_value()
            .string_value
        )
        output_topic = (
            self.declare_parameter('output_topic', '/cmd_vel_safe')
            .get_parameter_value()
            .string_value
        )
        axis_limit = (
            self.declare_parameter('axis_limit', 1.0)
            .get_parameter_value()
            .double_value
        )

        self.axis_limit = axis_limit
        self.subscription = self.create_subscription(
            Twist,
            input_topic,
            self.callback,
            10,
        )
        self.publisher = self.create_publisher(Twist, output_topic, 10)

    def callback(self, message: Twist) -> None:
        """Publish a clamped copy of the incoming command."""
        safe_linear_x, safe_angular_z = clamp_twist(
            message.linear.x,
            message.angular.z,
            limit=self.axis_limit,
        )

        safe_message = Twist()
        safe_message.linear.x = safe_linear_x
        safe_message.angular.z = safe_angular_z
        self.publisher.publish(safe_message)


def main() -> None:
    """Run the safety node."""
    rclpy.init()
    node = SafetyNode()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
