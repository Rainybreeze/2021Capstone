import os


class Roscore:
    def __init__(self):
        os.fork()
        os.system('source ~/catkin_ws/devel/setup.bash')
        os.system('roscore')


class Roslidar:
    def __init__(self):
        os.system('roslaunch ydlidar all_nodes.launch')
