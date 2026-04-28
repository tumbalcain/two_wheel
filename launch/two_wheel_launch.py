from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    mode_manager_node = Node(
        package='two_wheel',
        executable='mode_manager',
        name='mode_manager_node',
        output='screen',
    )
    
    motor_bridge_node = Node(
        package='two_wheel',
        executable='motor_bridge',
        name='motor_bridge_node',
        output='screen',
    )
    
    safety_node = Node(
        package='two_wheel',
        executable='safety',
        name='safety_node',
        output='screen',
    )
    
    socket_node = Node(
        package='two_wheel',
        executable='socket',
        name='socket_node',
        output='screen',
    )

    return LaunchDescription([
        mode_manager_node,
        motor_bridge_node,
        safety_node,
        socket_node
    ])