"""
Eenmalige camera-robot calibratie via ArUco markers.

Werkwijze:
  1. Houd alle ArUco markers in beeld (of geef een foto mee)
  2. Dit script detecteert automatisch de pixel-coördinaten
  3. Robot-coördinaten worden uit calibratie_config.py geladen (of interactief ingevoerd)
  4. De affiene transformatiematrix wordt berekend en opgeslagen in config/calibration.json
  5. Daarna kunnen de markers verwijderd worden

Gebruik:
    python calibratie.py                          # live OAK-D camera, SPACE om te calibreren
    python calibratie.py --image foto.jpg         # statische afbeelding
    python calibratie.py --interactief            # robot-coördinaten handmatig invoeren
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime

import cv2
import depthai as dai
import numpy as np

from calibratie_config import MARKER_IDS, MARKER_ROBOT_COORDS, Z_CONVEYOR, CALIBRATION_FILE
from aruco_transform import detecteer_aruco, teken_aruco_debug

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "debug")


def _bereken_en_sla_op(markers_px, robot_coords, z_conveyor):
    src_pts = np.float32([markers_px[mid] for mid in MARKER_IDS])
    dst_pts = np.float32([robot_coords[mid] for mid in MARKER_IDS])

    M = cv2.getAffineTransform(src_pts, dst_pts)
    rotation_offset_deg = math.degrees(math.atan2(float(M[1, 0]), float(M[0, 0])))

    data = {
        "affine_matrix": M.tolist(),
        "rotation_offset_deg": rotation_offset_deg,
        "z_conveyor": z_conveyor,
        "created_at": datetime.now().isoformat(),
        "markers": {
            str(mid): {
                "pixel": list(markers_px[mid]),
                "robot": list(robot_coords[mid]),
            }
            for mid in MARKER_IDS
        },
    }

    os.makedirs(os.path.dirname(CALIBRATION_FILE), exist_ok=True)
    with open(CALIBRATION_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return M, rotation_offset_deg, data


def _capture_from_camera():
    pipeline = dai.Pipeline()
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setPreviewSize(640, 480)
    camRgb.setInterleaved(False)
    camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("rgb")
    camRgb.preview.link(xout.input)

    print("[INFO] Camera gestart. Zorg dat alle markers zichtbaar zijn.")
    print("       Druk SPACE om te calibreren, Q om te stoppen.")

    with dai.Device(pipeline) as device:
        q = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        while True:
            frame = q.get().getCvFrame()
            preview = teken_aruco_debug(frame.copy())
            cv2.imshow("Calibratie — SPACE om op te nemen", preview)
            key = cv2.waitKey(1)
            if key == ord(' '):
                cv2.destroyAllWindows()
                return frame
            if key == ord('q'):
                cv2.destroyAllWindows()
                sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Camera-robot calibratie via ArUco markers")
    parser.add_argument("--image", default=None,
                        help="Afbeelding met alle ArUco markers (weggelaten = live camera)")
    parser.add_argument("--interactief", action="store_true",
                        help="Robot-coördinaten interactief invoeren i.p.v. uit configuratie")
    args = parser.parse_args()

    if args.image:
        frame = cv2.imread(args.image)
        if frame is None:
            print(f"[FOUT] Kan afbeelding niet openen: {args.image}")
            sys.exit(1)
        print(f"\n[INFO] Afbeelding geladen: {args.image}  ({frame.shape[1]}x{frame.shape[0]})")
    else:
        frame = _capture_from_camera()
        print(f"\n[INFO] Frame opgenomen van camera  ({frame.shape[1]}x{frame.shape[0]})")

    markers_px = detecteer_aruco(frame)
    ontbrekend = [mid for mid in MARKER_IDS if mid not in markers_px]

    print("\n[DETECTIE] Gevonden markers:")
    for mid in MARKER_IDS:
        if mid in markers_px:
            cx, cy = markers_px[mid]
            print(f"  ID {mid}: pixel ({cx:.1f}, {cy:.1f})")
        else:
            print(f"  ID {mid}: NIET GEVONDEN")

    if ontbrekend:
        print(f"\n[FOUT] Niet alle markers gevonden. Ontbreekt: {ontbrekend}")
        sys.exit(1)

    robot_coords = {}
    if args.interactief:
        print("\n[INPUT] Voer robot-coördinaten in voor elke marker (in mm):")
        for mid in MARKER_IDS:
            cx, cy = markers_px[mid]
            default = MARKER_ROBOT_COORDS.get(mid)
            print(f"\n  Marker ID {mid} — pixel ({cx:.1f}, {cy:.1f})")
            inp_x = input(f"    Robot X mm [{default[0] if default else ''}]: ").strip()
            inp_y = input(f"    Robot Y mm [{default[1] if default else ''}]: ").strip()
            rx = float(inp_x) if inp_x else default[0]
            ry = float(inp_y) if inp_y else default[1]
            robot_coords[mid] = (rx, ry)
    else:
        print("\n[INFO] Robot-coördinaten uit calibratie_config.py:")
        for mid in MARKER_IDS:
            rx, ry = MARKER_ROBOT_COORDS[mid]
            robot_coords[mid] = (rx, ry)
            print(f"  ID {mid}: robot ({rx:.1f}, {ry:.1f}) mm")

    M, rotation_offset_deg, _ = _bereken_en_sla_op(markers_px, robot_coords, Z_CONVEYOR)

    print(f"\n[CALIBRATIE] Affiene matrix berekend:")
    print(f"  [[{M[0,0]:.6f}, {M[0,1]:.6f}, {M[0,2]:.4f}]")
    print(f"   [{M[1,0]:.6f}, {M[1,1]:.6f}, {M[1,2]:.4f}]]")
    print(f"  Rotatieoffset: {rotation_offset_deg:.2f}°")
    print(f"\n[OK] Opgeslagen: {CALIBRATION_FILE}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    vis = teken_aruco_debug(frame, markers_px)
    for mid in MARKER_IDS:
        cx, cy = markers_px[mid]
        rx, ry = robot_coords[mid]
        cv2.putText(vis, f"robot ({rx:.0f},{ry:.0f})mm",
                    (int(cx) + 10, int(cy) + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 200, 0), 2)

    out_path = os.path.join(OUTPUT_DIR, "calibratie_verificatie.jpg")
    cv2.imwrite(out_path, vis)
    print(f"[INFO] Verificatieafbeelding: {out_path}")
    print("\n[KLAAR] Markers kunnen nu verwijderd worden.")


if __name__ == "__main__":
    main()
