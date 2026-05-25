"""
Gebruik:
    python test_main.py --model ../models/dataset.pt
    python test_main.py --model ../models/dataset.pt --image pad/naar/foto.jpg
    python test_main.py --model ../models/dataset.pt --conf 0.2

Zonder --image: pakt de eerste afbeelding uit test_main_input/.
Output (lokalisatie afbeelding) wordt opgeslagen in test_main_output/.
"""

import argparse
import os
import sys
import cv2

from test_detection import (
    load_model, detect, get_pose_in_bbox,
    DEFAULT_CLASSES, DEFAULT_COLORS, IMAGE_EXTS,
)
from test_lokalisatie import lokaliseer, STRATEGIEEN, PICK_PERCENT

INPUT_DIR  = os.path.join(os.path.dirname(__file__), "test_main_input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_main_output")


def main():
    parser = argparse.ArgumentParser(description="test_main — detectie + lokalisatie")
    parser.add_argument("--model", default="../models/dataset.pt", help="Pad naar .pt model")
    parser.add_argument("--conf",  type=float, default=0.5,        help="Confidence threshold")
    parser.add_argument("--image", default=None,                   help="Pad naar invoer afbeelding")
    args = parser.parse_args()

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
            print(f"[FOUT] Geen afbeeldingen gevonden in {INPUT_DIR}")
            sys.exit(1)
        print(f"[INFO] {len(image_paths)} afbeelding(en) gevonden\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []

    for image_path in image_paths:
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"[OVERGESLAGEN] Kan niet openen: {image_path}")
            continue

        detections = detect(frame, model)
        total = len(detections)

        if total == 0:
            print(f"[{os.path.basename(image_path)}]  geen objecten gevonden")
            continue

        best_row = detections.loc[detections["confidence"].idxmax()]
        cls_id   = int(best_row["class"])
        label    = DEFAULT_CLASSES[cls_id] if cls_id < len(DEFAULT_CLASSES) else best_row["name"]
        conf     = float(best_row["confidence"])

        x1 = max(0, int(best_row.xmin))
        y1 = max(0, int(best_row.ymin))
        x2 = min(frame.shape[1], int(best_row.xmax))
        y2 = min(frame.shape[0], int(best_row.ymax))

        crop = frame[y1:y2, x1:x2].copy()
        cx, cy, angle, pick_x, pick_y, annotated = lokaliseer(crop, label)

        output_path = os.path.join(OUTPUT_DIR, os.path.basename(image_path))
        cv2.imwrite(output_path, annotated)

        strat  = STRATEGIEEN.get(label, {})
        pct    = strat.get("pick_percent", PICK_PERCENT)
        regel  = strat.get("onderkant", "smalste")
        print(f"[{os.path.basename(image_path)}]")
        print(f"  object   : {label}  (conf={conf:.2f})")
        print(f"  strategie: onderkant={regel}  pick={int(pct*100)}%")
        print(f"  hoek     : {angle:.1f}°")
        print(f"  oppak    : ({pick_x},{pick_y})px")
        print(f"  -> {output_path}")

        results.append({
            "label": label, "confidence": conf,
            "total_detections": total,
            "angle": angle, "pick_x": pick_x, "pick_y": pick_y,
            "frame": annotated, "image_path": output_path,
        })

    return results


if __name__ == "__main__":
    main()
