#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import moveit_commander

def main():
    # Initializeer MoveIt en de ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('get_coordinates_continuous_node', anonymous=True)

    # Koppel de arm-groep
    move_group = moveit_commander.MoveGroupCommander("arm")

    # Vraag eenmalig het actieve referentiekader (de Origin) op
    planning_frame = move_group.get_planning_frame()
    
    print("\n==================================================")
    print("      START CONTINUE COORDINATEN MONITOR         ")
    print("      (Druk op Ctrl+C in deze terminal om te stoppen) ")
    print("==================================================")
    print("Referentiepoint (Origin): {}".format(planning_frame))
    print("==================================================\n")

    # De lus blijft draaien zolang de ROS node actief is (tot Ctrl+C)
    while not rospy.is_shutdown():
        # Vraag de LIVE TCP positie op van dit exacte moment
        current_pose = move_group.get_current_pose().pose

        # Print de coördinaten strak onder elkaar
        print("[LIVE DATA] - Tijd: {}".format(rospy.get_time()))
        print(" X : {:.4f}  (meters naar voren/achteren)".format(current_pose.position.x))
        print(" Y : {:.4f}  (meters naar links/rechts)".format(current_pose.position.y))
        print(" Z : {:.4f}  (meters omhoog vanaf origin)".format(current_pose.position.z))
        print(" Oriëntatie (qx, qy, qz, qw): {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(
            current_pose.orientation.x, 
            current_pose.orientation.y, 
            current_pose.orientation.z, 
            current_pose.orientation.w
        ))
        print("--------------------------------------------------")

        # Wacht exact 5 seconden voor de volgende meting
        rospy.sleep(5)

    print("\nMonitor gestopt.")
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
