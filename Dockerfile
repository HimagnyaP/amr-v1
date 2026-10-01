# ~/ros2_ws/Dockerfile
FROM osrf/ros:humble-desktop

RUN apt-get update && apt-get install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-xacro \
    ros-humble-teleop-twist-keyboard \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Auto-source ROS 2 on entry
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
WORKDIR /workspace/ros2_ws