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

# Teach points for dropping station
approach_drop_1 = RDK.Item('approach_drop')
drop_1 = RDK.Item('drop_1')
approach_drop_2 = drop_1.Pose()*transl(120,77,140)
drop_2 = drop_1.Pose()*transl(0,77,140)
approach_drop_3 = drop_1.Pose()*transl(120,227,140)
drop_3 = drop_1.Pose()*transl(0,227,140)
approach_drop_4 = drop_1.Pose()*transl(120,300,15)
drop_4 = drop_1.Pose()*transl(0,300,15)
drop_5 = RDK.Item('drop_5')
approach_drop_5 = drop_5.Pose()*transl(120,0,0)
approach_drop_6 = drop_5.Pose()*transl(120,-150,-5)
drop_6 = drop_5.Pose()*transl(0,-150,-5)

cone_pick_positions = [pick_1, pick_2, pick_3, pick_4, pick_5, pick_6]
approach_pick_positions = [approach_1, approach_2, approach_3, approach_4, approach_5, approach_6]
drop_positions = [drop_1, drop_2, drop_3, drop_4, drop_6, drop_5]
approach_drop_positions = [approach_drop_1, approach_drop_2, approach_drop_3, approach_drop_4, approach_drop_6, approach_drop_5]

# Loop through each cone position
for i in range(6):
    # Move to home position
    robot.MoveJ(home)
    open_gripper_program.RunProgram()
    time.sleep(1)
    
    # Move to the approach position and then pick up the cone
    robot.MoveJ(approach_pick_positions[i])
    time.sleep(1)
    robot.MoveJ(cone_pick_positions[i])
    time.sleep(1)
    close_gripper_program.RunProgram()
    time.sleep(2)
    attach.RunProgram()
    time.sleep(1)
    
    # Move to the filling station
    robot.MoveJ(approach_pick_positions[i])
    time.sleep(1)
    robot.MoveJ(approach_fill)
    time.sleep(1)
    
    # Lower speed for filling station
    robot.setSpeed(100)  # Set slower translation speed
    robot.setSpeedJoints(50)  # Set slower joint speed
    
    # Perform filling operations
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
    
    # Drop the cone at the dropping station
    robot.MoveJ(approach_drop_positions[i])
    robot.MoveJ(drop_positions[i])
    detach.RunProgram()
    time.sleep(1)
    robot.MoveJ(home)