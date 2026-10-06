import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    parameters = [{
        'frame_id': 'base_footprint',
        'subscribe_depth': True,
        'subscribe_rgb': True,
        'subscribe_scan': False,
        'approx_sync': True,
        'use_sim_time': True,
        'queue_size': 30,
        # RTAB-Map core parameters
        'RGBD/LinearUpdate': '0.05',
        'RGBD/AngularUpdate': '0.05',
        'RGBD/OptimizeFromGraphEnd': 'false',
        'Grid/RangeMax': '5.0',
        'Grid/RayTracing': 'true',
        'Reg/Strategy': '0',        # 0=Visual, 1=ICP, 2=Visual+ICP
        'Vis/MinInliers': '12',
    }]

    remappings = [
        ('rgb/image', '/camera/camera/image_raw'),
        ('depth/image', '/camera/camera/depth/image_raw'),
        ('rgb/camera_info', '/camera/camera/camera_info'),
        ('odom', '/odom'),
    ]

    rtabmap_slam_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        output='screen',
        parameters=parameters,
        remappings=remappings,
        arguments=['-d']  # Delete previous temporary database on fresh launch
    )

    rtabmap_viz_node = Node(
        package='rtabmap_viz',
        executable='rtabmap_viz',
        output='screen',
        parameters=parameters,
        remappings=remappings,
        additional_env={'QT_X11_NO_MITSHM': '1'}
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation clock'
        ),
        rtabmap_slam_node,
        rtabmap_viz_node
    ])
