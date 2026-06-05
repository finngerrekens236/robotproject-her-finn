#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib

from hoofdprogramma.msg import (
    KwastDetection,
    PickAndPlaceAction,
    PickAndPlaceGoal
)

from hoofdprogramma.srv import (
    StartCyclus,
    StartCyclusResponse
)


class Hoofdprogramma(object):
    def __init__(self):
        rospy.init_node('hoofdprogramma_node')

        # --------------------------------------------------
        # STATUS VARIABELEN
        # --------------------------------------------------
        self.system_running = False
        self.current_detection = None
        self.robot_busy = False

        # --------------------------------------------------
        # VISION SUBSCRIBER
        # Ontvangt detectiegegevens van vision node
        # --------------------------------------------------
        rospy.Subscriber(
            '/vision/detection',
            KwastDetection,
            self.vision_callback
        )

        # --------------------------------------------------
        # SERVICE VANUIT HMI
        # HMI start hiermee de cyclus
        # --------------------------------------------------
        self.start_service = rospy.Service(
            '/start_cyclus',
            StartCyclus,
            self.handle_start_cyclus
        )

        # --------------------------------------------------
        # ACTION CLIENT NAAR ROBOT
        # Hoofdprogramma stuurt robot opdrachten
        # --------------------------------------------------
        self.robot_client = actionlib.SimpleActionClient(
            '/pick_and_place',
            PickAndPlaceAction
        )

        rospy.loginfo('Wachten op robot action server...')
        self.robot_client.wait_for_server()
        rospy.loginfo('Robot action server verbonden')

        rospy.loginfo('Hoofdprogramma gestart')

    # ==================================================
    # CALLBACKS
    # ==================================================

    def vision_callback(self, msg):
        """
        Ontvangt objectdetectie van vision node.
        """

        self.current_detection = msg

        rospy.loginfo(
            'Vision detectie ontvangen | Type: %s',
            msg.kwast_type
        )

    # ==================================================
    # HMI SERVICE
    # ==================================================

    def handle_start_cyclus(self, req):
        """
        Wordt aangeroepen vanuit HMI.
        Start volledige sorteercyclus.
        """

        if self.robot_busy:
            return StartCyclusResponse(
                success=False,
                message='Robot is momenteel bezig'
            )

        rospy.loginfo('Cyclus gestart vanuit HMI')

        self.system_running = True

        success = self.run_cycle(req.kwast_type)

        if success:
            return StartCyclusResponse(
                success=True,
                message='Cyclus succesvol voltooid'
            )

        return StartCyclusResponse(
            success=False,
            message='Cyclus mislukt'
        )

    # ==================================================
    # HOOFD CYCLUS
    # ==================================================

    def run_cycle(self, requested_type):
        """
        Centrale state machine van het systeem.
        """

        rospy.loginfo('--- START CYCLUS ---')

        # --------------------------------------------------
        # 1. Wacht op vision detectie
        # --------------------------------------------------
        detection = self.wait_for_detection(timeout=10)

        if detection is None:
            rospy.logwarn('Geen detectie ontvangen')
            return False

        # --------------------------------------------------
        # 2. Controleer kwasttype
        # --------------------------------------------------
        detected_type = detection.kwast_type.lower()
        requested_type = requested_type.lower()

        rospy.loginfo(
            'Gedetecteerd: %s | Gevraagd: %s',
            detected_type,
            requested_type
        )

        if detected_type != requested_type:
            rospy.logwarn('Kwasttype komt niet overeen')
            return False

        # --------------------------------------------------
        # 3. Bepaal doelbak
        # --------------------------------------------------
        target_bin = self.get_target_bin(detected_type)

        rospy.loginfo('Doelbak: %s', target_bin)

        # --------------------------------------------------
        # 4. Stuur robot action
        # --------------------------------------------------
        success = self.send_robot_goal(
            detection.pose,
            detected_type,
            target_bin
        )

        if not success:
            rospy.logerr('Robot actie mislukt')
            return False

        rospy.loginfo('--- CYCLUS VOLTOOID ---')
        return True

    # ==================================================
    # ROBOT ACTION
    # ==================================================

    def send_robot_goal(self, pose, kwast_type, target_bin):
        """
        Stuurt pick-and-place opdracht naar robot.
        """

        self.robot_busy = True

        goal = PickAndPlaceGoal()
        goal.target_pose.header.frame_id = 'world'
        goal.target_pose.pose = pose
        goal.kwast_type = kwast_type

        rospy.loginfo('Verstuur robot goal...')

        self.robot_client.send_goal(
            goal,
            feedback_cb=self.robot_feedback_callback
        )

        self.robot_client.wait_for_result()

        result = self.robot_client.get_result()

        self.robot_busy = False

        if result.success:
            rospy.loginfo('Robot actie succesvol')
            return True

        rospy.logerr('Robot actie gefaald')
        return False

    def robot_feedback_callback(self, feedback):
        """
        Ontvangt live feedback van robot action.
        """

        rospy.loginfo('Robot status: %s', feedback.status)

    # ==================================================
    # HULPFUNCTIES
    # ==================================================

    def wait_for_detection(self, timeout=5):
        """
        Wacht op nieuwe vision detectie.
        """

        start_time = rospy.Time.now().to_sec()

        while not rospy.is_shutdown():
            if self.current_detection is not None:
                detection = self.current_detection
                self.current_detection = None
                return detection

            current_time = rospy.Time.now().to_sec()

            if current_time - start_time > timeout:
                return None

            rospy.sleep(0.1)

    def get_target_bin(self, kwast_type):
        """
        Bepaalt naar welke bak de robot moet.
        """

        mapping = {
            'norm': 'BakRB',
            'dik': 'BakRO',
            'rub': 'BakLB',
            'pen': 'BakLO'
        }

        return mapping.get(kwast_type, 'home')


# ==================================================
# MAIN
# ==================================================

if __name__ == '__main__':
    try:
        Hoofdprogramma()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
