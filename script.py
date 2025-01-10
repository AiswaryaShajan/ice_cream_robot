from robodk.robolink import *
from robodk import *
import time
from robodk.robomath import *

RDK = Robolink()  # Establish connection between RoboDK and Python Code
robot = RDK.Item('Epson VT6')
open_gripper_program = RDK.Item('open_gripper', ITEM_TYPE_PROGRAM)  # Opening the gripper
close_gripper_program = RDK.Item('close_gripper', ITEM_TYPE_PROGRAM)  # Closing the gripper
attach = RDK.Item('attach', ITEM_TYPE_PROGRAM)  # Attaching to the gripper
detach = RDK.Item('detach', ITEM_TYPE_PROGRAM)  # Detaching from the gripper
home = RDK.Item('home')

# INPUT STATION - PICKING
pick_1 = RDK.Item('pick_1')
pick_2 = RDK.Item('pick_2')
pick_3 = pick_1.Pose() * transl(0, 0, -120)
pick_4 = pick_2.Pose() * transl(0, 0, -120)
pick_5 = pick_1.Pose() * transl(0, 0, -240)
pick_6 = pick_2.Pose() * transl(0, 0, -240)
approach_pick = RDK.Item('approach_pick')

# FILL STATION (points in order of path)
approach_fill = RDK.Item('approach_fill')
enter_fill = RDK.Item('enter_fill')
fill_test_4 = RDK.Item('fill_test_4')
fill_1_go_down = RDK.Item('fill_1_go_down')
fill_1_go_up = fill_1_go_down.Pose() * transl(15, 0, 0)
fill_test_1 = RDK.Item('fill_test_1')
approach_fill_2 = RDK.Item('approach_fill_2')
fill_test_2 = RDK.Item('fill_test_2')
fill_2_go_down = RDK.Item('fill_2_go_down')
fill_2_go_up = fill_2_go_down.Pose() * transl(15, 0, 0)
exit_fill = RDK.Item('exit_fill')
fill_test = RDK.Item('fill_test')
fill_test_3 = RDK.Item('fill_test_3')

# OUTPUT STATION - DROPPING
approach_drop = RDK.Item('approach_drop')
drop_1 = RDK.Item('drop_1')
drop_2 = RDK.Item('drop_2')
drop_3 = RDK.Item('drop_3')
drop_4 = RDK.Item('drop_4')
drop_5 = RDK.Item('drop_5')
drop_6 = RDK.Item('drop_6')
approach_drop_1 = drop_1.Pose() * transl(100, 0, 0)
approach_drop_2 = drop_2.Pose() * transl(100, 0, 0)
approach_drop_3 = drop_3.Pose() * transl(100, 0, 0)
approach_drop_4 = drop_4.Pose() * transl(100, 0, 0)
approach_drop_5 = drop_5.Pose() * transl(100, 0, 0)
approach_drop_6 = drop_6.Pose() * transl(100, 0, 0)

# Lists for convenience
pick_positions = [pick_1, pick_2, pick_3, pick_4, pick_5, pick_6]
approach_drop_positions = [approach_drop_1, approach_drop_2, approach_drop_3, approach_drop_4, approach_drop_5, approach_drop_6]
drop_positions = [drop_1, drop_2, drop_3, drop_4, drop_5, drop_6]

# Loop through each cone position
for i in range(6):
    # Move to home position and open gripper
    robot.MoveJ(home)
    open_gripper_program.RunProgram()
    time.sleep(1)
    
    # Move to the approach position and then pick up the cone
    robot.MoveJ(approach_pick)
    robot.MoveL(pick_positions[i])
    time.sleep(1)
    close_gripper_program.RunProgram()
    time.sleep(2)
    attach.RunProgram()
    time.sleep(1)
    robot.MoveL(approach_pick)
    
    # Move to the filling station
    robot.MoveJ(approach_fill)
    robot.MoveL(enter_fill)

    # Lower speed for filling station
    robot.setSpeed(50)  # Set slower translation speed
    robot.setSpeedJoints(25)  # Set slower joint speed

    # Perform filling operations
    robot.MoveC(fill_test_4, fill_1_go_down)
    robot.MoveL(fill_1_go_up)
    robot.MoveL(fill_1_go_down)
    robot.MoveC(fill_test_1, approach_fill_2)
    robot.MoveC(fill_test_2, fill_2_go_down)
    robot.MoveL(fill_2_go_up)
    robot.MoveL(fill_2_go_down)
    robot.MoveL(fill_test)
    robot.MoveC(fill_test_3, exit_fill)
    
    # Restore original speed settings
    robot.setSpeed(500)  # Restore translation speed
    robot.setSpeedJoints(150)  # Restore joint speed

    # Move to the dropping station
    robot.MoveL(approach_drop)
    robot.MoveL(approach_drop_positions[i])
    robot.MoveL(drop_positions[i])
    detach.RunProgram()
    time.sleep(1)
    open_gripper_program.RunProgram()  # Open gripper after dropping
    time.sleep(2)
    robot.MoveL(approach_drop_positions[i])  # Go back to approach position

# Finish by moving to home position
time.sleep(1)
robot.MoveJ(home)