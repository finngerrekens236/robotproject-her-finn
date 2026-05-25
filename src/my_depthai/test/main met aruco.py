"""
Volledige pipeline: YOLO detectie + lokalisatie + ArUco pixel→robot transformatie.

Gebruik:
    python "main met aruco.py" --model ../models/model.pt
    python "main met aruco.py" --model ../models/model.pt --image test_main_met_arucu_input/ma.jpeg
    python "main met aruco.py" --test-aruco --image test_main_met_arucu_input/ma.jpeg

--test-aruco: sla YOLO over, test alleen of de ArUco markers gevonden worden.
Output wordt opgeslagen in test_main_met_arucu_output/.
"""

import argparse
import os
import sys
import cv2

from config import DEFAULT_MODEL_PATH, DEFAULT_CONF, DEFAULT_CLASSES, DEFAULT_COLORS
from test_detection import load_model, detect, IMAGE_EXTS
from test_lokalisatie import lokaliseer, STRATEGIEEN, PICK_PERCENT
from aruco_transform import (
    pixel_naar_robot, pixel_naar_robot_gecalibreerd,
    teken_aruco_debug, detecteer_aruco, laad_calibratie, MARKER_IDS,
)

INPUT_DIR  = os.path.join(os.path.dirname(__file__), "test_main_met_arucu_input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_main_met_arucu_output")

# Controleer eenmalig bij opstarten of calibratie beschikbaar is
try:
    laad_calibratie()
    _GECALIBREERD = True
    print("[INFO] calibration.json gevonden — gecalibreerde modus actief (markers niet nodig).")
except FileNotFoundError:
    _GECALIBREERD = False
    print("[WAARSCHUWING] Geen calibration.json — live marker detectie actief.")
    print("               Voer 'python calibratie.py --image <foto>' uit voor kalibratie.")


