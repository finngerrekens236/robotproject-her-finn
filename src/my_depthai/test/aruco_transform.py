"""
Transformeert pixel-oppakcoördinaten naar robot-coördinaten via 3 ArUco markers.

Twee modi:
  1. Live marker detectie (pixel_naar_robot) — vereist markers in elk frame
  2. Gecalibreerd (pixel_naar_robot_gecalibreerd) — laadt eenmalig opgeslagen matrix
     uit calibration.json, markers niet meer nodig

Gebruik gecalibreerde modus na uitvoeren van calibratie.py:
    from aruco_transform import pixel_naar_robot_gecalibreerd

    x, y, z, rz = pixel_naar_robot_gecalibreerd(pick_px, pick_py, angle_deg)
"""

import json
import math
import os
import cv2
import numpy as np

from config import (
    ARUCO_DICT, MARKER_IDS, MARKER_ROBOT_COORDS, Z_CONVEYOR, CALIBRATION_FILE,
)


def detecteer_aruco(frame):
    """
    Detecteert ArUco markers in frame.
    Geeft dict {marker_id: (cx_px, cy_px)} terug voor alle gevonden markers.
    """
    aruco_dict   = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    aruco_params = cv2.aruco.DetectorParameters()
    aruco_params.detectInvertedMarker = True
    detector     = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    corners, ids, _ = detector.detectMarkers(frame)

    result = {}
    if ids is None:
        return result

    for corner, mid in zip(corners, ids.flatten()):
        c  = corner[0]
        cx = float(c[:, 0].mean())
        cy = float(c[:, 1].mean())
        result[int(mid)] = (cx, cy)

    return result


def _bereken_affiene_matrix(markers_px):
    """
    Berekent affiene transformatiematrix (pixel → robot XY) op basis van
    de 3 geconfigureerde markers.
    Geeft (M, rotation_offset_deg) terug.
    """
    src_pts = np.float32([
        markers_px[mid] for mid in MARKER_IDS
    ])
    dst_pts = np.float32([
        MARKER_ROBOT_COORDS[mid] for mid in MARKER_IDS
    ])

    M = cv2.getAffineTransform(src_pts, dst_pts)  # 2×3 matrix

    # Rotatieoffset van camera-frame t.o.v. robot-frame
    rotation_offset_deg = math.degrees(math.atan2(float(M[1, 0]), float(M[0, 0])))

    return M, rotation_offset_deg


def pixel_naar_robot(pick_px, pick_py, angle_deg, frame):
    """
    Transformeert pixel-oppakcoördinaten naar robot-coördinaten.

    Parameters:
        pick_px, pick_py : oppakpunt in pixels (crop-onafhankelijk, origineel frame)
        angle_deg        : rotatiehoek uit lokaliseer (graden, camera-frame)
        frame            : het volledige BGR cameraframe (voor marker detectie)

    Geeft (x, y, z, rz_deg) terug in het robot-assenstelsel.
    Gooit ValueError als niet alle 3 markers zichtbaar zijn.
    """
    markers_px = detecteer_aruco(frame)

    ontbrekend = [mid for mid in MARKER_IDS if mid not in markers_px]
    if ontbrekend:
        raise ValueError(f"Markers niet gevonden: {ontbrekend}. "
                         f"Gevonden: {list(markers_px.keys())}")

    M, rotation_offset_deg = _bereken_affiene_matrix(markers_px)

    # Oppakpunt transformeren
    pt      = np.array([pick_px, pick_py, 1.0], dtype=np.float64)
    robot   = M @ pt
    robot_x = float(robot[0])
    robot_y = float(robot[1])

    # Hoek corrigeren voor camerarotatie t.o.v. robot
    rz_deg = angle_deg + rotation_offset_deg

    return robot_x, robot_y, float(Z_CONVEYOR), rz_deg


_calibratie_cache = None


def laad_calibratie():
    """
    Laadt calibration.json en geeft (M, rotation_offset_deg, z_conveyor) terug.
    Resultaat wordt gecached zodat het bestand maar één keer gelezen wordt.
    Gooit FileNotFoundError als calibration.json niet bestaat.
    """
    global _calibratie_cache
    if _calibratie_cache is not None:
        return _calibratie_cache

    if not os.path.exists(CALIBRATION_FILE):
        raise FileNotFoundError(
            f"Geen calibratie gevonden: {CALIBRATION_FILE}\n"
            "Voer eerst 'python calibratie.py --image <foto_met_markers.jpg>' uit."
        )

    with open(CALIBRATION_FILE) as f:
        data = json.load(f)

    M = np.array(data["affine_matrix"], dtype=np.float64)
    rotation_offset_deg = float(data["rotation_offset_deg"])
    z_conveyor = float(data["z_conveyor"])

    _calibratie_cache = (M, rotation_offset_deg, z_conveyor)
    return _calibratie_cache


def pixel_naar_robot_gecalibreerd(pick_px, pick_py, angle_deg):
    """
    Transformeert pixel-oppakcoördinaten naar robot-coördinaten via opgeslagen calibratie.
    Markers hoeven NIET meer zichtbaar te zijn in het frame.

    Parameters:
        pick_px, pick_py : oppakpunt in pixels (origineel frame)
        angle_deg        : rotatiehoek uit lokaliseer (graden, camera-frame)

    Geeft (x, y, z, rz_deg) terug in het robot-assenstelsel.
    Gooit FileNotFoundError als calibration.json niet bestaat.
    """
    M, rotation_offset_deg, z_conveyor = laad_calibratie()

    pt    = np.array([pick_px, pick_py, 1.0], dtype=np.float64)
    robot = M @ pt

    rz_deg = angle_deg + rotation_offset_deg
    return float(robot[0]), float(robot[1]), z_conveyor, rz_deg


def teken_aruco_debug(frame, markers_px=None):
    """
    Tekent gevonden markers en hun ID op een kopie van frame.
    Handig voor debuggen — geeft het geannoteerde frame terug.
    """
    if markers_px is None:
        markers_px = detecteer_aruco(frame)

    vis = frame.copy()
    for mid, (cx, cy) in markers_px.items():
        cv2.circle(vis, (int(cx), int(cy)), 8, (0, 165, 255), -1)
        cv2.putText(vis, f"ID {mid}  ({int(cx)},{int(cy)})",
                    (int(cx) + 10, int(cy) - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

    ontbrekend = [mid for mid in MARKER_IDS if mid not in markers_px]
    if ontbrekend:
        cv2.putText(vis, f"ONTBREEKT: {ontbrekend}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        cv2.putText(vis, "Alle markers gevonden", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)

    return vis
