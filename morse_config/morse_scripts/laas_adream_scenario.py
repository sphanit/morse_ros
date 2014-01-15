import subprocess
from morse.builder import *

# basic PR2 robot to the scene
james = BasePR2()
james.add_interface('ros')  #necessary for having correct tf
james.translate(x=8.2, y=5.5, z=0.0)
james.rotate(x=0.0, y=0.0, z=-1.57)

# keyboard control to the robot
keyboard = Keyboard()
keyboard.name = 'keyboard_control'
james.append(keyboard)

# adding odometry sensor to the robot, with ros interface
odometry = Odometry()
james.append(odometry)
#odometry.add_interface('ros', topic="/odom")
odometry.add_stream('ros')

# laser scanner to the robot, with ros interface
sick = Sick()
sick.translate(x=0.275, z=0.252)
james.append(sick)
sick.properties(Visible_arc = False)
sick.properties(laser_range = 30.0)
sick.properties(resolution = 1.0)
sick.properties(scan_window = 180.0)
sick.create_laser_arc()
#sick.add_interface('ros', topic='/base_scan')
sick.add_stream('ros')

# motion controller to the robot, with ros interface
motion = MotionXYW()
james.append(motion)
motion.add_interface('ros', topic='/cmd_vel')

# adding human model
human = Human()
human.translate(x=8.2, y=2.8, z=0.0)
human.rotate(x=0.0, y=0.0, z=1.57)
human.properties(WorldCamera = True)

# posture sensor for human (use this when ros publisher for humanposture is ready)
#humanposture = HumanPosture()
#humanposture.translate(<x>, <y>, <z>)
#humanposture.rotate(<rx>, <ry>, <rz>)
#human.append(humanposture)
#humanposture.add_interface('ros')

# pose sensor for the human
pose = Pose()
human.append(pose)
pose.add_interface('ros')

# set the environment to tum_kitchen
navigation_morse_dir = subprocess.check_output('rospack find navigation_morse', shell=True,
                                        stderr=subprocess.STDOUT).decode("utf-8").strip('\n')
env = Environment(navigation_morse_dir + "/morse_config/blender_files/laas_adream")
env.place_camera([18.0, 4.0, 10.0])
env.aim_camera([1.0, 0.0 , 1.57])
