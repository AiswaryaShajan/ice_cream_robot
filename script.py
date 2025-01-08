from robodk.robolink import *
from robodk import *
import time
from robodk.robomath import *

RDK = Robolink()  # Establish connection between RoboDK and Python Code
robot = RDK.Item('Epson VT6')
open_gripper_program = RDK.Item('open_gripper', ITEM_TYPE_PROGRAM)  # Opening the gripper
close_gripper_program = RDK.Item('close_gripper', ITEM_TYPE_PROGRAM)  # Closing the gripper
attach = RDK.Item('attach', ITEM_TYPE_PROGRAM)  # Attaching to the gripper
detach = RDK.Item('detach', ITEM_TYPE_PROGRAM) #Detaching from the gripper

# Teach points defined for home and picking up first cone from input station
home = RDK.Item('home')
pick_1 = RDK.Item('pick_1')

# Offset points for picking the remaining cones
pick_2 = pick_1.Pose() * transl(0, -121, 0)
pick_3 = pick_1.Pose() * transl(0, 0, -119)
pick_4 = pick_1.Pose() * transl(0, -121, -119)
pick_5 = pick_1.Pose() * transl(0, 0, -238)
pick_6 = pick_1.Pose() * transl(0, -121, -238)

# Offset points for approaching each cone
approach_1 = pick_1.Pose() * transl(300, 0, 0)
approach_2 = pick_1.Pose() * transl(300, -121, 0)
approach_3 = pick_1.Pose() * transl(300, 0, -119)
approach_4 = pick_1.Pose() * transl(300, -121, -119)
approach_5 = pick_1.Pose() * transl(300, 0, -238)
approach_6 = pick_1.Pose() * transl(300, -121, -238)

# Teach points for filling station
approach_fill = RDK.Item('approach_fill')  # Approach point for filling station
enter_fill = RDK.Item('enter_fill')
fill_1_go_up = RDK.Item('fill_1_go_up')
fill_1_go_down = fill_1_go_up.Pose() * transl(-15, 0, 0)
intermediate_fill = RDK.Item('intermediate_fill')
approach_fill_2 = RDK.Item('approach_fill_2')
intermediate_fill_2 = RDK.Item('intermediate_fill_2')
fill_2_go_down = RDK.Item('fill_2_go_down')
test_1 = RDK.Item('test_1')
test_2 = RDK.Item('test_2')
exit_fill = RDK.Item('exit_fill')

#Teach points for dropping station
Drop_1 = RDK.Item('Drop_1')
pre_drop = Drop_1.Pose() * transl(100, 0, 0)

# Set the robot speed (in mm/s for translation and deg/s for rotation)
robot.setSpeed(500)  # Set translation speed to 500 mm/s
robot.setSpeedJoints(150)  # Set joint speed to 150 deg/s

# Picking up the cone_1 from input station
robot.MoveJ(home)
open_gripper_program.RunProgram()
time.sleep(1)
robot.MoveJ(approach_1)
time.sleep(1)
robot.MoveL(pick_1)  # Pick up the first cone
time.sleep(1)
close_gripper_program.RunProgram()
time.sleep(2)
attach.RunProgram()
time.sleep(1)
robot.MoveL(approach_1)
time.sleep(1)
robot.MoveL(approach_fill)
time.sleep(1)

# Lower speed for filling station
robot.setSpeed(100)  # Set slower translation speed
robot.setSpeedJoints(50)  # Set slower joint speed
robot.MoveC(enter_fill, intermediate_fill)
robot.MoveL(fill_1_go_down)
time.sleep(1)
robot.MoveL(fill_1_go_up)
time.sleep(0.5)
robot.MoveL(fill_1_go_down)
time.sleep(1)
robot.MoveC(approach_fill_2, intermediate_fill_2)
robot.MoveL(fill_2_go_down)
fill_2_go_up = fill_2_go_down.Pose() * transl(25,0,0) 
robot.MoveL(fill_2_go_up)
time.sleep(1)
robot.MoveL(fill_2_go_down)
time.sleep(1)
robot.MoveL(test_1)
robot.MoveL(test_2)
robot.MoveL(exit_fill)

# Restore original speed settings
robot.setSpeed(500)  # Restore translation speed
robot.setSpeedJoints(150)  # Restore joint speed
# Dropping station
robot.MoveJ(pre_drop)
robot.MoveL(Drop_1)
detach.RunProgram()
robot.MoveJ(home)
