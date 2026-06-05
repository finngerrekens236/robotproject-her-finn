#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import moveit_commander
from geometry_msgs.msg import Pose

# HIER IMPORTING JE DE SERVICE VAN DE CAMERA
# (Vervang 'camera_package' en 'GetProductPose' door de echte namen)
from camera_package.srv import GetProductPose, GetProductPoseRequest

def main():
    # Initialiseer MoveIt en de ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_to_detected_product_node', anonymous=True)

    # Koppel de robotarm
    move_group = moveit_commander.MoveGroupCommander("arm")

    # Snelheid voor de veiligheid op 20% zetten
    move_group.set_max_velocity_scaling_factor(0.2)
    move_group.set_max_acceleration_scaling_factor(0.2)

    # --- 1. WACHTEN OP DE CAMERA SERVICE ---
    service_name = '/detect_product'
    rospy.loginfo("Wachten tot de camera service (%s) online is...", service_name)
    rospy.wait_for_service(service_name)
    
    try:
        # Maak een verbinding (client) naar de service
        get_product_pose = rospy.ServiceProxy(service_name, GetProductPose)
        
        # Doe de service call (we sturen een leeg request, of eventueel een product_id indien nodig)
        rospy.loginfo("Product gedetecteerd! Positie opvragen bij camera...")
        response = get_product_pose(GetProductPoseRequest())
        
    except rospy.ServiceException as e:
        rospy.logerr("Service call mislukt: %s", e)
        moveit_commander.roscpp_shutdown()
        return

    # --- 2. DE ONTVANGEN POSITIE IN DE TARGET_POSE ZETTEN ---
    target_pose = Pose()
    
    # We nemen aan dat de camera service een 'pose' of losse x,y,z teruggeeft.
    # Als de camera een kant-en-klaar geometry_msgs/Pose object teruggeeft (bijv. response.pose):
    target_pose = response.pose

    # (Als de camera losse variabelen teruggeeft, zou het er zo uitzien:)
    # target_pose.position.x = response.x
    # target_pose.position.y = response.y
    # target_pose.position.z = response.z
    # target_pose.orientation = response.orientation

    print("\n==================================================")
    print(" -> Plannen naar de ONTVANGEN camera positie...")
    print(" X: {}, Y: {}, Z: {}".format(target_pose.position.x, target_pose.position.y, target_pose.position.z))
    print("==================================================")

    # Stuur het doel naar MoveIt
    move_group.set_pose_target(target_pose)

    # Bereken en voer de beweging uit
    success = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    if success:
        print("\n=== Doel succesvol bereikt! ===")
    else:
        print("\n!!! Planning mislukt. Controleer de robotstatus. !!!")

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass