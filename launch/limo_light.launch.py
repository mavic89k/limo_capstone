"""
[원본 코드 출처 및 기반]
- 제조사(AgileX Robotics) limo_ros2 패키지 저장소의 'limo_base', 'limo_bringup'

[이 런치 파일의 역할]
LIMO 로봇 하드웨어의 모터와 센서들을 깨우는 가장 기초적인 실행 파일입니다.
(터미널 명령어 `light`를 치면 이 파일이 실행됩니다.)
1. 로봇 바퀴 모터 통신을 열고 움직임(odom)을 계산합니다.
2. 로봇의 3D 형태와 부품(라이다 등) 위치 정보(URDF)를 불러옵니다.
3. 머리 위에 달린 YDLidar 라이다 센서를 켜서 주변 스캔 데이터를 받아옵니다.
"""

# 최종 반환할 런치 컨테이너 객체
from launch import LaunchDescription

# 외부 패키지의 런치 파일을 불러오는 액션 클래스
from launch.actions import IncludeLaunchDescription

# 불러올 외부 런치 파일이 파이썬 형식임을 알림
from launch.launch_description_sources import PythonLaunchDescriptionSource

# get_package_share_directory와 비슷한 역할이나, 런치 파일 내부에서
# 경로 치환(Substitution) 용도로 좀 더 유연하게 패키지 경로를 찾을 때 쓰는 함수
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # [1] LIMO Base (하드웨어 베이스)
    base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('limo_base'), '/launch/limo_base.launch.py'
        ]),
        launch_arguments={'pub_odom_tf': 'true'}.items() 
    )

    # [2] LIMO Description (로봇 3D 외형 및 센서 위치 정보)
    urdf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('limo_description'), '/launch/load_urdf.launch.py'
        ])
    )

    # [3] YDLidar Driver (라이다 센서 드라이버)
    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('ydlidar_ros2_driver'), '/launch/ydlidar.launch.py'
        ])
    )

    return LaunchDescription([
        base_launch,
        urdf_launch,
        lidar_launch
    ])