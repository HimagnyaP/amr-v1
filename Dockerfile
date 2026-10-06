# ~/ros2_ws/Dockerfile
FROM osrf/ros:humble-desktop
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-xacro \
    ros-humble-teleop-twist-keyboard \
    ros-humble-rtabmap-ros \
    ros-humble-image-transport-plugins \
    python3-colcon-common-extensions \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Auto-source ROS 2 on entry
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
WORKDIR /workspace/ros2_ws