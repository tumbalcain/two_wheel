"""Mode-management node for routing teleop commands."""

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


class ModeManager(Node):
    """Pass commands from the selected input topic to the active control topic."""

    def __init__(self) -> None:
        """Create subscriptions and publishers for mode routing."""
        super().__init__('mode_manager_node')

        input_topic = (
            self.declare_parameter('input_topic', '/keyboard_cmd')
            .get_parameter_value()
            .string_value
        )
        output_topic = (
            self.declare_parameter('output_topic', '/cmd_vel_nav')
            .get_parameter_value()
            .string_value
        )

        self.subscription = self.create_subscription(
            Twist,
            input_topic,
            self.callback,
            10,
        )
        self.publisher = self.create_publisher(Twist, output_topic, 10)

        self.get_logger().info(f'Mode manager routing {input_topic} -> {output_topic}.')

    def callback(self, message: Twist) -> None:
        """Forward the incoming command unchanged."""
        self.publisher.publish(message)


def main() -> None:
    """Run the mode manager node."""
    rclpy.init()
    node = ModeManager()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
