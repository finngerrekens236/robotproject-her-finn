"""
Debug-versie van test_main.py.
Slaat per afbeelding alle tussenliggende stappen op in debug_output/<bestandsnaam>/.

Stappen die worden opgeslagen:
  01_origineel       — invoer afbeelding zoals die het YOLO-model ingaat
  02_yolo            — origineel met alle YOLO bounding boxes
  03_crop            — uitgesneden object (invoer voor lokaliseer)
  04_gray            — grijswaarden van de crop
  05_edges           — Canny-randen (na eventuele CLAHE)
  06_contours        — alle gevonden contours met hun oppervlaktes
  07_resultaat       — eindsresultaat van lokaliseer

Gebruik:
    python debug_main.py --model ../models/dataset.pt
    python debug_main.py --model ../models/dataset.pt --image test_main_input/h.JPG
"""

import argparse
import os
import sys
import cv2
import numpy as np

from test_detection import (
    load_model, detect, draw_result,
    DEFAULT_CLASSES, DEFAULT_COLORS, IMAGE_EXTS,
)
from test_lokalisatie import lokaliseer, STRATEGIEEN, PICK_PERCENT

INPUT_DIR  = os.path.join(os.path.dirname(__file__), "test_main_input")
DEBUG_DIR  = os.path.join(os.path.dirname(__file__), "debug_output")


def _save(folder, name, img):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    cv2.imwrite(path, img)
    print(f"    {name}")


def _preprocessing_steps(crop, label):
    """Herhaalt de preprocessing uit lokaliseer en geeft tussenbeelden terug."""
    strat       = STRATEGIEEN.get(label, {})
    method      = strat.get("method",     "canny")
    canny_low   = strat.get("canny_low",  50)
    canny_high  = strat.get("canny_high", 150)
    use_clahe   = strat.get("clahe",      False)
    use_denoise = strat.get("denoise",    False)
    min_area    = strat.get("min_area",   500)
    kernel      = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    if method == "value_otsu":
        v        = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)[:, :, 2]
        _, mask  = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        filtered = cv2.medianBlur(mask, 5)
        cnts, _  = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in cnts if cv2.contourArea(c) >= min_area]

        gray_img     = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)
        denoised_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)   # Otsu voor mediaan
        edges_img    = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)  # na mediaan filter
        suffix       = " (value_otsu)"
    else:
        gray   = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        def canny_pipeline(g):
            denoised = cv2.bilateralFilter(g, d=9, sigmaColor=75, sigmaSpace=75) if use_denoise else g
            blurred  = cv2.GaussianBlur(denoised, (5, 5), 0)
            edges    = cv2.Canny(blurred, canny_low, canny_high)
            edges    = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
            cnts, _  = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            return denoised, edges, [c for c in cnts if cv2.contourArea(c) >= min_area]

        denoised_gray, edges, contours = canny_pipeline(gray)
        clahe_used = False
        if not contours and use_clahe:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray  = clahe.apply(gray)
            denoised_gray, edges, contours = canny_pipeline(gray)
            clahe_used = True

        suffix       = " (CLAHE)" if clahe_used else ""
        gray_img     = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        denoised_img = cv2.cvtColor(denoised_gray, cv2.COLOR_GRAY2BGR) if use_denoise else None
        edges_img    = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    contours_img = crop.copy()
    for c in contours:
        area = cv2.contourArea(c)
        cv2.drawContours(contours_img, [c], -1, (0, 255, 0), 2)
        x, y, _, _ = cv2.boundingRect(c)
        cv2.putText(contours_img, f"{int(area)}px", (x, max(y - 4, 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)

    return gray_img, denoised_img, edges_img, contours_img, suffix


def debug_image(image_path, model):
    filename = os.path.basename(image_path)
    stem     = os.path.splitext(filename)[0]
    folder   = os.path.join(DEBUG_DIR, stem)

    print(f"\n[{filename}]")

    frame = cv2.imread(image_path)
    if frame is None:
        print("  [OVERGESLAGEN] Kan niet openen")
        return

    # 01 — origineel
    _save(folder, "01_origineel.jpg", frame)

    # YOLO detectie
    detections = detect(frame, model)

    # 02 — YOLO output (alle boxes)
    yolo_vis = draw_result(frame.copy(), detections, DEFAULT_CLASSES, DEFAULT_COLORS)
    _save(folder, "02_yolo.jpg", yolo_vis)

    if len(detections) == 0:
        print("  Geen objecten gevonden — stopt hier.")
        return

    best_row = detections.loc[detections["confidence"].idxmax()]
    cls_id   = int(best_row["class"])
    label    = DEFAULT_CLASSES[cls_id] if cls_id < len(DEFAULT_CLASSES) else best_row["name"]
    conf     = float(best_row["confidence"])

    x1 = max(0, int(best_row.xmin))
    y1 = max(0, int(best_row.ymin))
    x2 = min(frame.shape[1], int(best_row.xmax))
    y2 = min(frame.shape[0], int(best_row.ymax))

    # 03 — crop
    crop = frame[y1:y2, x1:x2].copy()
    _save(folder, "03_crop.jpg", crop)

    # 04, 05, 06 — preprocessing stappen
    gray_img, denoised_img, edges_img, contours_img, suffix = _preprocessing_steps(crop, label)
    _save(folder, f"04_gray{suffix}.jpg", gray_img)
    if denoised_img is not None:
        _save(folder, f"04b_denoised{suffix}.jpg", denoised_img)
    _save(folder, f"05_edges{suffix}.jpg", edges_img)
    _save(folder, f"06_contours{suffix}.jpg", contours_img)

    # 07 — eindresultaat lokaliseer
    cx, cy, angle, pick_x, pick_y, annotated = lokaliseer(crop, label)
    _save(folder, "07_resultaat.jpg", annotated)

    strat = STRATEGIEEN.get(label, {})
    pct   = strat.get("pick_percent", PICK_PERCENT)
    regel = strat.get("onderkant", "smalste")
    print(f"  object   : {label}  (conf={conf:.2f})")
    print(f"  strategie: onderkant={regel}  pick={int(pct*100)}%")
    print(f"  hoek     : {angle:.1f}°")
    print(f"  oppak    : ({x1 + pick_x},{y1 + pick_y})px  (originele afbeelding)")


def main():
    parser = argparse.ArgumentParser(description="Debug-versie van test_main")
    parser.add_argument("--model", default="../models/dataset.pt")
    parser.add_argument("--conf",  type=float, default=0.5)
    parser.add_argument("--image", default=None)
    args = parser.parse_args()

    print(f"[INFO] Model laden: {args.model}")
    try:
        model = load_model(args.model, args.conf)
        print("[INFO] Model geladen.")
    except Exception as e:
        print(f"[FOUT] {e}")
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
        debug_image(path, model)

    print(f"\n[INFO] Debug afbeeldingen opgeslagen in {DEBUG_DIR}/")


if __name__ == "__main__":
    main()
