"""
Bepaalt de oppaklocatie van een object uit een crop-afbeelding.

Gebruik:
    python test_lokalisatie.py
    python test_lokalisatie.py --image pad/naar/crop.jpg

Zonder --image: pakt de eerste afbeelding uit test_lokalisatie_input/.
Output: crop met rode as-lijn + groene oppak-lijn, opgeslagen in test_lokalisatie_output/.
"""

import argparse
import math
import os
import sys
import cv2
import numpy as np

from test_detection import IMAGE_EXTS
from config import PICK_PERCENT, STRATEGIEEN

INPUT_DIR  = os.path.join(os.path.dirname(__file__), "test_lokalisatie_input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_lokalisatie_output")


def _get_main_contour(crop):
    gray    = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges   = cv2.Canny(blurred, 30, 100)
    kernel  = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges   = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    return max(contours, key=cv2.contourArea)


def _sample_variance(crop, point, radius):
    """Gemiddelde grijswaarde-variance in een vierkant rondom point."""
    h, w = crop.shape[:2]
    x, y = int(point[0]), int(point[1])
    x1, y1 = max(0, x - radius), max(0, y - radius)
    x2, y2 = min(w, x + radius), min(h, y + radius)
    region = crop[y1:y2, x1:x2]
    if region.size == 0:
        return 0.0
    return float(np.var(cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)))


def _axis_crop_intersections(cx, cy, dx, dy, w, h):
    """Geeft de twee snijpunten van de as met de croprand terug."""
    t_values = []
    if abs(dx) > 1e-9:
        t_values += [(0 - cx) / dx, (w - cx) / dx]
    if abs(dy) > 1e-9:
        t_values += [(0 - cy) / dy, (h - cy) / dy]

    valid = []
    for t in t_values:
        px, py = cx + t * dx, cy + t * dy
        if -1 <= px <= w + 1 and -1 <= py <= h + 1:
            valid.append((t, np.array([px, py])))

    valid.sort(key=lambda x: x[0])
    return valid[0][1], valid[-1][1]


def _center_on_contour(pick, pdx, pdy, contours, largest_group, w, h):
    """Verschuift pick naar het midden van de twee contoursnijpunten op de loodrechte lijn."""
    mask = np.zeros((h, w), dtype=np.uint8)
    for i in largest_group:
        cv2.drawContours(mask, contours, i, 255, cv2.FILLED)

    reach = max(w, h)
    inside_ts = []
    for t in range(-reach, reach):
        px = int(round(pick[0] + t * pdx))
        py = int(round(pick[1] + t * pdy))
        if 0 <= px < w and 0 <= py < h and mask[py, px] > 0:
            inside_ts.append(t)

    if len(inside_ts) < 2:
        return pick

    t_mid = (inside_ts[0] + inside_ts[-1]) / 2.0
    return np.array([pick[0] + t_mid * pdx, pick[1] + t_mid * pdy])


def _group_touching_contours(contours):
    """Groepeert contours die elkaar raken via bounding-rect overlap (1px tolerantie)."""
    n = len(contours)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rects = [cv2.boundingRect(c) for c in contours]
    for i in range(n):
        x1, y1, w1, h1 = rects[i]
        for j in range(i + 1, n):
            x2, y2, w2, h2 = rects[j]
            if (x1 - 1 <= x2 + w2 and x1 + w1 + 1 >= x2 and
                    y1 - 1 <= y2 + h2 and y1 + h1 + 1 >= y2):
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[ri] = rj

    groups: dict = {}
    for i in range(n):
        root = find(i)
        groups.setdefault(root, []).append(i)
    return list(groups.values())


