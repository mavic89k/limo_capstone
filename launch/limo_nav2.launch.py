"""
[원본 코드 출처 및 기반]
- ROS 2 nav2_bringup 패키지의 'bringup_launch.py' (자율주행 풀 스택)

[이 런치 파일의 역할]
사전에 매핑하여 저장해 둔 지도를 바탕으로, 지정한 목적지(Waypoint)까지 자율주행을 수행할 때 씁니다.
1. Map Server를 켜서 저장된 지도(.yaml)를 메모리에 띄웁니다.
2. AMCL을 켜서 라이다 스캔 데이터와 지도를 비교해 현재 로봇의 위치를 추정합니다.
3. Planner/Controller를 켜서 목적지까지의 궤적을 그리고 장애물을 피하며 주행합니다.
4. LIMO 모델에 누락된 base_footprint 좌표계를 보정해줍니다.
"""

import os # 경로 처리를 위한 Python 내장 라이브러리

# 특정 패키지의 설치 폴더(share 디렉터리) 절대 경로를 찾아줌
from ament_index_python.packages import get_package_share_directory

# 최종적으로 실행할 런치 구조를 담아 ROS 2 실행기에 넘겨주는 컨테이너 객체
from launch import LaunchDescription

# DeclareLaunchArgument: 터미널에서 'map:=경로' 처럼 입력받을 수 있는 변수 선언
# IncludeLaunchDescription: 외부 패키지의 런치 파일을 이 파일 안에 끼워 넣음
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription

# 가져올 파일이 XML 등이 아닌 파이썬(.py) 런치 파일임을 명시함
from launch.launch_description_sources import PythonLaunchDescriptionSource

# 선언된 인자(LaunchArgument)의 실제 값을 꺼내어 사용할 때 씀
from launch.substitutions import LaunchConfiguration

# 단일 실행 파일(Node)을 구동하기 위한 클래스
from launch_ros.actions import Node


def generate_launch_description():
    pkg_limo_capstone = get_package_share_directory('limo_capstone')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')

    # 불러올 지도의 기본 경로 지정 
    default_map_path = os.path.join(pkg_limo_capstone, 'maps', 'domi_map.yaml')

    map_arg = DeclareLaunchArgument(
        'map',
        default_value=default_map_path,
        description='Full path to map yaml file to load'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # [1] 정적 TF 브로드캐스터 (좌표계 연결 보정)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint']
    )

    # [2] Nav2 전체 스택 (bringup_launch)
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': LaunchConfiguration('map'),             
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': 'true',
        }.items()
    )

    return LaunchDescription([
        map_arg,
        use_sim_time_arg,
        static_tf,           
        nav2_bringup_launch  
    ])