#!/usr/bin/env python

class RobotController(object):
    def __init__(self):
        print("[DUMMY] RobotController aangemaakt (geen MoveIt nodig)")

    def move_to_named_target(self, target_name):
        print("[DUMMY] Beweeg naar: {}".format(target_name))
        return True

    def gripper_on(self):
        print("[DUMMY] Gripper AAN")

    def gripper_off(self):
        print("[DUMMY] Gripper UIT")

    def pick(self, pose):
        print("[DUMMY] Pick uitgeprobeerd op positie: x={}, y={}, z={}".format(
            pose.position.x, pose.position.y, pose.position.z))
        return True
