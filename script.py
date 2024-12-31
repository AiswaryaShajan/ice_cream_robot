from robodk.robolink import *
from robodk import *
import time
from robodk.robomath import *

RDK = Robolink()  # Establish connection between RoboDK and Python Code
robot= RDK.Item('Epson VT6')
open_gripper_program = RDK.Item('open_gripper', ITEM_TYPE_PROGRAM)
close_gripper_program = RDK.Item('close_gripper', ITEM_TYPE_PROGRAM)

# Taught points for first two cones
pick_1 = RDK.Item('pick_1')
pick_2 = RDK.Item('pick_2')
# Offset points for the remaining
pick_3 = pick_1.Pose()*transl(0,0,-120)
pick_4 = pick_2.Pose()*transl(0,0,-120)
pick_5 = pick_1.Pose()*transl(0,0,-235)
pick_6 = pick_2.Pose()*transl(0,0,-235)

#Offset points for approaching each cone
approach_1 = pick_1.Pose()*transl(100,0,0)
approach_2 = pick_2.Pose()*transl(100,0,0)
approach_3 = pick_1.Pose()*transl(100,0,-120)
approach_4 = pick_2.Pose()*transl(100,0,-120)
approach_5 = pick_1.Pose()*transl(100,0,-235)
approach_6 = pick_2.Pose()*transl(100,0,-235)


# Robot path
robot.MoveL(approach_1)  
time.sleep(1)
robot.MoveJ(pick_1)  # Pick up the first cone
time.sleep(1)

robot.MoveL(approach_2)  
time.sleep(1)
robot.MoveL(pick_2)  # Pick up the second cone
time.sleep(1)

robot.MoveL(approach_3)  
time.sleep(1)
robot.MoveL(pick_3)  # Pick up the third cone
time.sleep(1)

robot.MoveL(approach_4)  
time.sleep(1)
robot.MoveL(pick_4)  # Pick up the fourth cone
time.sleep(1)

robot.MoveL(approach_5)  
time.sleep(1)
robot.MoveL(pick_5)  # Pick up the fifth cone
time.sleep(1)

robot.MoveL(approach_6)  
time.sleep(1)
robot.MoveL(pick_6)  # Pick up the sixth cone
time.sleep(1)