def lokaliseer(crop, label=""):
    """
    Bepaalt as-richting, onderkant (handle) en oppakpunt van het object.
    Geeft (cx, cy, angle_deg, pick_x, pick_y, annotated_frame) terug.
    label: objectklasse (bv. "vork") — bepaalt strategie uit STRATEGIEEN.
    """
    strategie       = STRATEGIEEN.get(label, {})
    method          = strategie.get("method",       "canny")
    pick_percent    = strategie.get("pick_percent", PICK_PERCENT)
    canny_low       = strategie.get("canny_low",    50)
    canny_high      = strategie.get("canny_high",   150)
    use_clahe       = strategie.get("clahe",        False)
    use_denoise     = strategie.get("denoise",      False)
    min_area        = strategie.get("min_area",     500)
    onderkant_regel = strategie.get("onderkant",    "smalste")

    h, w = crop.shape[:2]
    cx, cy = w // 2, h // 2

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    if method == "value_otsu":
        # HSV Value-kanaal + Otsu drempel + mediaan filter
        v = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)[:, :, 2]
        _, mask = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        mask     = cv2.medianBlur(mask, 5)
        cnts, _  = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in cnts if cv2.contourArea(c) >= min_area]
    else:
        # Canny — eerst zonder CLAHE proberen
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        def _run_canny(g):
            if use_denoise:
                g = cv2.bilateralFilter(g, d=9, sigmaColor=75, sigmaSpace=75)
            blurred = cv2.GaussianBlur(g, (5, 5), 0)
            edges   = cv2.Canny(blurred, canny_low, canny_high)
            edges   = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
            cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            return [c for c in cnts if cv2.contourArea(c) >= min_area]

        contours = _run_canny(gray)

        # CLAHE alleen als fallback: geen contours gevonden op normale Canny
        if not contours and use_clahe:
            clahe    = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            contours = _run_canny(clahe.apply(gray))

    if not contours:
        angle = 0.0
        pick_x, pick_y = cx, cy
        annotated = crop.copy()
        cv2.putText(annotated, "Geen contour", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return cx, cy, angle, pick_x, pick_y, annotated

    # Groepeer rakende contours, gebruik de grootste groep
    groups = _group_touching_contours(contours)
    largest_group = max(groups, key=lambda g: sum(len(contours[i]) for i in g))
    merged_pts = np.vstack([contours[i].reshape(-1, 2) for i in largest_group]).astype(float)

    rect = cv2.minAreaRect(merged_pts.astype(np.float32))
    (rx, ry), (rw, rh), rect_angle = rect

    # Zorg dat de hoek altijd langs de lange as staat
    if rw < rh:
        rect_angle += 90
    angle = rect_angle

    rad = math.radians(angle)
    dx  = math.cos(rad)
    dy  = math.sin(rad)

    # Snijpunten van de as (door crop-midden) met de croprand = werkelijke eindpunten
    end1, end2 = _axis_crop_intersections(cx, cy, dx, dy, w, h)

    # Onderkant = smalste kant: laagste spreiding loodrecht op de as
    pts = merged_pts
    perp_dx, perp_dy = -dy, dx

    projections = (pts[:, 0] - cx) * dx + (pts[:, 1] - cy) * dy
    t_min, t_max = projections.min(), projections.max()
    threshold = (t_max - t_min) * 0.25

    end1_pts, end2_pts = [], []
    t_end1 = (end1[0] - cx) * dx + (end1[1] - cy) * dy
    t_end2 = (end2[0] - cx) * dx + (end2[1] - cy) * dy

    for pt in pts:
        t = (pt[0] - cx) * dx + (pt[1] - cy) * dy
        s = pt[0] * perp_dx + pt[1] * perp_dy
        if t < min(t_end1, t_end2) + threshold:
            end1_pts.append(s)
        if t > max(t_end1, t_end2) - threshold:
            end2_pts.append(s)

    spread1 = np.std(end1_pts) if end1_pts else 0.0
    spread2 = np.std(end2_pts) if end2_pts else 0.0

    # Onderkant bepalen op basis van strategie
    if onderkant_regel == "breedste":
        # Breedste kant = handgreep (bv. schroevendraaier)
        bottom = end1 if spread1 >= spread2 else end2
        top    = end2 if spread1 >= spread2 else end1
    else:
        # Smalste kant = handgreep (bv. vork, lepel, tandenborstel)
        bottom = end1 if spread1 <= spread2 else end2
        top    = end2 if spread1 <= spread2 else end1

    # Oppakpunt langs de as
    pick = bottom + pick_percent * (top - bottom)

    # Loodrechte richting (ook gebruikt voor centrering en groene lijn)
    perp_rad = math.radians(angle + 90)
    pdx = math.cos(perp_rad)
    pdy = math.sin(perp_rad)

    # Verschuif oppakpunt naar het midden van de contour op de loodrechte lijn
    pick = _center_on_contour(pick, pdx, pdy, contours, largest_group, w, h)
    pick_x, pick_y = int(pick[0]), int(pick[1])

    # ── Tekenen ──────────────────────────────────
    annotated = crop.copy()
    reach = max(w, h) * 2

    # Rode lijn: as van rand tot rand
    cv2.line(annotated,
             (int(cx - reach * dx), int(cy - reach * dy)),
             (int(cx + reach * dx), int(cy + reach * dy)),
             (0, 0, 255), 2)

    # Groene lijn: loodrecht op de as door het oppakpunt, rand tot rand
    cv2.line(annotated,
             (int(pick_x - reach * pdx), int(pick_y - reach * pdy)),
             (int(pick_x + reach * pdx), int(pick_y + reach * pdy)),
             (0, 200, 0), 2)

    # Middelpunt (rood) en oppakpunt (groen)
    cv2.circle(annotated, (cx, cy), 6, (0, 0, 255), -1)
    cv2.circle(annotated, (pick_x, pick_y), 8, (0, 200, 0), -1)

    # Onderkant markering
    cv2.circle(annotated, (int(bottom[0]), int(bottom[1])), 8, (255, 165, 0), -1)
    cv2.putText(annotated, "onderkant", (int(bottom[0]) + 10, int(bottom[1]) + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)

    tag = f"[{label}]  " if label else ""
    cv2.putText(annotated, f"{tag}{angle:.1f} deg", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(annotated, f"oppak: ({pick_x},{pick_y})  {int(pick_percent*100)}%", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 0), 2)

    return cx, cy, angle, pick_x, pick_y, annotated


def main():
    parser = argparse.ArgumentParser(description="Lokaliseer oppakpositie vanuit crop")
    parser.add_argument("--image", default=None, help="Pad naar crop-afbeelding")
    args = parser.parse_args()

    if args.image:
        image_paths = [args.image]
    else:
        candidates = sorted(
            f for f in os.listdir(INPUT_DIR)
            if os.path.splitext(f)[1].lower() in IMAGE_EXTS
        )
        if not candidates:
            print(f"[FOUT] Geen afbeeldingen gevonden in {INPUT_DIR}")
            sys.exit(1)
        image_paths = [os.path.join(INPUT_DIR, f) for f in candidates]
        print(f"[INFO] {len(image_paths)} afbeelding(en) gevonden\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []

    for image_path in image_paths:
        crop = cv2.imread(image_path)
        if crop is None:
            print(f"[OVERGESLAGEN] Kan niet openen: {image_path}")
            continue

        # Label afleiden uit bestandsnaam (bv. "bb_schroevendraaier_1.JPG" → "schroevendraaier")
        stem = os.path.splitext(os.path.basename(image_path))[0].lower()
        label = next((k for k in STRATEGIEEN if k in stem), "")

        cx, cy, angle, pick_x, pick_y, annotated = lokaliseer(crop, label)
        strat = STRATEGIEEN.get(label, {})
        pct   = strat.get("pick_percent", PICK_PERCENT)
        regel = strat.get("onderkant", "smalste")
        print(f"[{os.path.basename(image_path)}]")
        print(f"  object   : {label or '(onbekend)'}")
        print(f"  strategie: onderkant={regel}  pick={int(pct*100)}%")
        print(f"  hoek     : {angle:.1f}°")
        print(f"  oppak    : ({pick_x},{pick_y})px")

        output_path = os.path.join(OUTPUT_DIR, os.path.basename(image_path))
        cv2.imwrite(output_path, annotated)
        print(f"  -> {output_path}\n")

        results.append({
            "cx": cx, "cy": cy, "angle": angle,
            "pick_x": pick_x, "pick_y": pick_y,
            "frame": annotated, "image_path": output_path,
        })

    return results


if __name__ == "__main__":
    main()
