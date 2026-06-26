#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import threading
import subprocess
from std_msgs.msg import String, Bool
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from xarm_msgs.msg import RobotMsg
from xarm_msgs.srv import SetAxis, SetInt16, ClearErr

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
# =========================
SORT_POSES = {
    "spoon":       {"x": -0.1053, "y": 0.1424, "z": 0.1257},
    "tootbrush":   {"x": -0.0128, "y": 0.1466, "z": 0.2177},
    "fork":        {"x": -0.0071, "y": 0.2587, "z": 0.2179},
    "screwdriver": {"x": -0.1231, "y": 0.2553, "z": 0.1259},
}

DEFAULT_SORT_POSE = {"x": -0.0128, "y": 0.1466, "z": 0.2177}

LIFT_HEIGHT      = 0.10   # meter omhoog na pick
CONVEYOR_TIMEOUT = 7.0    # seconden max conveyor looptijd
VISION_DELAY     = 3.0    # seconden wachten na conveyor stop voor foto

# Veilige positie boven de transportband
SAFE_APPROACH = {
    "x":  -0.1040,
    "y":  -0.2725,
    "z":   0.2656,
    "qx": -1.000,
    "qy":  0.000,
    "qz":  0.000,
    "qw":  0.000,
}


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

        # NOODSTOP
        rospy.Subscriber(
            '/ufactory/robot_states',
            RobotMsg,
            self._robot_state_callback
        )
        rospy.Subscriber(
            '/custom/emergency_stop',
            Bool,
            self._external_estop_callback
        )

        # XARM RESET SERVICES
        self.motion_enable_srv = rospy.ServiceProxy('/ufactory/motion_ctrl', SetAxis)
        self.set_state_srv     = rospy.ServiceProxy('/ufactory/set_state',   SetInt16)
        self.clear_error_srv   = rospy.ServiceProxy('/ufactory/clear_err',   ClearErr)

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
    # ROBOT STATE CALLBACK
    # Fysieke noodstop knop op de robot
    # =========================
    def _robot_state_callback(self, msg):
        # state 4 = error, state 5 = noodstop ingedrukt
        if msg.state in [4, 5]:
            rospy.logwarn("NOODSTOP GEDETECTEERD (robot state: %d)", msg.state)
            self._trigger_estop()

    # =========================
    # EXTERNE NOODSTOP CALLBACK
    # =========================
    def _external_estop_callback(self, msg):
        if msg.data:
            rospy.logwarn("EXTERNE NOODSTOP GEACTIVEERD")
            self._trigger_estop()

    # =========================
    # NOODSTOP LOGICA
    # =========================
    def _trigger_estop(self):

        if self.state == "idle":
            return

        rospy.logerr("NOODSTOP - alles stopt")

        self.state = "idle"

        # Conveyor stoppen
        try:
            self.conveyor_srv(False)
        except Exception as e:
            rospy.logerr("Conveyor stop fout: %s", e)

        # Robot direct stoppen
        self.group.stop()
        self.group.clear_pose_targets()

        # Gripper open zodat object niet vastgehouden blijft
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

        # HMI foutlamp aan
        self.status_pub.publish("fout")

    # =========================
    # ROBOT FOUT RESET
    # Wist error state 4 na noodstop loslaten
    # SetAxis(id, data): id=8 = alle assen, data=1 = enable
    # SetInt16(data):    data=0 = normale modus
    # =========================
    def _reset_robot_error(self):

        try:
            rospy.loginfo("Robot fout clearen...")

            self.clear_error_srv()           # wis de error
            rospy.sleep(0.5)

            self.motion_enable_srv(8, 1)     # motion enable alle assen
            rospy.sleep(0.5)

            self.set_state_srv(0)            # state 0 = klaar voor gebruik
            rospy.sleep(0.5)

            rospy.loginfo("Robot reset klaar")

        except Exception as e:
            rospy.logerr("Robot reset mislukt: %s", e)
