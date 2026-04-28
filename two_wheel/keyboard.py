"""Keyboard teleoperation node for the two-wheel drive stack."""

import sys
import termios
import tty

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


KEY_BINDINGS = {
    '8': (1.0, 0.0, 'forward'),
    '2': (-1.0, 0.0, 'reverse'),
    '4': (0.0, 1.0, 'turn left'),
    '6': (0.0, -1.0, 'turn right'),
    '[A': (1.0, 0.0, 'forward'),
    '[B': (-1.0, 0.0, 'reverse'),
    '[D': (0.0, 1.0, 'turn left'),
    '[C': (0.0, -1.0, 'turn right'),
    ' ': (0.0, 0.0, 'stop'),
}


class KeyboardNode(Node):
    """Publish teleop commands from keyboard input."""

    def __init__(self) -> None:
        """Configure publishers and runtime parameters."""
        super().__init__('keyboard_node')

        command_topic = (
            self.declare_parameter('command_topic', '/keyboard_cmd')
            .get_parameter_value()
            .string_value
        )
        self.linear_speed = (
            self.declare_parameter('linear_speed', 1.0)
            .get_parameter_value()
            .double_value
        )
        self.angular_speed = (
            self.declare_parameter('angular_speed', 1.0)
            .get_parameter_value()
            .double_value
        )
        self.debug_mode = (
            self.declare_parameter('debug_mode', False)
            .get_parameter_value()
            .bool_value
        )

        self.publisher = self.create_publisher(Twist, command_topic, 10)
        self.get_logger().info(
            'Keyboard control ready (8246 / arrow keys / space=stop / q=quit)'
        )

    def get_key(self) -> str:
        """Read a single raw keypress, including arrow keys."""
        file_descriptor = sys.stdin.fileno()
        original_settings = termios.tcgetattr(file_descriptor)

        try:
            tty.setraw(file_descriptor)
            key = sys.stdin.read(1)
            if key == '\x1b':
                key = sys.stdin.read(2)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, original_settings)

        return key

    def build_message(self, key: str) -> Twist | None:
        """Convert a keypress into a motion command."""
        binding = KEY_BINDINGS.get(key)
        if binding is None:
            return None

        linear_direction, angular_direction, label = binding
        message = Twist()
        message.linear.x = linear_direction * self.linear_speed
        message.angular.z = angular_direction * self.angular_speed

        if self.debug_mode:
            self.get_logger().info(f'Key command: {label}')

        return message

    def run(self) -> None:
        """Block on stdin and publish commands until the node is stopped."""
        while rclpy.ok():
            key = self.get_key()
            if key == 'q':
                self.get_logger().warning('Quitting keyboard node.')
                break

            message = self.build_message(key)
            if message is not None:
                self.publisher.publish(message)


def main() -> None:
    """Run the keyboard teleoperation node."""
    rclpy.init()
    node = KeyboardNode()

    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
