#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import threading
import subprocess
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


# =========================
# SORTEERBAK COORDINATEN
# Per object class een eigen afzetpositie.
# Pas de x/y/z waarden aan naar jouw opstelling.
# =========================
SORT_POSES = {
    "spoon":       {"x": -0.1053, "y": 0.1424, "z": 0.1257},
    "tootbrush":   {"x": -0.0128, "y": 0.1466, "z": 0.2177},
    "fork":        {"x": -0.0071, "y": 0.2587, "z": 0.2179},
    "screwdriver": {"x": -0.1231, "y": 0.2553, "z": 0.1259},
}

# Fallback als het gedetecteerde object niet in de lijst staat
DEFAULT_SORT_POSE = {"x": -0.0128, "y": 0.1466, "z": 0.2177}

# Hoogte van de lift tussenstap na pick (in meters)
LIFT_HEIGHT = 0.10


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
        rospy.Service('/start_cyclus',  StartCyclus,  self.start_callback)
        rospy.Service('/single_start',  SingleStart,  self.single_callback)
        rospy.Service('/stop_cyclus',   StopCyclus,   self.stop_callback)
        rospy.Service('/reset_cyclus',  ResetCyclus,  self.reset_callback)

        rospy.loginfo("Services geregistreerd")

        # CONVEYOR
        self.conveyor_srv = rospy.ServiceProxy('/conveyor_control', ConveyorControl)

        # VISION
        self.vision_srv = rospy.ServiceProxy('/vision/detect_object', DetectObject)

        # MOVEIT
        self.group = MoveGroupCommander("arm")
        self.group.set_pose_reference_frame("world")
        self.group.set_planning_time(5.0)
        self.group.set_num_planning_attempts(50)
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

        # Gripper open zodat er niets vastzit
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

        # Rij naar home in een aparte thread zodat de service direct terugkeert
        threading.Thread(target=self._go_home).start()

        return ResetCyclusResponse(True, "reset: robot gaat naar home")

    # =========================
    # PLAN EN UITVOER HELPER
    # Voorkomt herhaalde if/isinstance blokken
    # =========================
    def _plan_and_execute(self, label):
        """Plan vanuit de huidige pose target en voer uit. Geeft True/False terug."""

        plan = self.group.plan()

        if isinstance(plan, tuple):
            success    = plan[0]
            trajectory = plan[1]
        else:
            trajectory = plan
            success    = True

        if success and trajectory.joint_trajectory.points:
            self.group.execute(trajectory, wait=True)
            self.group.stop()
            self.group.clear_pose_targets()
            rospy.loginfo("%s bereikt", label)
            return True
        else:
            rospy.logwarn("%s planning mislukt", label)
            self.group.clear_pose_targets()
            return False

    # =========================
    # HOME BEWEGING (herbruikbaar)
    # =========================
    def _go_home(self):

        rospy.loginfo("GA NAAR HOME POSITIE")

        self.group.stop()
        self.group.clear_pose_targets()

        home_pose = Pose()
        home_pose.position.x =  -0.0575
        home_pose.position.y =  -0.0000
        home_pose.position.z =   0.4731
        home_pose.orientation.x = -1.000
        home_pose.orientation.y =  0.001
        home_pose.orientation.z =  0.000
        home_pose.orientation.w =  0.000

        self.group.set_pose_target(home_pose)
        self._plan_and_execute("HOME")

    # =========================
    # CYCLUS LOGICA  ← herhalend
    # =========================
    def _run_cyclus(self):

        rospy.loginfo("CYCLUS GESTART - druk Stop om te stoppen")

        while self.state == "cyclus_running":

            # --- Stap 1: conveyor aan ---
            self.conveyor_ready = False
            self.conveyor_srv(True)
            rospy.loginfo("Wachten op object bij startsensor...")

            # --- Stap 2: wacht op READY van conveyor ---
            while not self.conveyor_ready:
                if self.state != "cyclus_running":
                    rospy.loginfo("Cyclus onderbroken tijdens conveyor wachten")
                    self.conveyor_srv(False)
                    return
                rospy.sleep(0.1)

            rospy.loginfo("CONVEYOR READY - VISION START")

            # --- Stap 3: vision ---
            vision = self.vision_srv()

            if not (vision and vision.success):
                rospy.logwarn("Geen object gedetecteerd, volgende ronde...")
                rospy.sleep(3.0)
                continue

            # --- Stap 4: robot beweegt ---
            self._move_robot(vision.pick_pose, vision.object_class)

            rospy.loginfo("Ronde klaar - volgende ronde start...")

        rospy.loginfo("CYCLUS GESTOPT")

    # =========================
    # SINGLE LOGICA  ← één ronde
    # =========================
    def _run_single(self):

        self.conveyor_ready = False
        self.conveyor_srv(True)

        while not self.conveyor_ready:
            if self.state != "single_running":
                self.conveyor_srv(False)
                return
            rospy.sleep(0.1)

        rospy.loginfo("VISION START")

        vision = self.vision_srv()

        if vision and vision.success:
            self._move_robot(vision.pick_pose, vision.object_class)

        self.state = "idle"

    # =========================
    # MOVEIT FUNCTIE
    # =========================
    def _move_robot(self, pose_stamped, object_class):

        rospy.loginfo("ROBOT BEWEGING START voor object: %s", object_class)

        # --- Gripper open (zuig uit) ---
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

        pose = Pose()
        pose.position = pose_stamped.pose.position

        rospy.loginfo(
            "INCOMING POSITION -> X: %.4f, Y: %.4f, Z: %.4f",
            pose.position.x, pose.position.y, pose.position.z
        )
        rospy.loginfo(
            "INCOMING VALUES -> z: %.6f, w: %.6f",
            pose_stamped.pose.orientation.z,
            pose_stamped.pose.orientation.w
        )

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

        # =========================
        # STAP 1: PICK POSITIE
        # =========================
        self.group.set_pose_target(pose)
        if not self._plan_and_execute("Pick positie"):
            return

        # --- Gripper dicht (vast zuigen) ---
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])
        rospy.sleep(0.5)

        # =========================
        # STAP 2: LIFT OMHOOG
        # Recht omhoog vanuit pick positie zodat MoveIt een
        # makkelijk vertrekpunt heeft naar de sorteerbak.
        # =========================
        lift_pose = Pose()
        lift_pose.position.x = pose.position.x
        lift_pose.position.y = pose.position.y
        lift_pose.position.z = pose.position.z + LIFT_HEIGHT
        lift_pose.orientation = pose.orientation   # zelfde yaw behouden

        rospy.loginfo("LIFT OMHOOG naar z=%.4f", lift_pose.position.z)

        self.group.set_pose_target(lift_pose)
        if not self._plan_and_execute("Lift"):
            # Lift mislukt: probeer toch door te gaan naar sorteerbak
            rospy.logwarn("Lift mislukt, direct naar sorteerbak proberen")

        # =========================
        # STAP 3: SORTEERBAK
        # Vaste oriëntatie zodat de arm altijd op dezelfde
        # manier aankomt, ongeacht de pick-yaw.
        # =========================
        coords = SORT_POSES.get(object_class, DEFAULT_SORT_POSE)
        rospy.loginfo(
            "GA NAAR SORTEERBAK voor '%s' -> x=%.4f, y=%.4f, z=%.4f",
            object_class, coords["x"], coords["y"], coords["z"]
        )

        safe_pose = Pose()
        safe_pose.position.x  = coords["x"]
        safe_pose.position.y  = coords["y"]
        safe_pose.position.z  = coords["z"]

        # Vaste oriëntatie voor de sorteerbak (geen variabele yaw)
        safe_pose.orientation.x = -1.000
        safe_pose.orientation.y =  0.001
        safe_pose.orientation.z =  0.000
        safe_pose.orientation.w =  0.000

        self.group.set_pose_target(safe_pose)
        if not self._plan_and_execute("Sorteerbak"):
            return

        # --- Gripper open (loslaten) ---
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])
        rospy.sleep(0.5)

        # =========================
        # STAP 4: HOME
        # =========================
        self._go_home()


if __name__ == '__main__':
    Hoofdprogramma()
