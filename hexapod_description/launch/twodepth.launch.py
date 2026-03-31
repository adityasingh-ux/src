from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    qos = LaunchConfiguration('qos')
    localization = LaunchConfiguration('localization')

    parameters={
        'frame_id': 'base_footprint',
        'use_sim_time': use_sim_time,
        'subscribe_depth': True,
        'use_action_for_goal': True,
        'qos_image': qos,
        'qos_imu': qos,
        'Reg/Force3DoF': 'true',
        'Optimizer/GravitySigma': '0',  # Disable imu constraints (we are already in 2D)
        'Kp/MinDepth': '0.0',  # Set the minimum depth for loop closure detection
        'Kp/MaxDepth': '4.0',  # Set the maximum depth for loop closure detection
        'Kp/MaxDepthClose': '1.0'  # Set the maximum depth for loop closure detection in close range
    }

    remappings = [
        ('rgb/image', '/camera/image_raw'),
        ('rgb/camera_info', '/camera/camera_info'),
        ('depth/image', '/camera/depth/image_raw'),
        # ('rgb/image2', '/camera2/image_raw'),  # Add remappings for the second camera
        # ('rgb/camera_info2', '/camera2/camera_info'),
        # ('depth/image2', '/camera2/depth/image_raw')
    ]

    return LaunchDescription([

        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        
        DeclareLaunchArgument(
            'qos', default_value='2',
            description='QoS used for input sensor topics'),
            
        DeclareLaunchArgument(
            'localization', default_value='false',
            description='Launch in localization mode.'),

      Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']), # This will delete the previous database (~/.ros/rtabmap.db)
            
        # Localization mode:
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters,
              {'Mem/IncrementalMemory':'False',
               'Mem/InitWMWithAllNodes':'True'}],
            remappings=remappings),

        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            parameters=[parameters],
            remappings=remappings),
        # Node(
    ])