def verwerk_afbeelding(image_path, model, test_aruco_only=False):
    filename = os.path.basename(image_path)
    print(f"\n[{filename}]")

    frame = cv2.imread(image_path)
    if frame is None:
        print("  [OVERGESLAGEN] Kan niet openen")
        return None

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── ArUco markers (alleen bij live modus) ────────────────────────────────
    if _GECALIBREERD:
        markers_px = {}
        ontbrekend = []
        aruco_vis  = frame.copy()
        cv2.putText(aruco_vis, "gecalibreerde modus — markers niet nodig", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)
    else:
        markers_px = detecteer_aruco(frame)
        ontbrekend = [mid for mid in MARKER_IDS if mid not in markers_px]
        aruco_vis  = teken_aruco_debug(frame, markers_px)

        if ontbrekend:
            print(f"  [WAARSCHUWING] Markers niet gevonden: {ontbrekend}")
            print(f"  Gevonden: {list(markers_px.keys())}")
        else:
            print(f"  Markers gevonden: {list(markers_px.keys())}")
            for mid, (cx, cy) in markers_px.items():
                print(f"    ID {mid}: pixel ({int(cx)}, {int(cy)})")

    aruco_out = os.path.join(OUTPUT_DIR, f"aruco_{filename}")
    cv2.imwrite(aruco_out, aruco_vis)
    print(f"  -> {aruco_out}")

    if test_aruco_only:
        return None

    # ── YOLO detectie ────────────────────────────────────────────────────────
    if model is None:
        print("  Geen model geladen — gebruik --test-aruco voor aruco-only test")
        return None

    detections = detect(frame, model)
    if len(detections) == 0:
        print("  Geen objecten gevonden door YOLO")
        return None

    best_row = detections.loc[detections["confidence"].idxmax()]
    cls_id   = int(best_row["class"])
    label    = DEFAULT_CLASSES[cls_id] if cls_id < len(DEFAULT_CLASSES) else best_row["name"]
    conf     = float(best_row["confidence"])

    x1 = max(0, int(best_row.xmin))
    y1 = max(0, int(best_row.ymin))
    x2 = min(frame.shape[1], int(best_row.xmax))
    y2 = min(frame.shape[0], int(best_row.ymax))

    # ── Lokalisatie ──────────────────────────────────────────────────────────
    crop = frame[y1:y2, x1:x2].copy()
    cx, cy, angle, pick_x_crop, pick_y_crop, annotated = lokaliseer(crop, label)

    # Oppakpunt terug naar origineel frame
    pick_px = x1 + pick_x_crop
    pick_py = y1 + pick_y_crop

    # ── Pixel → robot coördinaten ────────────────────────────────────────────
    robot_result = None
    if _GECALIBREERD:
        rx, ry, rz_height, rz_deg = pixel_naar_robot_gecalibreerd(pick_px, pick_py, angle)
        robot_result = (rx, ry, rz_height, rz_deg)
    elif not ontbrekend:
        try:
            rx, ry, rz_height, rz_deg = pixel_naar_robot(pick_px, pick_py, angle, frame)
            robot_result = (rx, ry, rz_height, rz_deg)
        except ValueError as e:
            print(f"  [FOUT] ArUco transformatie mislukt: {e}")
    else:
        print("  [OVERGESLAGEN] Robot-coördinaten niet berekend — markers ontbreken")

    # ── Output opslaan ───────────────────────────────────────────────────────
    # Teken oppakpunt op het volledige frame
    full_vis = aruco_vis.copy()
    cv2.rectangle(full_vis, (x1, y1), (x2, y2), (0, 200, 0), 2)
    cv2.circle(full_vis, (pick_px, pick_py), 8, (0, 200, 0), -1)
    if robot_result:
        rx, ry, rz_height, rz_deg = robot_result
        cv2.putText(full_vis,
                    f"robot: ({rx:.1f}, {ry:.1f}) rz={rz_deg:.1f}deg",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)

    full_out = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(full_out, full_vis)

    crop_out = os.path.join(OUTPUT_DIR, f"crop_{filename}")
    cv2.imwrite(crop_out, annotated)

    # ── Terminal output ───────────────────────────────────────────────────────
    strat = STRATEGIEEN.get(label, {})
    pct   = strat.get("pick_percent", PICK_PERCENT)
    regel = strat.get("onderkant", "smalste")
    print(f"  object   : {label}  (conf={conf:.2f})")
    print(f"  strategie: onderkant={regel}  pick={int(pct*100)}%")
    print(f"  hoek     : {angle:.1f}°")
    print(f"  oppak px : ({pick_px},{pick_py})  (origineel frame)")
    if robot_result:
        rx, ry, rz_height, rz_deg = robot_result
        print(f"  robot X  : {rx:.2f} mm")
        print(f"  robot Y  : {ry:.2f} mm")
        print(f"  robot Z  : {rz_height:.2f} mm")
        print(f"  robot Rz : {rz_deg:.2f}°")
    print(f"  -> {full_out}")
    print(f"  -> {crop_out}")

    return robot_result


def main():
    parser = argparse.ArgumentParser(description="main met ArUco — detectie + lokalisatie + robot-coördinaten")
    parser.add_argument("--model",      default=DEFAULT_MODEL_PATH)
    parser.add_argument("--conf",       type=float, default=DEFAULT_CONF)
    parser.add_argument("--image",      default=None)
    parser.add_argument("--test-aruco", action="store_true",
                        help="Test alleen ArUco-detectie, sla YOLO over")
    args = parser.parse_args()

    model = None
    if not args.test_aruco:
        print(f"[INFO] Model laden: {args.model}")
        try:
            model = load_model(args.model, args.conf)
            print("[INFO] Model geladen.")
        except Exception as e:
            print(f"[FOUT] Kan model niet laden: {e}")
            sys.exit(1)

    if args.image:
        image_paths = [args.image]
    else:
        image_paths = []
        for root, _, files in os.walk(INPUT_DIR):
            for f in sorted(files):
                if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
                    image_paths.append(os.path.join(root, f))
        if not image_paths:
            print(f"[FOUT] Geen afbeeldingen in {INPUT_DIR}")
            sys.exit(1)
        print(f"[INFO] {len(image_paths)} afbeelding(en)\n")

    for path in image_paths:
        verwerk_afbeelding(path, model, test_aruco_only=args.test_aruco)

    print(f"\n[INFO] Output opgeslagen in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
