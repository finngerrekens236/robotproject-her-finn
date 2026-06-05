#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import actionlib
import moveit_commander
from geometry_msgs.msg import Pose
from std_msgs.msg import String  # Voor het /robot/status topic
import subprocess
import math
from tf.transformations import quaternion_from_euler, euler_from_quaternion

# =========================================================================
# IMPORT ACTION BERICHTEN
# Vervang 'jouw_package' door de naam van de package waar de .action file in zit
# =========================================================================
from my_demo.msg import PickPlaceAction, PickPlaceFeedback, PickPlaceResult

class RobotPickPlaceActionServer(object):
    # Feedback en Result objecten aanmaken
    _feedback = PickPlaceFeedback()
    _result = PickPlaceResult()

    def __init__(self, name):
        self._action_name = name
        
        # 1. Setup Status Publisher (/robot/status topic)
        self.status_pub = rospy.Publisher('/robot/status', String, queue_size=10)
        self.publish_status("IDLE")

        # 2. Initializeer MoveIt Commander
        self.move_group = moveit_commander.MoveGroupCommander("arm")
        self.move_group.set_max_velocity_scaling_factor(0.2)
        self.move_group.set_max_acceleration_scaling_factor(0.2)

        # 3. Start de Action Server
        self._as = actionlib.SimpleActionServer(
            self._action_name, 
            PickPlaceAction, 
            execute_cb=self.execute_cb, 
            auto_start=False
        )
        self._as.start()
        rospy.loginfo("Robot Action Server is actief op %s. Wachten op goal...", self._action_name)

    def publish_status(self, status_msg):
        """Hulpmethode om snel statusupdates op het topic te publiceren."""
        msg = String()
        msg.data = status_msg
        self.status_pub.publish(msg)

    def execute_cb(self, goal):
        """Deze functie start zodra het hoofdprogramma een 'Action Goal' stuurt."""
        rospy.loginfo("Nieuw Pick & Place doel ontvangen!")
        self.publish_status("BUSY_PICKING")

        # Voorbeeld feedback sturen (voortgang % of status)
        # Pas dit aan op basis van wat er in je PickPlaceFeedback.action staat
        # self._feedback.progress = 10
        # self._as.publish_feedback(self._feedback)

        # ==========================================
        # STAP 1: GRIPPER OPENEN VÓÓR VERPLAATSING
        # ==========================================
        print("\n -> Gripper openen...")
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

        # ==========================================
        # STAP 2: NAAR HET PRODUCT BEWEGEN
        # ==========================================
        target_pose = Pose()
        
        # We halen de coördinaten en oriëntatie nu UIT het ontvangen goal!
        # (Ik neem hier aan dat het hoofdprogramma een complete geometry_msgs/Pose meestuurt in het goal)
        target_pose.position.x = goal.target_pose.position.x
        target_pose.position.y = goal.target_pose.position.y
        target_pose.position.z = 0.165  # Vaste veilige pakhoogte
        
        # Pak de quaternion uit het goal van de camera/hoofdprogramma
        camera_q = [
            goal.target_pose.orientation.x,
            goal.target_pose.orientation.y,
            goal.target_pose.orientation.z,
            goal.target_pose.orientation.w
        ]
        
        # De vertrouwde oriëntatie-fix toepassen
        _, _, camera_yaw = euler_from_quaternion(camera_q)
        roll = math.radians(180) 
        pitch = math.radians(0)
        yaw = camera_yaw 
        
        q = quaternion_from_euler(roll, pitch, yaw)
        target_pose.orientation.x = q[0]
        target_pose.orientation.y = q[1]
        target_pose.orientation.z = q[2]
        target_pose.orientation.w = q[3]

        print("\n==================================================")
        print(" -> Plannen naar de ontvangen Action Goal positie...")
        print(" X: {}, Y: {}, Z: {}".format(target_pose.position.x, target_pose.position.y, target_pose.position.z))
        print("==================================================")

        self.move_group.set_pose_target(target_pose)
        success = self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        if not success:
            print("\n!!! Planning naar product mislukt. !!!")
            self.publish_status("ERROR_PLANNING_FAILED")
            self._result.success = False  # Pas dit aan op basis van je .action result definities
            self._as.set_aborted(self._result)
            return

        # ==========================================
        # STAP 3: PRODUCT GRIJPEN (GRIPPER DICHT)
        # ==========================================
        print("\n -> Product grijpen (gripper sluiten)...")
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])
        rospy.sleep(0.5)

        # ==========================================
        # STAP 4: 5 CENTIMETER OMHOOG (Z + 0.05m)
        # ==========================================
        print("\n -> 5 centimeter omhoog bewegen voor de veiligheid...")
        lift_pose = self.move_group.get_current_pose().pose
        lift_pose.position.z += 0.05

        self.move_group.set_pose_target(lift_pose)
        success_lift = self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        # ==========================================
        # ACTION AFRONDEN (RESULTAAT TERUGSTUREN)
        # ==========================================
        if success_lift:
            print("\n=== Product succesvol gegrepen en opgetild! ===")
            self.publish_status("IDLE")
            self._result.success = True  # Of wat er ook in je action result staat
            self._as.set_succeeded(self._result)
        else:
            print("\n!!! Optillen mislukt. !!!")
            self.publish_status("ERROR_LIFT_FAILED")
            self._result.success = False
            self._as.set_aborted(self._result)

def main():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('robot_action_server_node')

    # Start de klasse en noem de action server '/robot/pick_place'
    server = RobotPickPlaceActionServer('/robot/pick_place')
    
    rospy.spin()
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass