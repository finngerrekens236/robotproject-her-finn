"""
Standalone volledige pipeline test voor Windows — GEEN ROS of camera vereist.

Draait exact dezelfde stappen als de ROS vision node:
  1. YOLOv5 detectie
  2. Oppaklocalisatie via lokalisatie.py (per-class strategie)
  3. Pixel -> robot coördinaten via calibration.json

Gebruik:
    python test_full_pipeline.py --model ../models/model.pt --image foto.jpg
    python test_full_pipeline.py --model ../models/model.pt
"""

import argparse
import os
import sys

import cv2
import numpy as np
import torch

# Zorg dat scripts/ importeerbaar is (zelfde als vision_node.py)
_scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from lokalisatie import lokaliseer
from aruco_transform import pixel_naar_robot_gecalibreerd

from config import DEFAULT_CLASSES, DEFAULT_CONF, DEFAULT_MODEL_PATH

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
INPUT_DIR  = os.path.join(os.path.dirname(__file__), "test_detection_input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_detection_output")


def laad_model(model_path, conf):
    import pathlib
    pathlib.PosixPath = pathlib.WindowsPath
    model = torch.hub.load("ultralytics/yolov5", "custom",
                           path=model_path, force_reload=False, verbose=False)
    model.conf = conf
    model.eval()
    return model


def detecteer(frame, model):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(rgb)
    return results.pandas().xyxy[0]


def sla_debug_op(output_map, stem, label, stap_nr, naam, img):
    bestandsnaam = f"{stem}_stap{stap_nr}_{label}_{naam}.jpg"
    cv2.imwrite(os.path.join(output_map, bestandsnaam), img)


def verwerk_afbeelding(frame, model, classes, output_map, stem):
    detections = detecteer(frame, model)

    if len(detections) == 0:
        print("  Geen object gevonden.")
        cv2.imwrite(os.path.join(output_map, f"{stem}_stap1_volledig_frame.jpg"), frame)
        return

    best = detections.loc[detections["confidence"].idxmax()]
    cls_id = int(best["class"])
    label  = classes[cls_id] if cls_id < len(classes) else best["name"]
    x1, y1, x2, y2 = int(best.xmin), int(best.ymin), int(best.xmax), int(best.ymax)

    # Stap 1: volledig frame
    cv2.imwrite(os.path.join(output_map, f"{stem}_stap1_volledig_frame.jpg"), frame)

    # Stap 2: bounding box
    bbox_frame = frame.copy()
    cv2.rectangle(bbox_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(bbox_frame, f"{label} {best['confidence']:.2f}",
                (x1, max(y1 - 8, 12)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imwrite(os.path.join(output_map, f"{stem}_stap2_bounding_box.jpg"), bbox_frame)

    # Stap 3+: lokalisatie tussenstappen
    crop = frame[y1:y2, x1:x2]
    _, _, angle_deg, pick_x_crop, pick_y_crop, _, debug_stappen = lokaliseer(crop, label)

    for i, (naam, img) in enumerate(debug_stappen, start=3):
        sla_debug_op(output_map, stem, label, i, naam, img)

    # Pixel -> robot coördinaten
    cx = x1 + pick_x_crop
    cy = y1 + pick_y_crop

    try:
        rx, ry, rz, rz_deg = pixel_naar_robot_gecalibreerd(cx, cy, angle_deg)
        print(f"  [{label}] conf={best['confidence']:.2f}  oppak=({cx},{cy})px  hoek={angle_deg:.1f}°")
        print(f"           robot: x={rx:.1f}mm  y={ry:.1f}mm  z={rz:.1f}mm  rz={rz_deg:.1f}°")
    except FileNotFoundError as e:
        print(f"  [{label}] conf={best['confidence']:.2f}  oppak=({cx},{cy})px  hoek={angle_deg:.1f}°")
        print(f"  [WAARSCHUWING] Geen calibration.json — alleen pixelcoördinaten beschikbaar.")
        print(f"  ({e})")

    print(f"  Debug images -> {output_map}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Volledige vision pipeline test (geen ROS)")
    parser.add_argument("--model",   default=DEFAULT_MODEL_PATH, help="Pad naar .pt model")
    parser.add_argument("--conf",    type=float, default=DEFAULT_CONF, help="Confidence threshold")
    parser.add_argument("--image",   default=None, help="Verwerk één specifieke afbeelding")
    parser.add_argument("--classes", nargs="+", default=DEFAULT_CLASSES)
    args = parser.parse_args()

    print(f"[INFO] Model laden: {args.model}")
    try:
        model = laad_model(args.model, args.conf)
        print("[INFO] Model geladen.\n")
    except Exception as e:
        print(f"[FOUT] Kan model niet laden: {e}")
        sys.exit(1)

    input_files = (
        [args.image] if args.image
        else [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR)
              if os.path.splitext(f)[1].lower() in IMAGE_EXTS]
    )

    if not input_files:
        print(f"[FOUT] Geen afbeeldingen gevonden in {INPUT_DIR}")
        sys.exit(1)

    print(f"[INFO] {len(input_files)} afbeelding(en) te verwerken\n")

    for input_path in input_files:
        filename = os.path.basename(input_path)
        stem = os.path.splitext(filename)[0]

        frame = cv2.imread(input_path)
        if frame is None:
            print(f"  [OVERGESLAGEN] Kan niet openen: {filename}")
            continue

        output_map = os.path.join(OUTPUT_DIR, stem)
        os.makedirs(output_map, exist_ok=True)

        print(f"{filename}:")
        verwerk_afbeelding(frame, model, args.classes, output_map, stem)
        print()

    print(f"[INFO] Klaar. Resultaten in {OUTPUT_DIR}/")
