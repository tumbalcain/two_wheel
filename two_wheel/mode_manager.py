import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ModeManager(Node):
    def __init__(self):
        super().__init__("mode_manager_node")
        self.subscriber = self.create_subscription(Twist, "/keyboard_cmd",  self.callback, 10)
        self.publisher = self.create_publisher(Twist, "/cmd_vel_nav", 10)
        
        self.get_logger().info("Mode manager initiated.")
        
    def callback(self, msg):
        self.publisher.publish(msg)
    
def main():
    rclpy.init()
    node = ModeManager()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()