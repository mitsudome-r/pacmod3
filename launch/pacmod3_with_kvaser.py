# Copyright (c) 2019 AutonomouStuff, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import launch.actions
import launch.substitutions
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    bridge_params_file = DeclareLaunchArgument(
        'bridge_params',
        default_value=[launch.substitutions.ThisLaunchFileDir(),
                       '/bridge_params.yaml'])
    pacmod_params_file = DeclareLaunchArgument(
        'pacmod_params',
        default_value=[launch.substitutions.ThisLaunchFileDir(),
                       '/driver_params.yaml'])

    container = ComposableNodeContainer(
        name='pacmod3_with_kvaser',
        namespace='/pacmod',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='kvaser_interface',
                plugin='kvaser_interface::KvaserReaderNode',
                name='kvaser_reader',
                namespace='/pacmod',
                parameters=[{
                    'hardware_id': 65359,
                    'circuit_id': 0,
                    'bit_rate': 500000,
                    'enable_echo': True,
                }]),
            ComposableNode(
                package='kvaser_interface',
                plugin='kvaser_interface::KvaserWriterNode',
                name='kvaser_writer',
                namespace='/pacmod',
                parameters=[{
                    'hardware_id': 65359,
                    'circuit_id': 0,
                    'bit_rate': 500000,
                    'enable_echo': True,
                }]),
            ComposableNode(
                package='pacmod3',
                plugin='pacmod3::PACMod3Node',
                name='pacmod3_driver',
                namespace='/pacmod',
                parameters=[{
                    'vehicle_type': "LEXUS_RX_450H",
                    'frame_id': "pacmod",
                }]
            )
        ],
        output='screen',
    )

    log_info = LogInfo(
        msg=["bridge_params = ", LaunchConfiguration('bridge_params')])
    log_info2 = LogInfo(
        msg=["pacmod_params = ", LaunchConfiguration('pacmod_params')])

    return launch.LaunchDescription([
        bridge_params_file,
        pacmod_params_file,
        log_info,
        log_info2,
        container])
