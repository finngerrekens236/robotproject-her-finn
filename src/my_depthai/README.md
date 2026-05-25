# my_depthai — Vision package

Sorting pick-and-place robotcel | OAK-D RGB camera + YOLOv5 + ROS Noetic

## Overzicht

| Component | Beschrijving |
|---|---|
| `scripts/vision_node.py` | ROS node (draait op Linux VM) |
| `test/test_detection.py` | Standalone testscript (draait op Windows, geen ROS) |
| `config/vision_config.yaml` | Alle instellingen (model pad, klassen, kalibratie) |
| `models/model.pt` | Getraind YOLOv5 model (hier kopiëren na training) |
| `srv/DetectObject.srv` | Custom ROS service definitie |
| `launch/vision.launch` | ROS launch file |

---

## 1. Windows — testscript (geen ROS)

### Dependencies installeren

```bash
pip install depthai opencv-python torch torchvision pyyaml
```

### Model kopiëren

Kopieer je getrainde `model.pt` uit Google Drive naar:
```
ufactory_ws/src/my_depthai/models/model.pt
```

### Draaien

```bash
cd ufactory_ws/src/my_depthai/test

# Met OAK-D camera (automatisch gevonden)
python test_detection.py --model ../models/model.pt

# Met een testafbeelding (geen camera nodig)
python test_detection.py --model ../models/model.pt --image mijn_foto.jpg

# Confidence threshold aanpassen
python test_detection.py --model ../models/model.pt --conf 0.6
```

### Wat je ziet

- Live camera beeld met bounding boxes, labels en confidence scores
- Pijl die de rotatie van het object aangeeft
- Pixelcoördinaten en hoek in graden geprint in de terminal

---

## 2. Linux VM — ROS node

### VM setup (eenmalig)

```bash
# ROS Noetic basis al geïnstalleerd? Dan alleen:
sudo apt install ros-noetic-cv-bridge python3-rospy python3-yaml

pip3 install depthai torch torchvision opencv-python pyyaml
```

### Workspace bouwen

```bash
# Kopieer de hele ufactory_ws/ map naar de VM, dan:
cd ~/ufactory_ws
catkin build          # of: catkin_make
source devel/setup.bash
```

### Model kopiëren

```bash
cp model.pt ~/ufactory_ws/src/my_depthai/models/model.pt
```

### Vision node starten

```bash
roslaunch my_depthai vision.launch
```

### Service aanroepen (vanuit een andere terminal, ter test)

```bash
source ~/ufactory_ws/devel/setup.bash
rosservice call /vision/detect_object
```

### Service aanroepen vanuit het hoofdprogramma (Python)

```python
import rospy
from my_depthai.srv import DetectObject

rospy.wait_for_service('/vision/detect_object')
detect = rospy.ServiceProxy('/vision/detect_object', DetectObject)

resp = detect()
if resp.success:
    print(resp.object_class)           # bijv. "lepel"
    print(resp.pick_pose.pose.position)  # x, y, z in robot coördinaten
    print(resp.message)
```

---

## 3. Kalibratie (pixel -> robot coördinaten)

De `homography` matrix in `config/vision_config.yaml` zet pixelcoördinaten om naar
robotcoördinaten. Stap voor stap:

1. Leg minstens 4 bekende punten op de conveyor belt (bijv. hoeken van een raster)
2. Meet de pixelcoördinaten via het testscript (kijk in de terminal output)
3. Meet de robot XY-coördinaten van dezelfde punten (bijv. via teach pendant)
4. Bereken de homografie:

```python
import cv2, numpy as np

# Pixelcoördinaten [px, py] van de kalibratiepunten
src = np.float32([[px1,py1],[px2,py2],[px3,py3],[px4,py4]])
# Robot XY-coördinaten [rx, ry] van dezelfde punten
dst = np.float32([[rx1,ry1],[rx2,ry2],[rx3,ry3],[rx4,ry4]])

H, _ = cv2.findHomography(src, dst)
print(H.tolist())   # kopieer dit naar vision_config.yaml -> calibration.homography
```

5. Vul de matrix in `vision_config.yaml` in onder `calibration.homography`

---

## Opmerking over de OAK-D

De OAK-D wordt in dit project **alleen als RGB camera** gebruikt:
- Geen depth / stereo
- Geen on-device neural network (geen .blob conversie)
- Inferentie gebeurt op de computer zelf via PyTorch

De depthai library opent de camera en geeft ruwe RGB frames terug;
YOLOv5 + OpenCV doen de rest.
