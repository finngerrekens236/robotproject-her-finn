"""
Kalibratie-instellingen — pas aan voor jouw opstelling.
"""

import os
import cv2

# Dictionary passend bij je geprinte markers
ARUCO_DICT = cv2.aruco.DICT_4X4_50

# Marker IDs die je gebruikt (precies 3)
MARKER_IDS = [0, 1, 2]

# Robot-coördinaten (x, y) per marker ID in mm — inmeten met de robot
MARKER_ROBOT_COORDS = {
    0: (-163.8, -280.5),
    1: (-164, -96),
    2: ( -44,  -90),
}

# Vaste Z-hoogte van het oppakpunt in het robot-assenstelsel (mm)
Z_CONVEYOR = 10.0

# Pad naar het kalibratiebestand (relatief aan package root)
_pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALIBRATION_FILE = os.path.join(_pkg_dir, "config", "calibration.json")
