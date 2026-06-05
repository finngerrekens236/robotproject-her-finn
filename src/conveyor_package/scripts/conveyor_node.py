#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
import serial

ser = None
product_ready_pub = None


def control_callback(msg):
    if ser is None:
        return

    if msg.data == "start":
        ser.write(b"start\n")

    elif msg.data == "stop":
        ser.write(b"stop\n")


if __name__ == '__main__':

    rospy.init_node('conveyor_node')

    port = rospy.get_param("~port", "/dev/ttyACM0")

    try:
        ser = serial.Serial(port, 9600, timeout=1)
        rospy.sleep(2)
        rospy.loginfo("Serial connected: %s", port)

    except Exception as e:
        rospy.logerr("Serial error: %s", e)
        ser = None

    rospy.Subscriber('/conveyor/control', String, control_callback)

    product_ready_pub = rospy.Publisher(
        '/conveyor/product_ready',
        Bool,
        queue_size=10
    )

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        if ser and ser.in_waiting > 0:

            line = ser.readline().decode('utf-8', errors='ignore').strip()

            if not line:
                continue

            # ==========================
            # STATE MAPPING
            # ==========================

            if line == "Conveyor: Idle":
                rospy.loginfo("Conveyor: Idle (wacht op product)")

            elif line == "Conveyor: Running":
                rospy.loginfo("Conveyor: Running (product onderweg)")

            elif line == "Conveyor: Ready":
                rospy.loginfo("Conveyor: Ready (eindpositie bereikt)")
                product_ready_pub.publish(True)

        rate.sleep()
