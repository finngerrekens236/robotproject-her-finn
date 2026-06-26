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
    0: (-188.7, -277.5),
    1: (-19.9, -326.3),
    2: ( -7.3,  -197.8),
}

# Vaste Z-hoogte van het oppakpunt in het robot-assenstelsel (mm)
Z_CONVEYOR = 10.0

# Pad naar het kalibratiebestand (relatief aan package root)
_pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALIBRATION_FILE = os.path.join(_pkg_dir, "config", "calibration.json")
