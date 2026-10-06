AMR Simulation & SLAM Sandbox

This repository provides a Dockerized simulation and 3D SLAM development environment for an Autonomous Mobile Robot (AMR). It includes Gazebo physics simulation, diff-drive kinematics, depth camera integration, and RTAB-Map SLAM.

## Prerequisites

* **Docker Desktop** installed and running on the host (WSL2 backend recommended on Windows).
* **X11 Server** on the host for GUI forwarding:
* **Linux / native WSL2:** Uses native Wayland/X11 display (`DISPLAY=:0` or `$DISPLAY`).
* **Windows (VcXsrv / Xming):** Ensure access control is disabled (`-ac` flag checked).



---

## 1. Build the Docker Image

From the repository root on your host machine, build the image:

```bash
docker build -t ros2_sim_sandbox:latest .

```

---

## 2. Allow X11 GUI Forwarding (Host Terminal)

Before running the container, grant Docker permission to access your host X server.

### Linux / WSL2:

```bash
xhost +local:root

```

### Windows (VcXsrv):

Launch **XLaunch** with:

* Multiple windows
* Display number: `0`
* Start no client
* **Check** "Disable access control"

---

## 3. Run the Container

Start the container with the workspace bind-mounted to your host for real-time code synchronization:

```bash
docker run -it -d \
  --name ros2_sim_sandbox \
  --net=host \
  --ipc=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$(pwd)":/workspace/ros2_ws \
  ros2_sim_sandbox:latest

```

---

## 4. Build the ROS 2 Workspace

Enter the running container:

```bash
docker exec -it ros2_sim_sandbox bash

```

Inside the container terminal:

```bash
cd /workspace/ros2_ws
colcon build --symlink-install
source /workspace/ros2_ws/install/setup.bash

```

---

## 5. Quickstart: Launch Simulation & SLAM

Run each command in a separate container terminal (`docker exec -it ros2_sim_sandbox bash`):

### Terminal 1: Gazebo Simulation & Robot State Publisher

```bash
source /workspace/ros2_ws/install/setup.bash
export QT_X11_NO_MITSHM=1
ros2 launch amr_description sim.launch.py

```

### Terminal 2: RTAB-Map SLAM

```bash
source /workspace/ros2_ws/install/setup.bash
ros2 launch amr_description rtabmap.launch.py

```

### Terminal 3: Keyboard Teleoperation

```bash
source /workspace/ros2_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

```

Use `i` (forward), `j` / `l` (turn), and `k` (stop) to drive the AMR through the environment while monitoring map building in RViz.

---

## 6. Saving the Map

Once the environment is explored, save the occupancy grid and database:

```bash
# Save 2D Nav2 occupancy grid
mkdir -p /workspace/ros2_ws/maps
ros2 run nav2_map_server map_saver_cli -f /workspace/ros2_ws/maps/cafe_map

# Backup RTAB-Map 3D database
cp ~/.ros/rtabmap.db /workspace/ros2_ws/maps/cafe_rtabmap.db

```
