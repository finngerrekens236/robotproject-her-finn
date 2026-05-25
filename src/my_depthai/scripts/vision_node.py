#!/usr/bin/env python3
"""
ROS vision node voor de sorting pick-and-place robotcel.

Start:  roslaunch my_depthai vision.launch
Service: /vision/detect_object  (my_depthai/DetectObject)

De node:
  1. Opent de OAK-D als pure RGB camera
  2. Laadt het YOLOv5 .pt model via PyTorch
  3. Wacht op service calls van het hoofdprogramma
  4. Bij een call: detecteer + lokaliseer -> geef PoseStamped terug
"""

import os
import sys
import math

import cv2
import numpy as np
import torch
import yaml

import rospy
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped, Quaternion
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from my_depthai.srv import DetectObject, DetectObjectResponse

# ──────────────────────────────────────────────
# Hulpfuncties
# ──────────────────────────────────────────────

def euler_z_to_quaternion(rz_rad):
    """Rotatie om Z-as (in radialen) -> geometry_msgs/Quaternion."""
    return Quaternion(
        x=0.0,
        y=0.0,
        z=math.sin(rz_rad / 2.0),
        w=math.cos(rz_rad / 2.0),
    )


def pixel_to_robot(px, py, H, z_conveyor):
    """
    Transformeer pixel (px, py) naar robot XYZ via homografie matrix H.
    Z is de vaste hoogte van de conveyor belt.
    """
    pt = np.array([px, py, 1.0], dtype=np.float64)
    robot_h = H @ pt
    robot_h /= robot_h[2]  # homogene deling
    return float(robot_h[0]), float(robot_h[1]), float(z_conveyor)


def get_pose_in_bbox(frame, x1, y1, x2, y2):
    """
    Bereken precieze positie (cx, cy in pixels) en rotatie (graden)
    binnen de bounding box via contour analysis en minAreaRect.
    """
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        return (x1 + x2) // 2, (y1 + y2) // 2, 0.0

    gray    = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    binary  = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
        blockSize=21, C=4,
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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


# ──────────────────────────────────────────────
# VisionNode klasse
# ──────────────────────────────────────────────

