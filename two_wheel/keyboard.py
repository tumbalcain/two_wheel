import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import Twist
import sys, termios, tty

class KeyboardNode(Node):
    def __init__(self):
        super().__init__("keyboard_node")
        self.publisher = self.create_publisher(Twist, "/keyboard_cmd", 10)
        self.get_logger().info("Keyboard control ready (8246/Arrow Keys)")
        self.debug_mode = False
        
    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            
            if ch == "\x1b":
                ch = sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
    
    def run(self):
        while rclpy.ok():
            key = self.get_key()
            msg = Twist()
            
            if key == "8":
                msg.linear.x = 1.0
                if self.debug_mode == True:
                    self.get_logger().info("Key 8 Pressed.")
            elif key == "2":
                msg.linear.x = -1.0
                if self.debug_mode == True:
                    self.get_logger().info("Key 2 Pressed.")
            elif key == "4":
                msg.angular.z = 1.0
                if self.debug_mode == True:
                    self.get_logger().info("Key 4 Pressed.")
            elif key == "6":
                msg.angular.z = -1.0
                if self.debug_mode == True:
                    self.get_logger().info("Key 6 Pressed.")
            elif key == '[A':
                msg.linear.x = 1.0
                if self.debug_mode == True:
                    self.get_logger().info("Up Arrow Key Pressed.")
            elif key == '[B':
                msg.linear.x = -1.0
                if self.debug_mode == True:
                    self.get_logger().info("Down Arrow Key Pressed.")
            elif key == '[D':
                msg.angular.z = 1.0
                if self.debug_mode == True:
                    self.get_logger().info("Left Arrow Key Pressed.")
            elif key == '[C':
                msg.angular.z = -1.0
                if self.debug_mode == True:
                    self.get_logger().info("Right Arrow Key Pressed.")
            elif key == "q":
                self.get_logger().warn("Quitting keyboard node...")
                break
            
            self.publisher.publish(msg)
            
def main():
    rclpy.init()
    node = KeyboardNode()
    node.run()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()