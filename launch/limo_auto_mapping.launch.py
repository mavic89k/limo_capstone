"""
[원본 코드 출처 및 기반]
- SLAM: ROS 2 slam_toolbox 패키지의 'online_async_launch.py'
- Nav2: ROS 2 nav2_bringup 패키지의 'navigation_launch.py' (AMCL 및 Map Server 제외 버전)
- 탐색: ROS 2 explore_lite 패키지

[이 런치 파일의 역할]
새로운 공간에서 지도를 작성(매핑)할 때 사용하는 통합 런치 파일입니다.
1. slam_toolbox를 켜서 라이다 데이터를 바탕으로 실시간 2D 지도를 생성합니다.
2. Nav2 주행 엔진을 켜서 장애물을 피하며 주행할 수 있도록 합니다. (미리 저장된 지도를 쓰는 AMCL 노드는 끕니다)
3. LIMO 모델에 누락된 base_footprint 좌표계를 보정해줍니다.
4. (선택) explore_lite를 켜서 로봇이 맵의 빈 공간을 스스로 찾아가게 만듭니다.
"""

import os # 파일 및 디렉터리 경로를 생성하고 합치기 위한 Python 기본 라이브러리

# 특정 ROS 2 패키지가 설치된 전체 경로를 찾아주는 함수
from ament_index_python.packages import get_package_share_directory

# 런치 파일이 최종적으로 반환해야 하는 객체 (실행할 노드들을 담는 리스트 역할)
from launch import LaunchDescription

# 터미널에서 입력받을 변수(인자)를 선언하는 DeclareLaunchArgument
# 다른 패키지에 있는 런치 파일을 가져와서 실행해 주는 IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription

# 포함(Include)할 외부 런치 파일이 파이썬 형식(.py)임을 지정해 주는 클래스
from launch.launch_description_sources import PythonLaunchDescriptionSource

# 터미널이나 런치 파일 내부에서 선언된 변수(인자)의 값을 읽어올 때 사용하는 클래스
from launch.substitutions import LaunchConfiguration

# 특정 패키지 안의 실행 파일(노드)을 단독으로 구동할 때 사용하는 클래스
from launch_ros.actions import Node


def generate_launch_description():
    # 패키지 경로 불러오기
    pkg_limo_capstone = get_package_share_directory('limo_capstone')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
    pkg_slam_toolbox = get_package_share_directory('slam_toolbox')

    # 설정 파일(.yaml) 경로 선언
    slam_params_file = os.path.join(pkg_limo_capstone, 'config', 'slam_params.yaml')
    nav2_params_file = os.path.join(pkg_limo_capstone, 'config', 'nav2_explore_params.yaml')
    explore_params_file = os.path.join(pkg_limo_capstone, 'config', 'explore.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # [1] SLAM Toolbox 노드 (지도를 실시간으로 그리는 역할)
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam_toolbox, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_params_file': slam_params_file, 
        }.items()
    )

    # [2] Nav2 Navigation 노드 (자율주행의 핵심 엔진)
    nav2_navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav2_params_file, 
            'autostart': 'true'              
        }.items()
    )

    # [3] explore_lite 탐색 노드 (미탐색 구역을 스스로 찾아가는 역할)
    # explore_node = Node(
    #     package='explore_lite',
    #     executable='explore',
    #     name='explore_node',
    #     parameters=[explore_params_file],
    #     output='screen'
    # )

    # [4] 정적 TF 브로드캐스터 (좌표계 연결 보정)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint']
    )

    return LaunchDescription([
        slam_launch,             
        nav2_navigation_launch,  
        # explore_node,          
        static_tf                
    ])