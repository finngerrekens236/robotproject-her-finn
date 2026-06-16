#!/usr/bin/env python

import rospy
import serial
from std_msgs.msg import String

from hoofdprogramma.srv import (
    ConveyorControl,
    ConveyorControlResponse
)


class ConveyorNode:

    def __init__(self):

        rospy.init_node('conveyor_node')

        # =========================
        # SERIAL CONNECTION
        # =========================
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            rospy.sleep(2)
            rospy.loginfo("Arduino verbonden")
        except Exception as e:
            rospy.logerr("Geen Arduino verbinding: %s", e)
            self.ser = None

        # =========================
        # STATE
        # =========================
        self.ready = False
        self.running = False

        # =========================
        # STATUS PUBLISHER
        # =========================
        self.status_pub = rospy.Publisher(
            '/system/status',
            String,
            queue_size=10
        )

        # =========================
        # SERVICE
        # =========================
        rospy.Service(
            '/conveyor_control',
            ConveyorControl,
            self.control_callback
        )

        rospy.loginfo("Conveyor service ready")

        # =========================
        # SERIAL LOOP
        # =========================
        rospy.Timer(rospy.Duration(0.05), self.read_serial)

        rospy.spin()

    # ==================================================
    # SERVICE CALLBACK
    # ==================================================
    def control_callback(self, req):

        if req.run:

            rospy.loginfo("Conveyor START")

            self.ready = False
            self.running = True

            if self.ser:
                self.ser.write(b"start\n")

            self.status_pub.publish("conveyor_running")

            return ConveyorControlResponse(
                True,
                "Conveyor gestart",
                "RUNNING"
            )

        else:

            rospy.loginfo("Conveyor STOP")

            self.running = False

            if self.ser:
                self.ser.write(b"stop\n")

            self.status_pub.publish("idle")

            return ConveyorControlResponse(
                True,
                "Conveyor gestopt",
                "IDLE"
            )

    # ==================================================
    # SERIAL INPUT HANDLER
    # ==================================================
    def read_serial(self, event):

        if not self.ser:
            return

        if self.ser.in_waiting > 0:

            line = self.ser.readline().decode(errors='ignore').strip()

            if not line:
                return

            # DEBUG
            rospy.loginfo("Arduino RAW: %s", line)

            # ==================================================
            # READY DETECTIE (ROBUST)
            # ==================================================
            if "READY" in line.upper():

                rospy.loginfo("CONVEYOR READY (eindsensor bereikt)")
                self.ready = True

                self.status_pub.publish("conveyor_ready")

            # ==================================================
            # IDLE DETECTIE
            # ==================================================
            elif "IDLE" in line.upper():

                self.ready = False
                self.running = False
                self.status_pub.publish("idle")


# ==================================================
# MAIN
# ==================================================
if __name__ == '__main__':
    ConveyorNode()