# MoveIt controller herstellen na aborted state (toegevoegd)
    	try:
            rospy.loginfo("MoveIt controller herstellen...")
            self.group.stop()
            self.group.clear_pose_targets()

        # Gebruik de moveit_clear_err service die jouw robot aanbiedt
            moveit_clear = rospy.ServiceProxy('/ufactory/moveit_clear_err', ClearErr)
            moveit_clear()
            rospy.sleep(1.0)

            rospy.loginfo("MoveIt controller klaar")

    	except Exception as e:
            rospy.logerr("MoveIt controller reset mislukt: %s", e)
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

        # Robot error clearen en daarna naar home
        threading.Thread(target=self._reset_and_home).start()

        return ResetCyclusResponse(True, "reset: robot fout gecleard en gaat naar home")

    # =========================
    # RESET EN HOME (in thread)
    # =========================
    def _reset_and_home(self):
        self._reset_robot_error()
        self._go_home()

    # =========================
    # PLAN EN UITVOER HELPER
    # =========================
    def _plan_and_execute(self, label):

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
            self.status_pub.publish("fout")
            self.group.clear_pose_targets()
            return False

    # =========================
    # CONVEYOR WACHT HELPER
    # =========================
    def _wait_for_conveyor(self, expected_state):

        conveyor_start = rospy.Time.now()

        while not self.conveyor_ready:

            if self.state != expected_state:
                rospy.loginfo("Cyclus onderbroken tijdens conveyor wachten")
                self.conveyor_srv(False)
                return False

            elapsed = (rospy.Time.now() - conveyor_start).to_sec()

            if elapsed > CONVEYOR_TIMEOUT:
                rospy.logwarn(
                    "Conveyor timeout! Langer dan %.1f sec actief - gestopt",
                    CONVEYOR_TIMEOUT
                )
                self.conveyor_srv(False)
                self.status_pub.publish("fout")
                self.state = "idle"
                return False

            rospy.sleep(0.1)

        return True

    # =========================
    # HOME BEWEGING
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
    # VEILIGE POSITIE BOVEN BAND
    # =========================
    def _go_safe_approach(self):

        rospy.loginfo("GA NAAR VEILIGE POSITIE BOVEN BAND")

        approach_pose = Pose()
        approach_pose.position.x    = SAFE_APPROACH["x"]
        approach_pose.position.y    = SAFE_APPROACH["y"]
        approach_pose.position.z    = SAFE_APPROACH["z"]
        approach_pose.orientation.x = SAFE_APPROACH["qx"]
        approach_pose.orientation.y = SAFE_APPROACH["qy"]
        approach_pose.orientation.z = SAFE_APPROACH["qz"]
        approach_pose.orientation.w = SAFE_APPROACH["qw"]

        self.group.set_pose_target(approach_pose)
        return self._plan_and_execute("Veilige positie boven band")

    # =========================
    # CYCLUS LOGICA
    # =========================
    def _run_cyclus(self):

        rospy.loginfo("CYCLUS GESTART - druk Stop om te stoppen")

        while self.state == "cyclus_running":

            self.conveyor_ready = False
            self.conveyor_srv(True)
            rospy.loginfo("Wachten op object bij startsensor...")

            if not self._wait_for_conveyor("cyclus_running"):
                return

            rospy.loginfo("CONVEYOR READY - wachten %.1f sec voor foto...", VISION_DELAY)
            rospy.sleep(VISION_DELAY)
            rospy.loginfo("VISION START")

            vision = self.vision_srv()

            if not (vision and vision.success):
                self.status_pub.publish("fout")
                rospy.logwarn("Geen object gedetecteerd, volgende ronde...")
                rospy.sleep(3.0)
                continue

            self._move_robot(vision.pick_pose, vision.object_class)

            rospy.loginfo("Ronde klaar - volgende ronde start...")

        rospy.loginfo("CYCLUS GESTOPT")

    # =========================
    # SINGLE LOGICA
    # =========================
    def _run_single(self):

        self.conveyor_ready = False
        self.conveyor_srv(True)

        if not self._wait_for_conveyor("single_running"):
            self.state = "idle"
            return

        rospy.loginfo("CONVEYOR READY - wachten %.1f sec voor foto...", VISION_DELAY)
        rospy.sleep(VISION_DELAY)
        rospy.loginfo("VISION START")

        vision = self.vision_srv()

        if vision and vision.success:
            self._move_robot(vision.pick_pose, vision.object_class)
        else:
            self.status_pub.publish("fout")
            rospy.logwarn("Geen object gedetecteerd, reset")

        self.state = "idle"

    # =========================
    # MOVEIT FUNCTIE
    # =========================
    def _move_robot(self, pose_stamped, object_class):

        rospy.loginfo("ROBOT BEWEGING START voor object: %s", object_class)

        # --- Gripper open ---
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
        # STAP 1: VEILIGE POSITIE BOVEN BAND
        # =========================
        if not self._go_safe_approach():
            return

        if self.state == "idle":
            return

        # =========================
        # STAP 2: PICK POSITIE
        # =========================
        self.group.set_pose_target(pose)
        if not self._plan_and_execute("Pick positie"):
            return

        if self.state == "idle":
            return

        # --- Gripper dicht ---
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])
        rospy.sleep(0.5)

        # =========================
        # STAP 3: LIFT OMHOOG
        # =========================
        lift_pose = Pose()
        lift_pose.position.x = pose.position.x
        lift_pose.position.y = pose.position.y
        lift_pose.position.z = pose.position.z + LIFT_HEIGHT
        lift_pose.orientation = pose.orientation

        rospy.loginfo("LIFT OMHOOG naar z=%.4f", lift_pose.position.z)

        self.group.set_pose_target(lift_pose)
        if not self._plan_and_execute("Lift"):
            rospy.logwarn("Lift mislukt, direct naar sorteerbak proberen")

        if self.state == "idle":
            return

        # =========================
        # STAP 4: SORTEERBAK
        # =========================
        coords = SORT_POSES.get(object_class, DEFAULT_SORT_POSE)
        rospy.loginfo(
            "GA NAAR SORTEERBAK voor '%s' -> x=%.4f, y=%.4f, z=%.4f",
            object_class, coords["x"], coords["y"], coords["z"]
        )

        safe_pose = Pose()
        safe_pose.position.x    = coords["x"]
        safe_pose.position.y    = coords["y"]
        safe_pose.position.z    = coords["z"]
        safe_pose.orientation.x = -1.000
        safe_pose.orientation.y =  0.001
        safe_pose.orientation.z =  0.000
        safe_pose.orientation.w =  0.000

        self.group.set_pose_target(safe_pose)
        if not self._plan_and_execute("Sorteerbak"):
            return

        if self.state == "idle":
            return

        # --- Gripper open ---
        subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])
        rospy.sleep(0.5)

        # =========================
        # STAP 5: HOME
        # =========================
        self._go_home()


if __name__ == '__main__':
    Hoofdprogramma()
