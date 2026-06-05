#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import moveit_commander
from geometry_msgs.msg import Pose
import subprocess
import math
from tf.transformations import quaternion_from_euler, euler_from_quaternion
def main():
    # Initializeer MoveIt en de ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('pick_and_lift_node', anonymous=True)

    # Koppel de robotarm
    move_group = moveit_commander.MoveGroupCommander("arm")

    # Snelheid voor de veiligheid op 20% zetten
    move_group.set_max_velocity_scaling_factor(0.2)
    move_group.set_max_acceleration_scaling_factor(0.2)

    # ==========================================
    # STAP 1: GRIPPER OPENEN VÓÓR VERPLAATSING
    # ==========================================
    print("\n -> Gripper openen...")
    subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

   # ==========================================
    # STAP 2: NAAR HET PRODUCT BEWEGEN
    # ==========================================
    target_pose = Pose()
    
    # De XYZ coördinaten (in meters)
    target_pose.position.x = -0.122348003112
    target_pose.position.y = -0.276515803629
    target_pose.position.z = 0.165
    
    # --- DE FIX VOOR DE NIEUWE ORIËNTATIE ---
    

    # 1. We pakken de quaternion die uit je camera komt
    camera_q = [0.0, 0.0, -0.22821738467,   0.973610201947]
    
    # 2. We berekenen hoeveel graden rotatie (Yaw) dit is om de Z-as
    # (Bij deze specifieke w,z-waarden is dat ongeveer 39.8 graden)
    _, _, camera_yaw = euler_from_quaternion(camera_q)
    
    # 3. We dwingen de robot om recht naar beneden te kijken (Roll = 180 graden)
    # en we voegen de rotatie (Yaw) van de camera toe.
    roll = math.radians(180) 
    pitch = math.radians(0)
    yaw = camera_yaw 
    
    # 4. ROS berekent nu de gecorrigeerde quaternion die MoveIt wél snapt
    q = quaternion_from_euler(roll, pitch, yaw)
    
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]

    print("\n==================================================")
    print(" -> Plannen naar de nieuwe doelpositie...")
    print(" X: {}, Y: {}, Z: {}".format(target_pose.position.x, target_pose.position.y, target_pose.position.z))
    print(" Gecorrigeerde Quaternion -> X: {:.3f}, Y: {:.3f}, Z: {:.3f}, W: {:.3f}".format(q[0], q[1], q[2], q[3]))
    print("==================================================")

    print("\n==================================================")
    print(" -> Plannen naar de nieuwe doelpositie...")
    print(" X: {}, Y: {}, Z: {}".format(target_pose.position.x, target_pose.position.y, target_pose.position.z))
    print(" Oriëntatie (Quaternion) -> Z: {}, W: {}".format(target_pose.orientation.z, target_pose.orientation.w))
    print("==================================================")

    move_group.set_pose_target(target_pose)
    success = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    if not success:
        print("\n!!! Planning naar product mislukt. Script afgebroken. !!!")
        moveit_commander.roscpp_shutdown()
        return

    # ==========================================
    # STAP 3: PRODUCT GRIJPEN (GRIPPER DICHT)
    # ==========================================
    print("\n -> Product grijpen (gripper sluiten)...")
    subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])
    
    rospy.sleep(0.5) # Wacht even tot de vacuümvanger grip heeft

    # ==========================================
    # STAP 4: 5 CENTIMETER OMHOOG (Z + 0.05m)
    # ==========================================
    print("\n -> 5 centimeter omhoog bewegen voor de veiligheid...")
    
    # Haal de huidige positie op als startpunt voor de lift
    lift_pose = move_group.get_current_pose().pose
    
    # Let op: de robot gebruikt meters. We tellen 0.05 meter (5 cm) op bij de huidige Z-hoogte
    lift_pose.position.z += 0.05

    move_group.set_pose_target(lift_pose)
    success_lift = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    if success_lift:
        print("\n=== Product succesvol gegrepen en opgetild! ===")
    else:
        print("\n!!! Optillen mislukt. Controleer robotlimieten. !!!")

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass