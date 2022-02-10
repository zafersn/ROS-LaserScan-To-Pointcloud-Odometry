# 2D Lidar To 3D Point cloud Code File and Ros structure

Sample Video: [Youtube](https://youtu.be/Dk-FqrwyLrM)

![Point Cloud](/resources/picture/youtubepng.PNG)




## To summarize :

**note: this project reconfigured and shared on github 2 years after it was made. There may be some mistakes**

This project was created in order to convert from 2d laser scan data to point cloud 3d data, determine the nearest target point in Point Cloud datas.

we used encoder data as a 3. axis or you can use servo motor angle data.

look into, how I read encoder data and communicate with ROS [Read and publish encoder datas](https://github.com/zafersn/ROS-LaserScan-To-Pointcloud-Odometry/blob/master//resources/arduino-code/pozisyon_control.ino)

if you would like to know that to provide communication between ros and other embedded device ( without heavy ros packages) over the serial, look this essay: https://zafersn.medium.com/how-to-communicate-directly-with-ros-over-serial-7b792c640de7

## The steps to run the project :

> note: this project reconfigured and shared on github 2 years after it was made. There might some mistakes

1. Go `lidar_package/launch/` file and start `tilt_model_rviz.launch` file. `roslaunch lidar_package tilt_model_rviz.launch`

> After that, you may need to follow instruction below respectively,

2. start code.py `rusrun lidar_package code.py` or `python code.py`


### Please do not hesitate any further question or feedback!




