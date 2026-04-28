import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class MotorBridge(Node):
    def __init__(self):
        super().__init__("motor_bridge_node")
        self.subscriber = self.create_subscription(Twist, "/cmd_vel_safe", self.callback, 10)
        self.publisher = self.create_publisher(Float32MultiArray, "/wheel_speed", 10)
        
        self.get_logger().info("Motor bridge initiated.")
    
    def callback(self, msg):
        left = msg.linear.x - msg.angular.z
        right = msg.linear.x + msg.angular.z
        
        out = Float32MultiArray()
        out.data = [left, right]
        self.publisher.publish(out)
        
def main():
    rclpy.init()
    node = MotorBridge()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()