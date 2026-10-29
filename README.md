# 🚗 LIMO Capstone Project (자율주행 및 자동 탐색 로봇)

본 프로젝트는 ROS 2 환경에서 LIMO 로봇을 활용하여 미지의 실내 환경을 자동으로 탐색(Frontier Exploration)하고 지도를 작성(SLAM)하며, 생성된 지도를 바탕으로 자율주행(Nav2)을 수행하는 캡스톤 디자인 프로젝트입니다.
실제 로봇(Real Robot) 주행 환경과 통합된 Gazebo 가상 시뮬레이션(Simulation) 환경을 모두 제공하여 알고리즘 검증 및 평가가 가능합니다.

## 📂 디렉터리 구조 (Directory Structure)

* `launch/` : 실제 로봇 구동 및 시뮬레이션 환경 실행을 위한 런치 파일

* `config/` : SLAM, Nav2(DWB 및 RPP 플러그인) 파라미터 및 RViz 설정 파일 (`.yaml`, `.xml`, `.rviz`)

* `maps/` : 실제 주행 및 시뮬레이션에서 생성/사용되는 2D 점유 격자 지도 데이터 (`.pgm`, `.yaml`)

* `worlds/` : Gazebo 시뮬레이션 테스트를 위한 가상 3D 환경 맵 파일 (`.sdf`)

* `models/` : 시뮬레이션 내 로봇 및 장애물의 3D 모델, 메시 데이터 (`.dae`, `.urdf`, `.sdf`)

* `scripts/` : 복합 장애물 환경 생성 및 자율주행 성능 평가를 위한 파이썬 스크립트 및 JSON 데이터

* `cpp_source_backup/` : 실차 적용 전 시뮬레이션에서 검증된 C++ 커스텀 소스코드 백업 (예: `explore.cpp`, `smooth_motion.cc`)

## 🛠️ 설치 및 빌드 방법 (Installation & Build)

본 패키지는 `setup.py`를 통해 모든 하위 디렉터리의 자원(맵, 모델, 설정 파일 등)을 ROS 2 `share` 경로로 자동으로 패키징 및 배포합니다.

```
# 1. 워크스페이스의 src 폴더로 이동 후 저장소 복제 (팀 깃허브 주소로 변경)
cd ~/limo_ws/src
git clone https://github.com/mavic89k/limo_capstone.git

# 2. 필수 의존성 패키지 설치
cd ~/limo_ws
rosdep install --from-paths src --ignore-src -r -y

# 3. 패키지 빌드 (데이터 배포 포함)
colcon build --symlink-install --packages-select limo_capstone

# 4. 환경 변수 적용
source install/setup.bash

```

## 🚀 실행 방법 (Usage)

### 1. 실제 로봇 (Real LIMO) 환경

실제 로봇의 라이다(LiDAR) 센서와 모터를 이용한 주행입니다.

**자동 탐색 및 맵핑 (Auto Mapping)**

```
ros2 launch limo_capstone limo_auto_mapping.launch.py

```

**자율 주행 (Navigation2 - DWB Planner)**

```
ros2 launch limo_capstone limo_nav2.launch.py

```

### 2. 가상 시뮬레이션 (Gazebo) 환경

Gazebo 시뮬레이션 환경에서는 DWB 대신 RPP(Regulated Pure Pursuit) 플러그인을 사용하여 동적/정적 장애물 회피 및 주행 성능을 평가합니다.

**가상 환경 및 로봇 실행**

```
# 주의: 아래 파일명은 실제 사용하신 시뮬레이션 런치 파일 이름으로 변경하여 실행하세요.
ros2 launch limo_capstone [시뮬레이션_런치파일이름].launch.py

```

**동적 장애물 및 평가 시나리오 실행**

```
python3 src/limo_capstone/scripts/sim_ctl.py

```

## 📝 주요 커스텀 및 핵심 트러블슈팅

프로젝트 진행 중 발생한 주요 이슈를 분석하고 시스템 구조 레벨에서 직접 튜닝하여 해결한 내역입니다.

### 1. 자율주행 및 탐색 알고리즘 최적화

* **실내 좁은 공간 주행(Navigation) 최적화**
  * **이슈:** 폭이 좁은 복도나 방의 벽 근처에 접근 시, 로봇이 경로 생성을 포기하고 멈춰버리는(Freezing) 현상 발생.
  * **해결:** Nav2 코스트맵 인플레이션 반경(`inflation_radius`)을 기본 0.55m에서 **0.30m로 축소**하고 비용 가중치를 조절하여 좁은 공간에서도 유연하게 회피 기동을 하도록 해결.

* **목표 산출 알고리즘 튜닝 (`explore_lite`)**
  * **이슈:** 자동 탐색 중 로봇이 비효율적인 경로로 이동하거나 미지의 영역(Frontier) 목표점을 제대로 산출하지 못함.
  * **해결:** 원본 `explore.cpp` 코드를 분석하여 목표 좌표 산출 방식을 기존 무게중심(`centroid`)에서 **중간점(`middle`)** 방식으로 변경하여 탐색 효율 극대화. (수정 코드는 `cpp_source_backup/` 보존)

### 2. ROS 2 시스템 및 통신 안정화

* **TF 누락 보정 (Costmap 충돌 에러 해결)**
  * **이슈:** Nav2 실행 시 TF 트리 누락으로 인해 코스트맵 생성 및 구동 불가.
  * **해결:** 로봇의 기본 URDF에 누락되어 있던 `base_footprint` 프레임을 런치 파일 내부에서 동적으로 변환(`Static Transform Publisher`) 및 연결하여 시스템 에러 해결.

* **시간 동기화 오류 및 Odom 지연 최적화**
  * **이슈:** `Failed to compute odom pose` 에러와 함께 위치 추정 실패 및 심각한 지연 현상 발생.
  * **해결:** `use_sim_time: False` 파라미터를 명시적으로 지정하고, TF 통신 허용 오차(Tolerance)를 1.0초로 여유 있게 늘려 메시지 드롭 현상을 완화함.

* **RViz2 QoS 최적화를 통한 지도 미수신 문제 해결**
  * **이슈:** SLAM 노드가 지도를 발행한 후 RViz2가 늦게 실행되면 화면에 지도가 뜨지 않는 통신 단절 현상.
  * **해결:** RViz2 Map 디스플레이의 통신 신뢰성(QoS) `Durability` 정책을 `Volatile`에서 **`Transient Local`**로 변경하여, 늦게 켜진 노드도 과거 지도를 성공적으로 수신하도록 개선.

### 3. 패키지 배포 자동화

* **setup.py 빌드 스크립트 수정**
  * **이슈:** 시뮬레이션 자원(`maps`, `worlds`, `scripts`) 패키징 중 디렉터리가 섞여 `colcon build` 에러 발생.
  * **해결:** `data_files` 배열 내에 `os.path.isfile` 조건문을 활용한 파일 필터링 로직을 도입하여 빌드 및 배포 자동화 환경 구축.