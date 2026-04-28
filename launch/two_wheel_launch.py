"""Launch the core two-wheel ROS 2 nodes."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Build the launch description for the control pipeline."""
    roborio_ip = LaunchConfiguration('roborio_ip')
    roborio_port = LaunchConfiguration('roborio_port')

    return LaunchDescription([
        DeclareLaunchArgument(
            'roborio_ip',
            default_value='127.0.0.1',
            description='IP address for the RoboRIO socket bridge.',
        ),
        DeclareLaunchArgument(
            'roborio_port',
            default_value='12345',
            description='TCP port for the RoboRIO socket bridge.',
        ),
        Node(
            package='two_wheel',
            executable='mode_manager',
            name='mode_manager_node',
            output='screen',
        ),
        Node(
            package='two_wheel',
            executable='motor_bridge',
            name='motor_bridge_node',
            output='screen',
        ),
        Node(
            package='two_wheel',
            executable='safety',
            name='safety_node',
            output='screen',
        ),
        Node(
            package='two_wheel',
            executable='socket',
            name='socket_node',
            output='screen',
            parameters=[{
                'roborio_ip': roborio_ip,
                'roborio_port': roborio_port,
            }],
        ),
    ])
