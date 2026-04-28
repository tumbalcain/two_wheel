"""Socket bridge for sending wheel commands to the RoboRIO."""

import json
import socket

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class SocketNode(Node):
    """Forward wheel-speed commands to a remote RoboRIO over TCP."""

    def __init__(self) -> None:
        """Create the subscription and initialize socket parameters."""
        super().__init__('socket_node')

        input_topic = (
            self.declare_parameter('input_topic', '/wheel_speed')
            .get_parameter_value()
            .string_value
        )
        self.roborio_ip = (
            self.declare_parameter('roborio_ip', '127.0.0.1')
            .get_parameter_value()
            .string_value
        )
        self.roborio_port = (
            self.declare_parameter('roborio_port', 12345)
            .get_parameter_value()
            .integer_value
        )
        self.socket_timeout = (
            self.declare_parameter('socket_timeout', 1.0)
            .get_parameter_value()
            .double_value
        )
        self.sock: socket.socket | None = None

        self.subscription = self.create_subscription(
            Float32MultiArray,
            input_topic,
            self.callback,
            10,
        )

        self.get_logger().info(
            f'Socket bridge ready for {self.roborio_ip}:{self.roborio_port}.'
        )
        self._connect()

    def _connect(self) -> None:
        """Open a TCP connection to the RoboRIO if needed."""
        if self.sock is not None:
            return

        try:
            self.sock = socket.create_connection(
                (self.roborio_ip, self.roborio_port),
                timeout=self.socket_timeout,
            )
        except OSError as error:
            self.sock = None
            self.get_logger().warning(
                f'Unable to connect to RoboRIO at '
                f'{self.roborio_ip}:{self.roborio_port}: {error}'
            )
            return

        self.get_logger().info('Connected to RoboRIO.')

    def _close_socket(self) -> None:
        """Close the active socket connection, if one exists."""
        if self.sock is None:
            return

        try:
            self.sock.close()
        finally:
            self.sock = None

    def callback(self, message: Float32MultiArray) -> None:
        """Serialize and send the current wheel command."""
        if len(message.data) < 2:
            self.get_logger().warning(
                'Ignoring wheel command with fewer than two values.'
            )
            return

        if self.sock is None:
            self._connect()
            if self.sock is None:
                return

        payload = {
            'leftOne': float(message.data[0]),
            'leftTwo': float(message.data[0]),
            'rightOne': float(message.data[1]),
            'rightTwo': float(message.data[1]),
        }

        try:
            self.sock.sendall(json.dumps(payload).encode('utf-8') + b'\n')
        except OSError as error:
            self.get_logger().error(f'Socket send failed: {error}')
            self._close_socket()

    def destroy_node(self) -> bool:
        """Close the socket before shutting down the node."""
        self._close_socket()
        return super().destroy_node()


def main() -> None:
    """Run the socket bridge node."""
    rclpy.init()
    node = SocketNode()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
