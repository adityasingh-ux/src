import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_mr_robot_desc = get_package_share_directory('hexapod_description')

    world_path= get_package_share_directory("hexapod_description")+"/worlds/obs.world"


    gazebo=IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('ros_gz_sim'), '/launch/gz_sim.launch.py']),launch_arguments={
                    # 'gz_args' : [world_path + " -v 4"] , 'on_exit_shutdown' : 'true'
                    'gz_args' : [world_path] , 'on_exit_shutdown' : 'true'

                }.items()
    )

    # launch GZ Sim with empty world
    # gz_sim = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource(
    #                 os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
    #             ),
    #             launch_arguments={'gz_args': '-r empty.sdf'}.items()     
    #         )
    
    # spawn robot with rviz
    robot = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(pkg_mr_robot_desc, 'launch', 'robot.launch.py')
                )
            )

    return LaunchDescription([
        gazebo,
        robot
    ])