class VisionNode:

    def __init__(self):
        rospy.init_node("vision_node", anonymous=False)

        # Config laden
        pkg_dir   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cfg_path  = rospy.get_param("~config", os.path.join(pkg_dir, "config", "vision_config.yaml"))
        with open(cfg_path, "r") as f:
            self.cfg = yaml.safe_load(f)

        self.classes    = self.cfg["classes"]
        self.conf_thresh = self.cfg["model"]["confidence_threshold"]
        self.z_conveyor  = self.cfg["calibration"]["z_conveyor"]
        self.H           = np.array(self.cfg["calibration"]["homography"], dtype=np.float64)

        # Model laden
        model_path = os.path.join(pkg_dir, self.cfg["model"]["path"])
        rospy.loginfo(f"[vision_node] Model laden: {model_path}")
        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom",
            path=model_path, force_reload=False, verbose=False,
        )
        self.model.conf = self.conf_thresh
        self.model.eval()
        rospy.loginfo("[vision_node] Model geladen.")

        # Camera initialiseren (OAK-D als pure RGB)
        self._init_camera()

        # ROS publishers / services
        self.bridge        = CvBridge()
        self.img_pub       = rospy.Publisher(
            self.cfg["ros"]["image_topic"], Image, queue_size=1)
        self.debug_img_pub = rospy.Publisher(
            self.cfg["ros"]["debug_image_topic"], Image, queue_size=1)

        self.service = rospy.Service(
            self.cfg["ros"]["service_name"],
            DetectObject,
            self._handle_detect,
        )
        rospy.loginfo(f"[vision_node] Service klaar: {self.cfg['ros']['service_name']}")

    # ── Camera ──────────────────────────────────

    def _init_camera(self):
        import depthai as dai
        import time

        pipeline = dai.Pipeline()
        cam_rgb  = pipeline.create(dai.node.ColorCamera)
        xout     = pipeline.create(dai.node.XLinkOut)
        xout.setStreamName("rgb")

        w = self.cfg["camera"]["width"]
        h = self.cfg["camera"]["height"]
        cam_rgb.setPreviewSize(w, h)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setFps(self.cfg["camera"]["fps"])
        cam_rgb.preview.link(xout.input)

        device_id = self.cfg["camera"].get("device_id", "")

        # Probeer camera te verbinden met retry
        max_retries = 5
        for attempt in range(max_retries):
            try:
                if device_id:
                    self.device = dai.Device(pipeline, dai.DeviceInfo(device_id))
                else:
                    self.device = dai.Device(pipeline)
                self.q_rgb = self.device.getOutputQueue(name="rgb", maxSize=1, blocking=True)
                rospy.loginfo("[vision_node] OAK-D camera geïnitialiseerd.")
                return
            except RuntimeError as e:
                rospy.logwarn(f"[vision_node] Camera niet gevonden (poging {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)

        rospy.logerr("[vision_node] Camera kon niet geïnitialiseerd worden na {0} pogingen".format(max_retries))
        raise RuntimeError("OAK-D camera niet beschikbaar")

    def _get_frame(self):
        pkt = self.q_rgb.get()
        return pkt.getCvFrame()  # BGR numpy array

    # ── Detectie ────────────────────────────────

    def _detect(self, frame):
        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(rgb)
        return results.pandas().xyxy[0]

    def _best_detection(self, detections):
        """Geeft de detectie met de hoogste confidence terug (of None)."""
        if len(detections) == 0:
            return None
        return detections.loc[detections["confidence"].idxmax()]

    # ── Service handler ──────────────────────────

    def _handle_detect(self, _req):
        resp = DetectObjectResponse()

        try:
            frame = self._get_frame()

            # Publiceer raw image
            self.img_pub.publish(
                self.bridge.cv2_to_imgmsg(frame, encoding="bgr8"))

            detections = self._detect(frame)
            best       = self._best_detection(detections)

            if best is None:
                resp.success      = False
                resp.message      = "Geen object gevonden"
                resp.object_class = ""
                return resp

            x1, y1, x2, y2 = (int(best.xmin), int(best.ymin),
                               int(best.xmax), int(best.ymax))
            cls_id  = int(best["class"])
            label   = self.classes[cls_id] if cls_id < len(self.classes) else best["name"]

            cx, cy, angle_deg = get_pose_in_bbox(frame, x1, y1, x2, y2)
            rx, ry, rz_height = pixel_to_robot(cx, cy, self.H, self.z_conveyor)
            rz_rad            = math.radians(angle_deg)

            # PoseStamped opbouwen
            pose           = PoseStamped()
            pose.header    = Header(stamp=rospy.Time.now(), frame_id="base_link")
            pose.pose.position.x    = rx
            pose.pose.position.y    = ry
            pose.pose.position.z    = rz_height
            pose.pose.orientation   = euler_z_to_quaternion(rz_rad)

            resp.success      = True
            resp.object_class = label
            resp.message      = (f"Gevonden: {label} conf={best['confidence']:.2f} "
                                 f"pos=({rx:.4f},{ry:.4f},{rz_height:.4f}) "
                                 f"rz={angle_deg:.1f}deg")
            resp.pick_pose    = pose

            rospy.loginfo(f"[vision_node] {resp.message}")

            # Debug image
            debug = frame.copy()
            cv2.rectangle(debug, (x1, y1), (x2, y2), (0, 200, 0), 2)
            cv2.circle(debug, (cx, cy), 6, (0, 0, 255), -1)
            length = 50
            rad    = math.radians(angle_deg)
            ex     = int(cx + length * math.cos(rad))
            ey     = int(cy + length * math.sin(rad))
            cv2.arrowedLine(debug, (cx, cy), (ex, ey), (0, 0, 255), 2, tipLength=0.3)
            cv2.putText(debug, f"{label} {best['confidence']:.2f}",
                        (x1, max(y1 - 8, 12)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)
            self.debug_img_pub.publish(
                self.bridge.cv2_to_imgmsg(debug, encoding="bgr8"))

        except Exception as e:
            rospy.logerr(f"[vision_node] Fout: {e}")
            resp.success  = False
            resp.message  = str(e)

        return resp

    # ── Spin ────────────────────────────────────

    def spin(self):
        rospy.loginfo("[vision_node] Klaar, wacht op service calls...")
        rospy.spin()


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if __name__ == "__main__":
    try:
        node = VisionNode()
        node.spin()
    except rospy.ROSInterruptException:
        pass
