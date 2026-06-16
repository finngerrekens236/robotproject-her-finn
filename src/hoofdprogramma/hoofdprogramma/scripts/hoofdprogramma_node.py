#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import threading

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler, euler_from_quaternion

from moveit_commander import MoveGroupCommander

from hoofdprogramma.srv import (
    StopCyclus,
    StopCyclusResponse,
    StartCyclus,
    StartCyclusResponse,
    SingleStart,
    SingleStartResponse,
    ResetCyclus,
    ResetCyclusResponse,
    ConveyorControl
)

from my_depthai.srv import DetectObject


class Hoofdprogramma(object):

    def __init__(self):

        rospy.init_node('hoofdprogramma_node')

        self.state = "idle"
        self.conveyor_ready = False

        # STATUS
        self.status_pub = rospy.Publisher(
            '/system/status',
            String,
            queue_size=10
        )

        rospy.Subscriber(
            '/system/status',
            String,
            self.status_callback
        )

        # SERVICES
        rospy.Service(
            '/start_cyclus',
            StartCyclus,
            self.start_callback
        )

        rospy.Service(
            '/single_start',
            SingleStart,
            self.single_callback
        )

        rospy.Service(
            '/stop_cyclus',
            StopCyclus,
            self.stop_callback
        )

        rospy.Service(
            '/reset_cyclus',
            ResetCyclus,
            self.reset_callback
        )

        rospy.loginfo("Services geregistreerd")

        # CONVEYOR
        self.conveyor_srv = rospy.ServiceProxy(
            '/conveyor_control',
            ConveyorControl
        )

        # VISION
        self.vision_srv = rospy.ServiceProxy(
            '/vision/detect_object',
            DetectObject
        )

        # MOVEIT
        self.group = MoveGroupCommander("arm")
        self.group.set_pose_reference_frame("link_base")
        self.group.set_max_velocity_scaling_factor(0.2)
        self.group.set_max_acceleration_scaling_factor(0.2)

        rospy.loginfo("Wachten op MoveIt...")
        rospy.sleep(2)
        rospy.loginfo("Systeem klaar")

        rospy.spin()

    # =========================
    # STATUS CALLBACK
    # =========================
    def status_callback(self, msg):

        if msg.data == "conveyor_ready":
            self.conveyor_ready = True

        elif msg.data == "conveyor_running":
            self.conveyor_ready = False

    # =========================
    # START CYCLUS
    # =========================
    def start_callback(self, req):

        if self.state != "idle":
            return StartCyclusResponse(False, "Systeem bezig")

        self.state = "cyclus_running"
        self.conveyor_ready = False

        threading.Thread(target=self._run_cyclus).start()

        return StartCyclusResponse(True, "OK")

    # =========================
    # SINGLE
    # =========================
    def single_callback(self, req):

        if self.state != "idle":
            return SingleStartResponse(False, "Systeem bezig")

        self.state = "single_running"
        self.conveyor_ready = False

        threading.Thread(target=self._run_single).start()

        return SingleStartResponse(True, "OK")

    # =========================
    # STOP / RESET
    # =========================
    def stop_callback(self, req):

        self.state = "idle"
        self.conveyor_srv(False)

        return StopCyclusResponse(True, "gestopt")

    def reset_callback(self, req):

        self.state = "idle"
        self.conveyor_srv(False)

        return ResetCyclusResponse(True, "reset")

    # =========================
    # CYCLUS LOGICA
    # =========================
    def _run_cyclus(self):

        self.conveyor_srv(True)

        while not self.conveyor_ready:

            if self.state != "cyclus_running":
                return

            rospy.sleep(0.2)

        rospy.loginfo("VISION START")

        vision = self.vision_srv()

        if vision and vision.success:

            pose = vision.pick_pose
            self._move_robot(pose)

        self.state = "idle"

    # =========================
    # SINGLE LOGICA
    # =========================
    def _run_single(self):

        self.conveyor_srv(True)

        while not self.conveyor_ready:

            if self.state != "single_running":
                return

            rospy.sleep(0.2)

        rospy.loginfo("VISION START")

        vision = self.vision_srv()

        if vision and vision.success:

            pose = vision.pick_pose
            self._move_robot(pose)

        self.state = "idle"

    # =========================
    # MOVEIT FUNCTIE
    # =========================
    def _move_robot(self, pose_stamped):

        rospy.loginfo("ROBOT BEWEGING START")

        pose = Pose()
        pose.position = pose_stamped.pose.position

        # Yaw uit vision halen, roll=180 toevoegen zodat grijper naar beneden wijst
        camera_q = [
            pose_stamped.pose.orientation.x,
            pose_stamped.pose.orientation.y,
            pose_stamped.pose.orientation.z,
            pose_stamped.pose.orientation.w,
        ]
        _, _, camera_yaw = euler_from_quaternion(camera_q)
        q = quaternion_from_euler(math.radians(180), 0.0, camera_yaw)
        pose.orientation.x = q[0]
        pose.orientation.y = q[1]
        pose.orientation.z = q[2]
        pose.orientation.w = q[3]

        self.group.set_pose_target(pose)

        plan = self.group.plan()

        if isinstance(plan, tuple):
            success = plan[0]
            trajectory = plan[1]
        else:
            trajectory = plan
            success = True

        if success and trajectory.joint_trajectory.points:
            self.group.execute(trajectory, wait=True)
            self.group.stop()
            self.group.clear_pose_targets()
            rospy.loginfo("Robot klaar")
        else:
            rospy.logwarn("Planning mislukt")
            self.group.clear_pose_targets()


if __name__ == '__main__':
    Hoofdprogramma()
