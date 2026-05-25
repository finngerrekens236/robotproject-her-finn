"""
Standalone testscript voor Windows — GEEN ROS vereist.

Gebruik:
    python test_detection.py --model ../models/dataset.pt
    python test_detection.py --model ../models/dataset.pt --image foto.jpg
    python test_detection.py --model ../models/dataset.pt --conf 0.2
"""

import os
import sys
import cv2
import numpy as np
import torch

from config import DEFAULT_CLASSES, DEFAULT_COLORS, DEFAULT_CONF, DEFAULT_MODEL_PATH

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
INPUT_DIR  = os.path.join(os.path.dirname(__file__), "test_detection_input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_detection_output")


# ──────────────────────────────────────────────
# Publieke API (importeerbaar vanuit test_main)
# ──────────────────────────────────────────────

def load_model(model_path: str, conf: float = 0.5):
    import pathlib
    pathlib.PosixPath = pathlib.WindowsPath
    model = torch.hub.load("ultralytics/yolov5", "custom",
                           path=model_path, force_reload=False, verbose=False)
    model.conf = conf
    model.eval()
    return model


def detect(frame, model):
    """YOLOv5 inferentie op een BGR frame. Geeft pandas DataFrame terug."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(rgb)
    return results.pandas().xyxy[0]


def get_pose_in_bbox(frame, x1, y1, x2, y2):
    """Geeft (cx, cy, angle_deg) terug via contour analyse binnen de bounding box."""
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        return (x1 + x2) // 2, (y1 + y2) // 2, 0.0

    gray    = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges   = cv2.Canny(blurred, 50, 150)
    kernel  = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges   = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return (x1 + x2) // 2, (y1 + y2) // 2, 0.0

    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 100:
        return (x1 + x2) // 2, (y1 + y2) // 2, 0.0

    rect = cv2.minAreaRect(largest)
    (cx_crop, cy_crop), (w_rect, h_rect), angle = rect

    cx = int(x1 + cx_crop)
    cy = int(y1 + cy_crop)
    if w_rect < h_rect:
        angle += 90

    return cx, cy, angle


def draw_result(frame, det, classes=None, colors=None):
    """Tekent alle detecties op het frame."""
    if classes is None:
        classes = DEFAULT_CLASSES
    if colors is None:
        colors = DEFAULT_COLORS

    for _, row in det.iterrows():
        x1, y1, x2, y2 = int(row.xmin), int(row.ymin), int(row.xmax), int(row.ymax)
        cls_id = int(row["class"])
        label  = classes[cls_id] if cls_id < len(classes) else row["name"]
        color  = colors[cls_id % len(colors)]

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
        cv2.putText(frame, label, (x1 + 3, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return frame


# ──────────────────────────────────────────────
# Standalone script
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YOLOv5 detectie testscript (geen ROS)")
    parser.add_argument("--model",   default=DEFAULT_MODEL_PATH, help="Pad naar .pt model")
    parser.add_argument("--conf",    type=float, default=DEFAULT_CONF, help="Confidence threshold")
    parser.add_argument("--image",   default=None,                   help="Verwerk één specifieke afbeelding")
    parser.add_argument("--classes", nargs="+", default=DEFAULT_CLASSES)
    args = parser.parse_args()

    print(f"[INFO] Model laden: {args.model}")
    try:
        model = load_model(args.model, args.conf)
        print("[INFO] Model geladen.")
    except Exception as e:
        print(f"[FOUT] Kan model niet laden: {e}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

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
        stem, ext = os.path.splitext(filename)

        frame = cv2.imread(input_path)
        if frame is None:
            print(f"  [OVERGESLAGEN] Kan niet openen: {filename}")
            continue

        detections = detect(frame, model)
        annotated  = draw_result(frame.copy(), detections, args.classes)
        cv2.imwrite(os.path.join(OUTPUT_DIR, filename), annotated)

        label_counts = {}
        for _, row in detections.iterrows():
            cls_id = int(row["class"])
            label  = args.classes[cls_id] if cls_id < len(args.classes) else row["name"]
            label_counts[label] = label_counts.get(label, 0) + 1

            x1 = max(0, int(row.xmin))
            y1 = max(0, int(row.ymin))
            x2 = min(frame.shape[1], int(row.xmax))
            y2 = min(frame.shape[0], int(row.ymax))

            cx, cy, angle = get_pose_in_bbox(frame, x1, y1, x2, y2)
            print(f"  [{label}] conf={row['confidence']:.2f}  pos=({cx},{cy})px  angle={angle:.1f}°")

            crop_name = f"{stem}_{label}_{label_counts[label]}{ext}"
            cv2.imwrite(os.path.join(OUTPUT_DIR, crop_name), frame[y1:y2, x1:x2].copy())

        print(f"  {filename} -> {len(detections)} detectie(s): {list(label_counts.keys())}")

    print(f"\n[INFO] Resultaten opgeslagen in {OUTPUT_DIR}")
