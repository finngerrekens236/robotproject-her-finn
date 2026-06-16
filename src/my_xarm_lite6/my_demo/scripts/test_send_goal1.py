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

from my_demo.msg import PickPlaceAction, PickPlaceFeedback, PickPlaceResult


class RobotPickPlaceActionServer(object):

    _feedback = PickPlaceFeedback()
    _result = PickPlaceResult()

    def __init__(self, name):
        self._action_name = name

        self.status_pub = rospy.Publisher('/robot/status', String, queue_size=10)
        self.publish_status("IDLE")

        self.move_group = moveit_commander.MoveGroupCommander("arm")
        self.move_group.set_max_velocity_scaling_factor(0.2)
        self.move_group.set_max_acceleration_scaling_factor(0.2)

        self._as = actionlib.SimpleActionServer(
            self._action_name,
            PickPlaceAction,
            execute_cb=self.execute_cb,
            auto_start=False
        )
        self._as.start()

        rospy.loginfo("Robot Action Server actief")

    def publish_status(self, msg):
        self.status_pub.publish(String(data=msg))

    def execute_cb(self, goal):

        rospy.loginfo("Nieuw pick & place doel ontvangen")
        self.publish_status("BUSY_PICKING")

        # -----------------------------
        # GRIPPER OPEN
        # -----------------------------
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

        # -----------------------------
        # POSE OPBOUWEN (FIXED)
        # -----------------------------
        target_pose = PoseStamped()
        target_pose.header.frame_id = "world"
        target_pose.header.stamp = rospy.Time.now()

        target_pose.pose.position.x = goal.target_pose.position.x
        target_pose.pose.position.y = goal.target_pose.position.y
        target_pose.pose.position.z = 0.165

        # quaternion uit vision gebruiken
        qx = goal.target_pose.orientation.x
        qy = goal.target_pose.orientation.y
        qz = goal.target_pose.orientation.z
        qw = goal.target_pose.orientation.w

        _, _, yaw = euler_from_quaternion([qx, qy, qz, qw])

        # veilige robot oriëntatie (tool naar beneden + yaw)
        roll = math.radians(180)
        pitch = 0.0
        q = quaternion_from_euler(roll, pitch, yaw)

        target_pose.pose.orientation.x = q[0]
        target_pose.pose.orientation.y = q[1]
        target_pose.pose.orientation.z = q[2]
        target_pose.pose.orientation.w = q[3]

        # -----------------------------
        # DEBUG LOGGING (BELANGRIJK)
        # -----------------------------
        rospy.logwarn("===== MOVEIT TARGET =====")
        rospy.logwarn("FRAME: %s", target_pose.header.frame_id)
        rospy.logwarn("X Y Z: %.3f %.3f %.3f",
                      target_pose.pose.position.x,
                      target_pose.pose.position.y,
                      target_pose.pose.position.z)
        rospy.logwarn("Q: %.3f %.3f %.3f %.3f",
                      target_pose.pose.orientation.x,
                      target_pose.pose.orientation.y,
                      target_pose.pose.orientation.z,
                      target_pose.pose.orientation.w)

        # -----------------------------
        # MOVEIT PLANNING
        # -----------------------------
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

        # -----------------------------
        # GRIPPER SLUIT
        # -----------------------------
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])
        rospy.sleep(0.5)

        # -----------------------------
        # LIFT
        # -----------------------------
        lift_pose = self.move_group.get_current_pose().pose
        lift_pose.position.z += 0.05

        self.move_group.set_pose_target(lift_pose)
        success_lift = self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        # -----------------------------
        # RESULT
        # -----------------------------
        if success_lift:
            rospy.loginfo("Pick & place succesvol")
            self.publish_status("IDLE")
            self._result.success = True
            self._as.set_succeeded(self._result)
        else:
            rospy.logerr("Lift mislukt")
            self.publish_status("ERROR_LIFT_FAILED")
            self._result.success = False
            self._as.set_aborted(self._result)


def main():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('robot_action_server_node')

    RobotPickPlaceActionServer('/robot/pick_place')

    rospy.spin()
    moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    main()
