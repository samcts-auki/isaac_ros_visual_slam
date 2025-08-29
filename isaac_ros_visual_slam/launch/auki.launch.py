# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2021-2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import launch
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    """Launch file which brings up visual slam node configured for RealSense."""
    camera_torso_vslam_static_transform_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0.000',' 0.000', '0.000'
                   '1.000', '0.000', '-0.787', '0.000', 'd435_link', 'd435_link_vslam']
    )

    visual_slam_node = ComposableNode(
        name='visual_slam_node',
        package='isaac_ros_visual_slam',
        plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
        parameters=[{
                    'denoise_input_images': False,
                    'rectified_images': True,
                    'enable_debug_mode': False,
                    'debug_dump_path': '/tmp/cuvslam',
                    'enable_slam_visualization': False,
                    'enable_landmarks_view': False,
                    'enable_observations_view': False,
                    'map_frame': 'map',
                    'odom_frame': 'odom_vslam',
                    'base_frame': 'd435_link_vslam',
                    'odom_reference_frame': 'd435_link',
                    'input_imu_frame': 'd435_gyro_optical_frame',
                    'enable_imu_fusion': True,
                    'gyro_noise_density': 0.000244,
                    'gyro_random_walk': 0.000019393,
                    'accel_noise_density': 0.001862,
                    'accel_random_walk': 0.003,
                    'calibration_frequency': 200.0,
                    'img_jitter_threshold_ms': 20.00,
                    'publish_map_to_odom_tf': False,
                    'publish_odom_to_base_tf': True,
                    'invert_odom_to_base_tf': False,
                    'enable_localization_n_mapping': False
                    }],
        remappings=[('stereo_camera/left/image', '/d435/infra1/image_rect_raw'),
                    ('stereo_camera/left/camera_info', '/d435/infra1/camera_info'),
                    ('stereo_camera/right/image', '/d435/infra2/image_rect_raw'),
                    ('stereo_camera/right/camera_info', '/d435/infra2/camera_info'),
                    ('visual_slam/imu', '/d435/imu')]
    )

    visual_slam_launch_container = ComposableNodeContainer(
        name='visual_slam_launch_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            visual_slam_node
        ],
        output='screen'
    )

    return launch.LaunchDescription([
        camera_torso_vslam_static_transform_publisher,
        visual_slam_launch_container, 
        ])
