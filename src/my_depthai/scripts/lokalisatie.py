"""
Bepaalt de oppaklocatie van een object uit een crop-afbeelding.
"""

import math
import cv2
import numpy as np

# ── Per-object strategieën ─────────────────────────────────────────────────────

PICK_PERCENT = 0.35

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

# ── Hulpfuncties ───────────────────────────────────────────────────────────────

def _sample_variance(crop, point, radius):
    h, w = crop.shape[:2]
    x, y = int(point[0]), int(point[1])
    x1, y1 = max(0, x - radius), max(0, y - radius)
    x2, y2 = min(w, x + radius), min(h, y + radius)
    region = crop[y1:y2, x1:x2]
    if region.size == 0:
        return 0.0
    return float(np.var(cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)))


def _axis_crop_intersections(cx, cy, dx, dy, w, h):
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


# ── Hoofdfunctie ───────────────────────────────────────────────────────────────

def lokaliseer(crop, label=""):
    """
    Bepaalt as-richting en oppakpunt van het object in de crop.

    Parameters:
        crop  : BGR afbeelding van de bounding box
        label : objectklasse (bv. "vork") — bepaalt strategie uit STRATEGIEEN

    Geeft (cx, cy, angle_deg, pick_x, pick_y, annotated_frame) terug.
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
        v = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)[:, :, 2]
        _, mask = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        mask     = cv2.medianBlur(mask, 5)
        cnts, _  = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in cnts if cv2.contourArea(c) >= min_area]
    else:
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
        if not contours and use_clahe:
            clahe    = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            contours = _run_canny(clahe.apply(gray))

    if not contours:
        annotated = crop.copy()
        cv2.putText(annotated, "Geen contour", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return cx, cy, 0.0, cx, cy, annotated

    groups = _group_touching_contours(contours)
    largest_group = max(groups, key=lambda g: sum(len(contours[i]) for i in g))
    merged_pts = np.vstack([contours[i].reshape(-1, 2) for i in largest_group]).astype(float)

    rect = cv2.minAreaRect(merged_pts.astype(np.float32))
    (rx, ry), (rw, rh), rect_angle = rect

    if rw < rh:
        rect_angle += 90

    rad = math.radians(rect_angle)
    dx  = math.cos(rad)
    dy  = math.sin(rad)

    end1, end2 = _axis_crop_intersections(cx, cy, dx, dy, w, h)

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

    if onderkant_regel == "breedste":
        bottom = end1 if spread1 >= spread2 else end2
        top    = end2 if spread1 >= spread2 else end1
    else:
        bottom = end1 if spread1 <= spread2 else end2
        top    = end2 if spread1 <= spread2 else end1

    pick = bottom + pick_percent * (top - bottom)

    # Werkelijke hoek van steel naar top — lost 180° ambiguïteit van minAreaRect op
    direction = top - bottom
    angle = math.degrees(math.atan2(direction[1], direction[0]))

    perp_rad = math.radians(angle + 90)
    pdx = math.cos(perp_rad)
    pdy = math.sin(perp_rad)

    pick = _center_on_contour(pick, pdx, pdy, contours, largest_group, w, h)
    pick_x, pick_y = int(pick[0]), int(pick[1])

    # ── Tekenen ──────────────────────────────────────────────────────────────────
    annotated = crop.copy()
    reach = max(w, h) * 2

    cv2.line(annotated,
             (int(cx - reach * dx), int(cy - reach * dy)),
             (int(cx + reach * dx), int(cy + reach * dy)),
             (0, 0, 255), 2)

    cv2.line(annotated,
             (int(pick_x - reach * pdx), int(pick_y - reach * pdy)),
             (int(pick_x + reach * pdx), int(pick_y + reach * pdy)),
             (0, 200, 0), 2)

    cv2.circle(annotated, (cx, cy), 6, (0, 0, 255), -1)
    cv2.circle(annotated, (pick_x, pick_y), 8, (0, 200, 0), -1)
    cv2.circle(annotated, (int(bottom[0]), int(bottom[1])), 8, (255, 165, 0), -1)
    cv2.putText(annotated, "onderkant", (int(bottom[0]) + 10, int(bottom[1]) + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)

    tag = f"[{label}]  " if label else ""
    cv2.putText(annotated, f"{tag}{angle:.1f} deg", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(annotated, f"oppak: ({pick_x},{pick_y})  {int(pick_percent*100)}%", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 0), 2)

    return cx, cy, angle, pick_x, pick_y, annotated
