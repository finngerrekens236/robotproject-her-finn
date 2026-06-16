#!/usr/bin/env python2

import Tkinter as tk
import rospy
import threading

from std_msgs.msg import String
from hoofdprogramma.srv import StartCyclus, SingleStart, StopCyclus, ResetCyclus


class HMIApp:

    def __init__(self):

        rospy.init_node('ros_hmi_node', anonymous=True)

        # =========================
        # ROS INTERFACE
        # =========================

        self.start_service = rospy.ServiceProxy('/start_cyclus', StartCyclus)
	self.single_service = rospy.ServiceProxy('/single_start', SingleStart)
        self.stop_service = rospy.ServiceProxy('/stop_cyclus', StopCyclus)
	self.reset_service = rospy.ServiceProxy('/reset_cyclus', ResetCyclus)

        rospy.Subscriber('/system/status', String, self.update_lights)

        # =========================
        # STATE
        # =========================
        self.state = "startup"

        # =========================
        # GUI THREAD
        # =========================
        self.gui_thread = threading.Thread(target=self.setup_gui)
        self.gui_thread.daemon = True
        self.gui_thread.start()

        rospy.spin()

    # =========================
    # GUI
    # =========================
    def setup_gui(self):

        self.master = tk.Tk()
        self.master.title("ROS HMI")
        self.master.geometry("300x450")
        self.master.configure(bg="#dcdcdc")

        self.button_frame = tk.Frame(self.master, bg="#dcdcdc")
        self.button_frame.pack(pady=10)

        # START CYCLUS
        self.cyclus_btn = tk.Button(
            self.button_frame,
            text="Cyclus Start",
            width=20,
            command=self.start_cyclus
        )
        self.cyclus_btn.grid(row=0, column=0, pady=5)

	#START SINGLE
	self.single_btn = tk.Button(
    	    self.button_frame,
            text="Single Start",
    	    width=20,
    	    command=self.single_start
	)
	self.single_btn.grid(row=1, column=0, pady=5)

        # STOP
        self.stop_btn = tk.Button(
            self.button_frame,
            text="Stop",
            width=20,
            command=self.stop_cyclus
        )
        self.stop_btn.grid(row=2, column=0, pady=5)

	#RESET
	self.reset_btn = tk.Button(
    	    self.button_frame,
    	    text="Reset",
    	    width=20,
    	    command=self.reset_cyclus
	)
	self.reset_btn.grid(row=3, column=0, pady=5)

        # STATUS
        self.status_label = tk.Label(self.master, text="Status:", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.green_light = tk.Label(self.master, text="IDLE", bg="gray", width=15, height=2)
        self.green_light.pack(pady=2)

        self.orange_light = tk.Label(self.master, text="RUNNING", bg="gray", width=15, height=2)
        self.orange_light.pack(pady=2)

        self.red_light = tk.Label(self.master, text="ERROR", bg="gray", width=15, height=2)
        self.red_light.pack(pady=2)

        self.master.mainloop()

    # =========================
    # START CYCLUS
    # =========================
    def start_cyclus(self):

        rospy.loginfo("Cyclus START knop gedrukt")

        try:
            resp = self.start_service(True)
            rospy.loginfo(resp.message)

        except rospy.ServiceException as e:
            rospy.logerr("Start service fout: %s", e)

    # =========================
    # START SINGLE
    # =========================

    def single_start(self):

    	rospy.loginfo("Single start knop")

    	try:
            resp = self.single_service(True)
            rospy.loginfo(resp.message)

   	except rospy.ServiceException as e:
            rospy.logerr("Single start fout: %s", e)

    # =========================
    # STOP CYCLUS
    # =========================
    def stop_cyclus(self):

        rospy.loginfo("Cyclus STOP knop gedrukt")

        try:
            resp = self.stop_service(True)
            rospy.loginfo(resp.message)

        except rospy.ServiceException as e:
            rospy.logerr("Stop service fout: %s", e)

    # =========================
    # RESET CYCLUS
    # =========================

    def reset_cyclus(self):

    	rospy.loginfo("RESET knop gedrukt")

        try:
            resp = self.reset_service(True)
       	    rospy.loginfo(resp.message)

        except rospy.ServiceException as e:
            rospy.logerr("Reset fout: %s", e)

    # =========================
    # STATUS UPDATE
    # =========================
    def update_lights(self, msg):

        status = msg.data.lower()

        self.set_all_lights("gray")

        if status == "cyclus_start":
            self.orange_light.config(bg="orange")
        elif status == "conveyor_running":
            self.orange_light.config(bg="orange")
        elif status == "idle":
            self.green_light.config(bg="green")
        elif status == "fout":
            self.red_light.config(bg="red")
	elif status == "single_running":
    	    self.orange_light.config(bg="orange")
	elif status == "cyclus_running":
    	    self.orange_light.config(bg="orange")
        else:
            rospy.logwarn("Onbekende status: %s", status)

    # =========================
    # HELPER
    # =========================
    def set_all_lights(self, color):
        self.green_light.config(bg=color)
        self.orange_light.config(bg=color)
        self.red_light.config(bg=color)


if __name__ == '__main__':
    try:
        HMIApp()
    except rospy.ROSInterruptException:
        pass
