# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

ROS1 Noetic workspace for a sorting pick-and-place robot cell. The vision component (this repo, branch `VisionFinnWindows`) runs on Windows for development/testing and on a Linux VM for full ROS integration. It detects objects (vork, lepel, schroevendraaier, tandenborstel) via YOLOv5 and exposes their 6D pose via a ROS service to the main robot program.

## Build & Run

**Build (Linux VM only):**
```bash
catkin build
source devel/setup.bash
```

**Run the vision node:**
```bash
roslaunch my_depthai vision.launch
```

**Call the service:**
```bash
rosservice call /vision/detect_object
```

**Standalone Windows test (no ROS needed):**
```bash
cd src/my_depthai/test
python test_detection.py --model ../models/model.pt [--image photo.jpg] [--conf 0.6]
```

**One-time calibration (Linux VM):**
```bash
cd src/my_depthai/scripts
python3 calibratie.py [--image photo.jpg] [--interactief]
```

## Architecture

```
OAK-D Camera (RGB only, 640×480)
    ↓
vision_node.py          — ROS node; background thread reads frames, serves /vision/detect_object
    ├── YOLOv5 inference (ultralytics, CPU by default)
    ├── lokalisatie.py  — finds pick point & orientation within bounding box (contour analysis)
    └── aruco_transform.py — converts pixel coords → robot base_link coords (mm)
```

The service response (`DetectObject.srv`) returns a `geometry_msgs/PoseStamped` with the pick pose in the robot base frame. Z is fixed (from `calibration.json`).

## Key Files

| File | Role |
|------|------|
| `src/my_depthai/scripts/vision_node.py` | Main ROS node |
| `src/my_depthai/scripts/lokalisatie.py` | Per-class pick-point strategy (contour/edge/HSV) |
| `src/my_depthai/scripts/aruco_transform.py` | Pixel→robot coordinate transform |
| `src/my_depthai/scripts/calibratie.py` | Generates `calibration.json` from ArUco markers |
| `src/my_depthai/scripts/calibratie_config.py` | Marker IDs and known robot coords (mm) |
| `src/my_depthai/config/vision_config.yaml` | Model path, confidence, camera settings, homography |
| `src/my_depthai/config/calibration.json` | Affine matrix output from calibration (do not hand-edit) |
| `src/my_depthai/srv/DetectObject.srv` | ROS service definition |
| `src/my_depthai/test/test_detection.py` | Windows standalone test |
| `src/my_depthai/test/config.py` | Per-class detection strategies and colors |

## Coordinate Transform

Two modes in `aruco_transform.py`:
- **Live ArUco** (`pixel_naar_robot`): detects markers each frame, computes affine on-the-fly — requires markers visible at runtime.
- **Pre-calibrated** (`pixel_naar_robot_gecalibreerd`): loads `calibration.json` — used by `vision_node.py` in production.

Calibration uses 3 ArUco markers (IDs 0, 1, 2) with known robot coords defined in `calibratie_config.py`. After running `calibratie.py` once, the markers can be removed.

## Per-Class Localization Strategies

Each class uses a different edge/segmentation method in `lokalisatie.py` to find the object's long axis and pick point:

| Class | Edge method | "Bottom" end |
|-------|-------------|--------------|
| vork | Canny(50,150) | Narrowest |
| lepel | Canny(30,100) + CLAHE | Narrowest |
| tandenborstel | Canny(50,150) | Narrowest |
| schroevendraaier | HSV value + Otsu | Widest |

Pick point = 50% along axis from bottom end. Debug images saved to `src/my_depthai/debug/`.

## Notes

- The workspace is shared with Tim's `Timhoofdprogramma` branch (main robot program). Vision exposes `/vision/detect_object`; the main program calls it.
- `core.protectNTFS` must be temporarily disabled to checkout `Timhoofdprogramma` on Windows (Tim's branch previously had `:Zone.Identifier` files; they have been removed as of 2026-06-16).
- All source comments and variable names are in Dutch.
- `models/model.pt` is the YOLOv5 weights file — not in git, must be present locally.
