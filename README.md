# 🚗 LIMO ROS 2 Capstone Project

이 저장소는 **AgileX LIMO** 로봇을 활용한 실내 자율 매핑(SLAM) 및 자율주행(Nav2) 캡스톤 프로젝트 패키지입니다. ROS 2 환경에서 LIMO의 센서 데이터를 바탕으로 지도를 생성하고, 장애물을 회피하며 목적지까지 이동하는 전체 파이프라인을 포함하고 있습니다.

## 🛠️ 개발 환경 (Environment)
* **OS:** Ubuntu 22.04 LTS
* **ROS Version:** ROS 2 Humble
* **Hardware:** AgileX LIMO Pro
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
