import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SafetyNode(Node):
    def __init__(self):
        super().__init__("safety_node")
        self.subscriber = self.create_subscription(Twist, "/cmd_vel_nav", self.callback, 10)
        self.publisher = self.create_publisher(Twist, "/cmd_vel_safe", 10)
        
    def callback(self, msg):
        msg.linear.x = max(min(msg.linear.x, 1.0), -1.0)
        msg.angular.z = max(min(msg.angular.z, 1.0), -1.0)
        self.publisher.publish(msg)
        
def main():
    rclpy.init()
    node = SafetyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()