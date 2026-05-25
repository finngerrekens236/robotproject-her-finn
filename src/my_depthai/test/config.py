"""
Centrale configuratie — alle instelbare waarden staan hier.
Pas dit bestand aan voor jouw opstelling.
"""

import os
import cv2

# ── ArUco markers ─────────────────────────────────────────────────────────────

# Dictionary passend bij je geprinte markers
# Opties: cv2.aruco.DICT_4X4_50 | DICT_5X5_100 | DICT_6X6_250
ARUCO_DICT = cv2.aruco.DICT_4X4_50

# Marker IDs die je gebruikt (precies 3)
MARKER_IDS = [0, 1, 2]

# Robot-coördinaten (x, y) per marker ID in mm — inmeten met de robot
MARKER_ROBOT_COORDS = {
    0: (  0.0,   0.0),   # marker 0 — links voor
    1: (110.0,   0.0),   # marker 1 — rechts voor
    2: ( 40.0, 220.0),   # marker 2 — links achter
}

# Vaste Z-hoogte van het oppakpunt in het robot-assenstelsel (mm)
Z_CONVEYOR = 10.0

# ── Calibratie ────────────────────────────────────────────────────────────────

CALIBRATION_FILE = os.path.join(os.path.dirname(__file__), "calibration.json")

# ── YOLO model ────────────────────────────────────────────────────────────────

DEFAULT_MODEL_PATH = "../models/model.pt"
DEFAULT_CONF       = 0.5

DEFAULT_CLASSES = ["vork", "schroevendraaier", "lepel", "tandenborstel"]
DEFAULT_COLORS  = [
    (200, 200, 0),   # vork              — geel
    (0,   0, 220),   # schroevendraaier  — blauw
    (0, 200,   0),   # lepel             — groen
    (220, 0, 220),   # tandenborstel     — paars
]

# ── Lokalisatie ───────────────────────────────────────────────────────────────

# Standaard pick-percentage langs de as (0.0 = onderkant, 1.0 = bovenkant)
PICK_PERCENT = 0.35

# Per-object strategie: pas aan per klasse
STRATEGIEEN = {
    "vork": {
        "method": "canny", "onderkant": "smalste", "pick_percent": 0.50,
        "canny_low": 50, "canny_high": 150, "clahe": False, "denoise": False, "min_area": 500,
    },
    "lepel": {
        "method": "canny", "onderkant": "smalste", "pick_percent": 0.50,
        "canny_low": 30, "canny_high": 100, "clahe": True, "denoise": True, "min_area": 150,
    },
    "tandenborstel": {
        "method": "canny", "onderkant": "smalste", "pick_percent": 0.50,
        "canny_low": 50, "canny_high": 150, "clahe": False, "denoise": False, "min_area": 500,
    },
    "schroevendraaier": {
        "method": "value_otsu", "onderkant": "breedste", "pick_percent": 0.50, "min_area": 500,
    },
}
