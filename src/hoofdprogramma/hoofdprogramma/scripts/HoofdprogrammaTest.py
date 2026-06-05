#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String, Bool

class SimpelHoofdprogramma(object):
    def __init__(self):
        rospy.init_node('hoofdprogramma_node')

        # Interne status van ons hoofdprogramma
        self.system_running = False
        self.sensor_triggered = False

        # --------------------------------------------------
        # COUPLING MET HMI EN CONVEYOR NODE
        # --------------------------------------------------
        # Luisteren naar de HMI (Start / Stop knoppen)
        rospy.Subscriber('hmi_commands', String, self.hmi_callback)

        # Publisher naar de conveyor node (Let op de topicnaam en kleine letters!)
        self.conveyor_pub = rospy.Publisher('/conveyor/control', String, queue_size=10)

        # Subscriber voor de sensor (Luistert naar de Bool van de conveyor node)
        rospy.Subscriber('/conveyor/product_ready', Bool, self.sensor_callback)

        rospy.loginfo('=== Hoofdprogramma (Stap 1) ONLINE en stand-by ===')

    def hmi_callback(self, msg):
        """Verwerkt de knoppen van de HMI."""
        command = msg.data.strip()
        rospy.loginfo('HMI Knop ontvangen: "%s"', command)

        # GECORRIGEERD: We luisteren nu naar de exacte string die jouw HMI stuurt!
        if command == "single_start" or command == "Start" or command == "start cyclus":
            if not self.system_running:
                rospy.loginfo('Systeem geactiveerd via single_start! Transportband krijgt startsein...')
                self.system_running = True
                self.sensor_triggered = False
                
                # Stuur "start" in kleine letters naar jouw conveyor node
                self.conveyor_pub.publish("start")
            else:
                rospy.logwarn('Systeem draait al.')

        elif command == "Stop":
            rospy.logwarn('Noodstop ingedrukt! Band stoppen.')
            self.stop_systeem()

    def sensor_callback(self, msg):
        """Wordt aangeroepen zodra de conveyor node 'True' stuurt."""
        # Alleen reageren als ons hoofdprogramma ook daadwerkelijk actief is!
        if self.system_running and msg.data == True:
            rospy.loginfo('SENSORSIGNALONTVANGEN: Product heeft het einde bereikt!')
            
            # Schakel de band meteen uit via het hoofdprogramma
            self.stop_systeem()
            
            # Hier komt in de volgende stap je camera-trigger!

    def stop_systeem(self):
        """Zet de interne status op False en stopt de band."""
        self.system_running = False
        self.conveyor_pub.publish("stop")
        rospy.loginfo('Transportband stilgelegd.')

if __name__ == '__main__':
    try:
        programma = SimpelHoofdprogramma()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass