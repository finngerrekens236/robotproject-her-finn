#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
import moveit_commander
import subprocess

from geometry_msgs.msg import Pose

from hoofdprogramma.msg import (
    PickAndPlaceAction,
    PickAndPlaceFeedback,
    PickAndPlaceResult
)


class RobotController(object):

    def __init__(self):

        # --------------------------------------------------
        # MOVEIT INITIALISATIE
        # --------------------------------------------------

        moveit_commander.roscpp_initialize([])

        self.group = moveit_commander.MoveGroupCommander("arm")

        rospy.loginfo("RobotController gestart")

        # Planning instellingen
        self.group.set_num_planning_attempts(20)
        self.group.set_planning_time(10)
        self.group.allow_replanning(True)

        # Toleranties
        self.group.set_goal_position_tolerance(0.01)
        self.group.set_goal_orientation_tolerance(0.01)

        # --------------------------------------------------
        # ACTION SERVER
        # Ontvangt opdrachten van hoofdprogramma
        # --------------------------------------------------

        self.server = actionlib.SimpleActionServer(
            '/pick_and_place',
            PickAndPlaceAction,
            execute_cb=self.execute_callback,
            auto_start=False
        )

        self.server.start()

        rospy.loginfo("PickAndPlace Action Server gestart")

    # ==================================================
    # ACTION CALLBACK
    # ==================================================

    def execute_callback(self, goal):

        feedback = PickAndPlaceFeedback()
        result = PickAndPlaceResult()

        rospy.loginfo("Nieuwe robot goal ontvangen")

        # Goal data ophalen
        target_pose = goal.target_pose.pose
        kwast_type = goal.kwast_type

        # --------------------------------------------------
        # HOMEPOSITIE
        # --------------------------------------------------

        feedback.status = "Ga naar homepositie"
        self.server.publish_feedback(feedback)

        if not self.move_to_named_target("home"):

            rospy.logerr("Homepositie mislukt")

            result.success = False
            self.server.set_aborted(result)

            return

        # --------------------------------------------------
        # PICK OPERATIE
        # --------------------------------------------------

        feedback.status = "Pick operatie gestart"
        self.server.publish_feedback(feedback)

        if not self.pick(target_pose):

            rospy.logerr("Pick operatie mislukt")

            result.success = False
            self.server.set_aborted(result)

            return

        # --------------------------------------------------
        # DOELBAK BEPALEN
        # --------------------------------------------------

        mapping = {
            "norm": "BakRB",
            "dik": "BakRO",
            "rub": "BakLB",
            "pen": "BakLO"
        }

        target_bin = mapping.get(kwast_type.lower(), "home")

        rospy.loginfo("Doelbak: %s", target_bin)

        # --------------------------------------------------
        # NAAR DOELBAK
        # --------------------------------------------------

        feedback.status = "Beweeg naar doelbak"
        self.server.publish_feedback(feedback)

        if not self.move_to_named_target(target_bin):

            rospy.logerr("Beweging naar doelbak mislukt")

            result.success = False
            self.server.set_aborted(result)

            return

        # --------------------------------------------------
        # LOSLATEN
        # --------------------------------------------------

        feedback.status = "Object loslaten"
        self.server.publish_feedback(feedback)

        self.gripper_on()

        rospy.sleep(1.0)

        # --------------------------------------------------
        # TERUG NAAR HOME
        # --------------------------------------------------

        feedback.status = "Terug naar homepositie"
        self.server.publish_feedback(feedback)

        self.move_to_named_target("home")

        # --------------------------------------------------
        # ACTIE VOLTOOID
        # --------------------------------------------------

        rospy.loginfo("Robot actie succesvol voltooid")

        result.success = True

        self.server.set_succeeded(result)

    # ==================================================
    # ROBOT FUNCTIES
    # ==================================================

    def move_to_named_target(self, target_name):

        rospy.loginfo("Ga naar named target: %s", target_name)

        self.group.set_named_target(target_name)

        success = self.group.go(wait=True)

        self.group.stop()
        self.group.clear_pose_targets()

        return success

    def move_to_pose(self, pose):

        rospy.loginfo("Beweeg naar pose")

        self.group.set_start_state_to_current_state()
        self.group.set_pose_target(pose)

        success = self.group.go(wait=True)

        self.group.stop()
        self.group.clear_pose_targets()

        return success

    def pick(self, pose, descend_distance=0.03):

        rospy.loginfo("Start pick operatie")

        # --------------------------------------------------
        # BOVEN OBJECT
        # --------------------------------------------------

        if not self.move_to_pose(pose):
            return False

        # --------------------------------------------------
        # ZAKKEN
        # --------------------------------------------------

        lowered_pose = Pose()

        lowered_pose.position.x = pose.position.x
        lowered_pose.position.y = pose.position.y
        lowered_pose.position.z = pose.position.z - descend_distance

        lowered_pose.orientation = pose.orientation

        if not self.move_to_pose(lowered_pose):
            return False

        # --------------------------------------------------
        # VACUUM AAN
        # --------------------------------------------------

        rospy.sleep(1.0)

        self.gripper_off()

        # --------------------------------------------------
        # TERUG OMHOOG
        # --------------------------------------------------

        if not self.move_to_pose(pose):
            return False

        rospy.loginfo("Pick operatie voltooid")

        return True

    # ==================================================
    # GRIPPER
    # ==================================================

    def gripper_on(self):

        rospy.loginfo("Gripper AAN")

        subprocess.call([
            'rosservice',
            'call',
            '/ufactory/vacuum_gripper_set',
            '1'
        ])

    def gripper_off(self):

        rospy.loginfo("Gripper UIT")

        subprocess.call([
            'rosservice',
            'call',
            '/ufactory/vacuum_gripper_set',
            '0'
        ])


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    rospy.init_node("robot_controller_node")

    RobotController()

    rospy.spin()