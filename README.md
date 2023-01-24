# Franka-Emika-Panda-Manipulation-via-Learning-through-demonstration

## About
This repository is for the research internship done at TU Munich, under MSc Esteve Valls and Prof Dongheui Lee. 

The main goal of this project is to control a Franka Panda Arm, by feeding in trajectories performed by the right palm of user. 

The project is divided into 3 subparts -
1. 3D Pose Estimation and Recording Trajectories of right palm of user through MediaPipe
2. After recording same motion multiple times, we get a learned trajectory with the help of DMPs
3. This learned trajectory is then implemented on a Franka Panda Simulation in Gazebo

Link to [Paper](https://docs.google.com/document/d/15dwVdk-WKLVMnLVukNsmk3NElljAcn5vlwIM2_LcbXc/edit?usp=sharing).
Link to [Final Presentation](https://1drv.ms/p/s!AgS-uMOuiZu9hQuuwWgZkoKYTLNy).

## Instructions
Clone and installed the original franka_ros repo (by franka emika) from gitlab.

Replace the following files in the franka emika repo, with the files with the same name from this current repo.
1. src/franka_ros/franka_example_controllers/src/cartesian_impedance_example_controller.cpp
2. src/franka_ros/franka_example_controllers/include/cartesian_impedance_example_controller.h 
3. src/franka_ros/franka_gazebo/world/stone.sdf

### Step 1 - 3D Pose Estimation and Recording Trajectories
Follow the instructions (marked by #-->) given in webcam_pose_estimation.py to adjust it depending on whether you want to use your default webcam, or a pre-recorded video for recording a trajectory.
Multiple trajectories (4-5) need to be recorded to get a good learned Trajectory in the next step.

### Step 2 - Obtaining Learned Trajectory with help of DMPs
Follow the instructions (marked by #-->) given in demo_regression.py to get the learned trajectory from the previously recorded trajectories.

### Step 3 - Implementing learned Trajectory on Gazebo Simulator of Franka Panda Arm
Update the trajectory file name in src/franka_ros/franka_example_controllers/src/cartesian_impedance_example_controller.cpp (line 195), depending on whichever trajectory you are using (default is trajectory.txt - generated in demo_regression_IP.py (line 176))


To run - 
```
cd catkin_ws

catkin_make -DCMAKE_BUILD_TYPE=Release -DFranka_DIR:PATH=~/libfranka/build

catkin devel/setup.sh

roslaunch franka_gazebo panda.launch x:=-0.5     controller:=cartesian_impedance_example_controller     rviz:=true 
# (this is the launch command for launching gazebo simulator)
```
