"""Convert safe twist commands into differential wheel speeds."""

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

from two_wheel.control import build_wheel_command


class MotorBridge(Node):
    """Translate drive commands into left and right wheel outputs."""

    def __init__(self) -> None:
        """Create subscriptions and publishers for wheel-speed output."""
        super().__init__('motor_bridge_node')

        input_topic = (
            self.declare_parameter('input_topic', '/cmd_vel_safe')
            .get_parameter_value()
            .string_value
        )
        output_topic = (
            self.declare_parameter('output_topic', '/wheel_speed')
            .get_parameter_value()
            .string_value
        )
        max_wheel_speed = (
            self.declare_parameter('max_wheel_speed', 1.0)
            .get_parameter_value()
            .double_value
        )

        self.max_wheel_speed = max_wheel_speed
        self.subscription = self.create_subscription(
            Twist,
            input_topic,
            self.callback,
            10,
        )
        self.publisher = self.create_publisher(Float32MultiArray, output_topic, 10)

        self.get_logger().info(f'Motor bridge routing {input_topic} -> {output_topic}.')

    def callback(self, message: Twist) -> None:
        """Publish normalized wheel speeds derived from a twist command."""
        left_speed, right_speed = build_wheel_command(
            message.linear.x,
            message.angular.z,
            limit=self.max_wheel_speed,
        )

        wheel_message = Float32MultiArray()
        wheel_message.data = [left_speed, right_speed]
        self.publisher.publish(wheel_message)


def main() -> None:
    """Run the motor bridge node."""
    rclpy.init()
    node = MotorBridge()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
