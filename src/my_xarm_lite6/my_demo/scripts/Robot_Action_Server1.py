#!/usr/bin/env python
# -- coding: utf-8 --

import sys
import rospy
import actionlib
import moveit_commander

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

import subprocess
import math

from tf.transformations import quaternion_from_euler, euler_from_quaternion

# TF2 FIX
import tf2_ros
import tf2_geometry_msgs

from my_demo.msg import PickPlaceAction, PickPlaceFeedback, PickPlaceResult


class RobotPickPlaceActionServer(object):

    _feedback = PickPlaceFeedback()
    _result = PickPlaceResult()

    def __init__(self, name):

        self._action_name = name

        # STATUS
        self.status_pub = rospy.Publisher('/robot/status', String, queue_size=10)
        self.publish_status("IDLE")

        # MOVEIT
        self.move_group = moveit_commander.MoveGroupCommander("arm")
        self.move_group.set_max_velocity_scaling_factor(0.2)
        self.move_group.set_max_acceleration_scaling_factor(0.2)
        self.move_group.set_planning_time(10)

        # TF2 LISTENER (BELANGRIJK)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        # ACTION SERVER
        self._as = actionlib.SimpleActionServer(
            self._action_name,
            PickPlaceAction,
            execute_cb=self.execute_cb,
            auto_start=False
        )

        self._as.start()
        rospy.loginfo("Robot Action Server gestart")

    def publish_status(self, msg):
        self.status_pub.publish(String(data=msg))

    # =========================================================
    # MAIN EXECUTION
    # =========================================================
    def execute_cb(self, goal):

        rospy.loginfo("Pick & Place goal ontvangen")
        self.publish_status("BUSY_PICKING")

        # -------------------------
        # GRIPPER OPEN
        # -------------------------
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

        # -------------------------
        # INPUT POSE (CAMERA FRAME)
        # -------------------------
        pose_in = goal.target_pose

        # -------------------------
        # TF TRANSFORM: camera → world
        # -------------------------
        try:
            transformed_pose = self.tf_buffer.transform(
                pose_in,
                "world",
                rospy.Duration(1.0)
            )
        except Exception as e:
            rospy.logerr("TF transform failed: %s", str(e))
            self.publish_status("ERROR_TF_FAILED")

            self._result.success = False
            self._as.set_aborted(self._result)
            return

        # -------------------------
        # SAFE POSE VARIABEL
        # -------------------------
        target_pose = transformed_pose

        # Optioneel: vaste Z hoogte (veilig pakvlak)
        target_pose.pose.position.z = 0.165

        # -------------------------
        # ORIENTATIE FIX
        # -------------------------
        q = [
            target_pose.pose.orientation.x,
            target_pose.pose.orientation.y,
            target_pose.pose.orientation.z,
            target_pose.pose.orientation.w
        ]

        _, _, yaw = euler_from_quaternion(q)

        roll = math.radians(180)
        pitch = 0.0

        q_new = quaternion_from_euler(roll, pitch, yaw)

        target_pose.pose.orientation.x = q_new[0]
        target_pose.pose.orientation.y = q_new[1]
        target_pose.pose.orientation.z = q_new[2]
        target_pose.pose.orientation.w = q_new[3]

        # -------------------------
        # MOVEIT PLANNING
        # -------------------------
        rospy.loginfo("Planning naar target pose...")

        self.move_group.set_pose_target(target_pose)

        success = self.move_group.go(wait=True)

        self.move_group.stop()
        self.move_group.clear_pose_targets()

        if not success:
            rospy.logerr("Planning mislukt")
            self.publish_status("ERROR_PLANNING_FAILED")

            self._result.success = False
            self._as.set_aborted(self._result)
            return

        # -------------------------
        # GRIPPER SLUIT
        # -------------------------
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])
        rospy.sleep(0.5)

        # -------------------------
        # LIFT
        # -------------------------
        lift_pose = self.move_group.get_current_pose().pose
        lift_pose.position.z += 0.05

        self.move_group.set_pose_target(lift_pose)

        success_lift = self.move_group.go(wait=True)

        self.move_group.stop()
        self.move_group.clear_pose_targets()

        # -------------------------
        # RESULT
        # -------------------------
        if success_lift:
            rospy.loginfo("Pick & Place succesvol")
            self.publish_status("IDLE")

            self._result.success = True
            self._as.set_succeeded(self._result)
        else:
            rospy.logerr("Lift mislukt")
            self.publish_status("ERROR_LIFT_FAILED")

            self._result.success = False
            self._as.set_aborted(self._result)


# =========================================================
# MAIN
# =========================================================
def main():

    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('robot_action_server_node')

    RobotPickPlaceActionServer('/robot/pick_place')

    rospy.spin()

    moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    main()
