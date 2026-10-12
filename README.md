# 🚗 LIMO ROS 2 Capstone Project

이 저장소는 **AgileX LIMO** 로봇을 활용한 실내 자율 매핑(SLAM) 및 자율주행(Nav2) 캡스톤 프로젝트 패키지입니다. ROS 2 환경에서 LIMO의 센서 데이터를 바탕으로 지도를 생성하고, 장애물을 회피하며 목적지까지 이동하는 전체 파이프라인을 포함하고 있습니다.

## 🛠️ 개발 환경 (Environment)
* **OS:** Ubuntu 22.04 LTS
* **ROS Version:** ROS 2 Humble
* **Hardware:** AgileX LIMO (YDLidar Tmini Plus 탑재)

## 📁 주요 디렉터리 구조 (Structure)
```text
limo_capstone/
├── launch/
│   ├── limo_light.launch.py          # LIMO 하드웨어 및 센서 통합 구동 스위치
│   ├── limo_auto_mapping.launch.py   # 실시간 2D 매핑(SLAM) 및 주행 엔진 실행
│   └── limo_nav2.launch.py           # 저장된 지도를 기반으로 한 Nav2 자율주행 실행
├── config/
│   ├── slam_params.yaml              # slam_toolbox 설정 (해상도, 갱신 주기 등)
│   ├── nav2_explore_params.yaml      # Nav2 주행 알고리즘 설정 (속도, DWB, 코스트맵 마진 등)
│   └── explore.yaml                  # (선택) explore_lite 자율 프론티어 탐색 설정
└── maps/
    ├── domi_map.yaml / .png          # 기숙사 테스트용 지도 파일
    └── demo_map.yaml / .png          # 시연용 지도 파일 (예정)
```

## ⚙️ 빌드 방법 (Build Instructions)
로컬 PC나 로봇에 패키지를 클론한 후 아래 명령어로 빌드합니다.
```bash
cd ~/capstone_ws
colcon build --symlink-install --packages-select limo_capstone
source install/setup.bash
```

---

## 🚀 실행 가이드 (How to Run)

본 프로젝트는 크게 **[1] 매핑(지도 저장)**과 **[2] 자율주행(순찰)** 두 단계로 나뉘어 실행됩니다. 모든 작업 전, 터미널 1에서 반드시 하드웨어를 먼저 구동해야 합니다.

### Step 0. 하드웨어 구동 (필수)
모터와 라이다 센서를 켭니다.
```bash
# [터미널 1]
light
```

### Step 1. 매핑 모드 (SLAM)
새로운 공간의 지도를 그릴 때 사용합니다.
```bash
# [터미널 2]
ros2 launch limo_capstone limo_auto_mapping.launch.py
```
> **Tip:** RViz2를 켜고 조종기나 키보드로 로봇을 천천히 이동시키며 맵을 스캔합니다.

### Step 2. 지도 저장
매핑이 완료되면 매핑 런치 파일을 끄기 전에 새 터미널을 열어 지도를 저장합니다.
```bash
# [터미널 3]
ros2 run nav2_map_server map_saver_cli -f ~/capstone_ws/src/limo_capstone/maps/demo_map
```

### Step 3. Nav2 자율주행 모드
저장된 지도를 불러와 목적지 자율주행을 시작합니다.
```bash
# [터미널 2] (기존 매핑 노드 종료 후 실행)
ros2 launch limo_capstone limo_nav2.launch.py map:=/home/pcu/capstone_ws/src/limo_capstone/maps/demo_map.yaml
```

### Step 4. RViz2 제어 (노트북 등 원격 PC)
```bash
# [노트북 터미널]
rviz2 -d /opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz
```
1. `2D Pose Estimate` 툴을 이용해 지도상에 로봇의 초기 위치를 지정합니다.
2. `Nav2 Goal` 툴을 이용해 이동할 목적지를 클릭하면 자율주행을 시작합니다.

---
