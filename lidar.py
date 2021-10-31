import os, time, sys

class roscore:
    def __init__(self):
        os.system('source ~/catkin_ws/devel/setup.bash')
        os.system('roscore')

class roslidar:
    def __init__(self):
        os.system('roslaunch ydlidar all_nodes.launch')
