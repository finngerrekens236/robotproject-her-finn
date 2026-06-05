#!/usr/bin/env python2
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from hoofdprogramma.msg import KwastDetection
from hoofdprogramma.srv import StartCyclus  # <-- aangepaste service
from xarm_msgs.msg import RobotMsg
from std_srvs.srv import Trigger

class Hoofdprogramma(object):
    def __init__(self):
        rospy.init_node('hoofdprogramma_node')

        # Interne status
        self.homing_done = False
        self.kwast_ontvangen = False
        self.kwast_pose = None
        self.kwast_type = ""
        self.loop_mode = False
        self.emergency_stop = False
	self.last_robot_err = 0

        # Publishers
        self.transportband_pub = rospy.Publisher('/transportband_command', String, queue_size=10)
        self.status_pub = rospy.Publisher('/status_light', String, queue_size=10)
        self.vision_enable_pub = rospy.Publisher('/vision_enable', String, queue_size=1)

        # Subscribers
        rospy.Subscriber('/transportband_status', String, self.transportband_status_cb)
        rospy.Subscriber('/kwast_detectie', KwastDetection, self.kwast_detectie_cb)
        rospy.Subscriber('/hmi_commands', String, self.hmi_command_cb)
        rospy.Subscriber("/ufactory/robot_states", RobotMsg, self.robot_state_cb)

        rospy.spin()

    # ==== Noodstop ===
    def robot_state_cb(self, msg):
        if msg.err == 2 and self.last_robot_err != 2 and not self.emergency_stop:
            rospy.logwarn("Robot E-Stop geactiveerd! (err=2)")
            self.emergency_stop = True
            self.status_pub.publish("noodstop")
            self.transportband_pub.publish("stop")

	self.last_robot_err = msg.err

    # === Stap 0: HMI input ===
    def hmi_command_cb(self, msg):
        if self.emergency_stop:
            rospy.logwarn("Stap afgebroken door noodstop.")
            return
        
        rospy.loginfo("Ontvangen HMI-commando: %s", msg.data)
        if msg.data == "home":
            rospy.loginfo("Stap 0: stuur carrousel naar home")
            self.transportband_pub.publish("home")
        elif msg.data == "single_start":
            if not self.homing_done:
                rospy.logwarn("Kan niet starten: homing is nog niet voltooid.")
                return
            self.start_cyclus()
        elif msg.data == "start_cyclus":
            if not self.homing_done:
                rospy.logwarn("Kan niet starten: homing is nog niet voltooid.")
                return
            self.loop_mode = True
            self.start_cyclus()
        elif msg.data == "stop":
            self.loop_mode = False
            rospy.loginfo("Cyclus is gestopt door gebruiker.")
        elif msg.data == "reset":
            rospy.loginfo("Reset ontvangen: systeem terug naar beginstatus.")

            # Probeer foutstatus op robot te clearen
            try:
                rospy.wait_for_service('/ufactory/clear_err', timeout=2)
                clear_srv = rospy.ServiceProxy('/ufactory/clear_err', Trigger)
                resp = clear_srv()
                if resp.success:
                    rospy.loginfo("Robotfout succesvol gewist.")
                else:
                    rospy.logwarn("Kon robotfout niet wissen: %s", resp.message)
            except Exception as e:
                rospy.logwarn("Service /ufactory/clear_err niet beschikbaar: %s", str(e))

            self.emergency_stop = False
            self.homing_done = False
            self.status_pub.publish("reset_voltooid")
	    self.transportband_pub.publish("home")

            rospy.sleep(0.2)

    # === Stap 1: Carrousel afwachten ===
    def transportband_status_cb(self, msg):
        status = msg.data.strip().lower()
        if "homing" in status and "klaar" in status:
            rospy.loginfo("Stap 1: Homing voltooid.")
            self.homing_done = True
        elif "cycle_done" in status:
            rospy.loginfo("Stap 1: Carrousel is klaar. Start visiondetectie.")
            self.start_vision_detectie()

    # === Stap 2: Detectie ontvangen ===
    def kwast_detectie_cb(self, msg):
        self.kwast_pose = msg.pose
        self.kwast_type = msg.kwast_type
        self.kwast_ontvangen = True
        rospy.loginfo("Stap 2: Type kwast gedetecteerd: %s", self.kwast_type)

    def start_cyclus(self):
        if self.emergency_stop:
            rospy.logwarn("Stap afgebroken door noodstop.")
            return

        rospy.loginfo("Stap 1: Start carrousel met single_start")
        self.kwast_ontvangen = False
        self.transportband_pub.publish("single_start")

    def start_vision_detectie(self):
        if self.emergency_stop:
            rospy.logwarn("Stap afgebroken door noodstop.")
            return

        rospy.loginfo("Stap 2: Vision ingeschakeld")
        self.vision_enable_pub.publish("aan")

        timeout = rospy.Time.now() + rospy.Duration(30.0)
        while not self.kwast_ontvangen and rospy.Time.now() < timeout:
            rospy.sleep(0.1)

        self.vision_enable_pub.publish("uit")

        if not self.kwast_ontvangen:
            rospy.logwarn("Stap 2: Geen kwast gevonden binnen tijd.")
            self.status_pub.publish("kwast_niet_gevonden")
            return

        # Ga door naar stap 3
        self.start_robotcyclus()

    # === Stap 3: Robot aansturen via service met kwast_type ===
    def start_robotcyclus(self):
        if self.emergency_stop:
            rospy.logwarn("Stap afgebroken door noodstop.")
            return

        rospy.loginfo("Stap 3: Start robotcyclus via service")
        rospy.wait_for_service('/start_robot_cyclus')
        try:
            start_srv = rospy.ServiceProxy('/start_robot_cyclus', StartCyclus)
            response = start_srv(self.kwast_type)

            if response.success:
                rospy.loginfo("Stap 3: Robotcyclus geslaagd: %s", response.message)
                #self.status_pub.publish("geslaagd")
            else:
                rospy.logwarn("Stap 3: Robotcyclus mislukt: %s", response.message)
                self.status_pub.publish("mislukt")
        except rospy.ServiceException as e:
            rospy.logerr("Stap 3: Service call faalde: %s", str(e))
            self.status_pub.publish("mislukt")

        # === Stap 4: Cyclus afronden ===
        self.kwast_ontvangen = False
        #self.status_pub.publish("cyclus_voltooid")
        rospy.loginfo("Stap 4: Cyclus volledig afgerond.")

        # Herstart indien in cyclus-modus
        if self.loop_mode:
            rospy.sleep(1.0)  # optionele kleine pauze
            self.start_cyclus()

if __name__ == '__main__':
    try:
        Hoofdprogramma()
    except rospy.ROSInterruptException:
        pass
