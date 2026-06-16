#!/usr/bin/env python2

import rospy
from std_msgs.msg import String
from my_depthai.srv import DetectObject
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


class Hoofdprogramma:

    def __init__(self):

        rospy.init_node('hoofdprogramma_node')

        # =========================
        # STATE MACHINE
        # =========================
        self.state = "idle"

        # =========================
        # STATUS PUBLISHER
        # =========================
        self.status_pub = rospy.Publisher(
            '/system/status',
            String,
            queue_size=10
        )

        # =========================
        # CONVEYOR CLIENT
        # =========================
        self.conveyor_srv = rospy.ServiceProxy(
            '/conveyor_control',
            ConveyorControl
        )
        # =========================
        # VISION CLIENT
        # =========================
	self.vision_srv = rospy.ServiceProxy(
    	    '/vision/detect_object',
    	    DetectObject
	)

        # =========================
        # SERVICES
        # =========================
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

        rospy.loginfo("Hoofdprogramma ready")

        rospy.spin()

    # ==================================================
    # CYCLUS START
    # ==================================================
    def start_callback(self, req):

        if self.state != "idle":
            return StartCyclusResponse(False, "Systeem bezig")

        rospy.loginfo("Cyclus gestart")

        self.state = "cyclus_running"
        self.status_pub.publish("cyclus_start")

        self.conveyor_srv(True)

        self.status_pub.publish("conveyor_running")

        return StartCyclusResponse(True, "Cyclus gestart")

    # ==================================================
    # SINGLE START
    # ==================================================
    def single_callback(self, req):

        if self.state != "idle":
            return SingleStartResponse(False, "Systeem bezig")

        rospy.loginfo("Single start")

        self.state = "single_running"

        self.conveyor_srv(True)

        self.status_pub.publish("single_running")

        return SingleStartResponse(True, "Single cycle gestart")

    # ==================================================
    # STOP
    # ==================================================
    def stop_callback(self, req):

        rospy.loginfo("STOP CYCLUS")

        self.conveyor_srv(False)

        self.state = "idle"

        self.status_pub.publish("idle")

        return StopCyclusResponse(True, "Cyclus gestopt")

    # ==================================================
    # RESET
    # ==================================================
    def reset_callback(self, req):

        rospy.loginfo("RESET CYCLUS")

        self.conveyor_srv(False)

        self.state = "idle"

        self.status_pub.publish("idle")

        return ResetCyclusResponse(True, "Systeem gereset")


if __name__ == '__main__':
    Hoofdprogramma()
