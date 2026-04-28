import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import socket
import json

ROBORIO_IP = "127.0.0.1" # CHANGE THIS
PORT = 12345

class SocketNode(Node):
    def __init__(self):
        super().__init__("socket_node")
        self.subscriber = self.create_subscription(Float32MultiArray, "/wheel_speed", self.callback, 10)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ROBORIO_IP, PORT))
        
        self.get_logger().info("Socket initiated.")
        
        self.get_logger().info("Connected to RoboRIO")
    
    def callback(self, msg):
        data = {
            "leftOne":msg.data[0],
            "leftTwo":msg.data[0],
            "rightOne":msg.data[1],
            "rightTwo":msg.data[1]
        }
        try:
            self.sock.send((json.dumps(data) + "\n").encode())
        except:
            self.get_logger().error("Socket send failed.")
            
def main():
    rclpy.init()
    node = SocketNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()