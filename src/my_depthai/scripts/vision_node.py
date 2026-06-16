#!/usr/bin/env python3
"""
ROS vision node voor de sorting pick-and-place robotcel.
"""

import json
import os
import sys
import math
import time
import threading

import cv2
import numpy as np
import torch
import yaml

import rospy
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped, Quaternion, Pose

from my_depthai.srv import DetectObject, DetectObjectResponse

_pkg_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_scripts_dir = os.path.dirname(os.path.abspath(__file__))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from lokalisatie import lokaliseer


def euler_z_to_quaternion(rz_rad):
    return Quaternion(
        x=0.0,
        y=0.0,
        z=math.sin(rz_rad / 2.0),
        w=math.cos(rz_rad / 2.0),
    )


def pixel_to_robot(px, py, H, z_conveyor):
    pt = np.array([px, py, 1.0], dtype=np.float64)
    robot_h = H @ pt
    robot_h /= robot_h[2]
    return float(robot_h[0]), float(robot_h[1]), float(z_conveyor)


class VisionNode:

    def __init__(self):
        rospy.init_node("vision_node", anonymous=False)

        pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cfg_path = rospy.get_param("~config", os.path.join(pkg_dir, "config", "vision_config.yaml"))

        with open(cfg_path, "r") as f:
            self.cfg = yaml.safe_load(f)

        self.classes = self.cfg["classes"]
        self.conf_thresh = self.cfg["model"]["confidence_threshold"]

        cal_path = os.path.join(pkg_dir, "config", "calibration.json")

        if os.path.exists(cal_path):
            with open(cal_path, "r") as f:
                cal = json.load(f)

            M = np.array(cal["affine_matrix"], dtype=np.float64)
            self.H = np.vstack([M, [0.0, 0.0, 1.0]])
            self.z_conveyor = cal["z_conveyor"]
            self.rotation_offset_deg = cal["rotation_offset_deg"]

            det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
            self.angle_sign = -1.0 if det < 0 else 1.0
        else:
            self.z_conveyor = self.cfg["calibration"]["z_conveyor"]
            self.H = np.array(self.cfg["calibration"]["homography"], dtype=np.float64)
            self.rotation_offset_deg = 0.0
            self.angle_sign = 1.0

        model_path = os.path.join(pkg_dir, self.cfg["model"]["path"])
        self.model = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path=model_path,
            force_reload=False,
            verbose=False,
        )

        self.model.conf = self.conf_thresh
        self.model.eval()

        self._init_camera()

        self.debug_dir = os.path.join(pkg_dir, "debug")
        os.makedirs(self.debug_dir, exist_ok=True)

        self.service = rospy.Service(
            self.cfg["ros"]["service_name"],
            DetectObject,
            self._handle_detect,
        )

    def _init_camera(self):
        import depthai as dai

        pipeline = dai.Pipeline()
        cam_rgb = pipeline.create(dai.node.ColorCamera)
        xout = pipeline.create(dai.node.XLinkOut)
        xout.setStreamName("rgb")

        w = self.cfg["camera"]["width"]
        h = self.cfg["camera"]["height"]

        cam_rgb.setPreviewSize(w, h)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setFps(self.cfg["camera"]["fps"])
        cam_rgb.preview.link(xout.input)

        self.device = dai.Device(pipeline)
        self.q_rgb = self.device.getOutputQueue("rgb", maxSize=4, blocking=False)

        self._latest_frame = None
        self._lock = threading.Lock()
        self._event = threading.Event()

        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        while not rospy.is_shutdown():
            pkt = self.q_rgb.get()
            with self._lock:
                self._latest_frame = pkt.getCvFrame()
            self._event.set()

    def _get_frame(self):
        self._event.clear()
        self._event.wait(timeout=5)
        with self._lock:
            return self._latest_frame.copy()

    def _detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(rgb)
        return results.pandas().xyxy[0]

    def _best_detection(self, det):
        if len(det) == 0:
            return None
        return det.loc[det["confidence"].idxmax()]

    def _handle_detect(self, _req):
        resp = DetectObjectResponse()

        try:
            frame = self._get_frame()
            det = self._detect(frame)
            best = self._best_detection(det)

            if best is None:
                resp.success = False
                resp.message = "Geen object"
                return resp

            x1, y1, x2, y2 = int(best.xmin), int(best.ymin), int(best.xmax), int(best.ymax)

            crop = frame[y1:y2, x1:x2]
            _, _, angle_deg, px, py, _ = lokaliseer(crop, best["name"])

            cx = x1 + px
            cy = y1 + py

            rx, ry, rz = pixel_to_robot(cx, cy, self.H, self.z_conveyor)

            robot_angle = self.angle_sign * angle_deg + self.rotation_offset_deg
            rz_rad = math.radians(robot_angle)

            rx /= 1000.0
            ry /= 1000.0
            rz = 0.165

            pose = PoseStamped()
            pose.header = Header(stamp=rospy.Time.now(), frame_id="link_base")

            pose.pose.position.x = rx
            pose.pose.position.y = ry
            pose.pose.position.z = rz

            quat = euler_z_to_quaternion(rz_rad)
            pose.pose.orientation = quat

            rospy.loginfo(
                "pos=(%.4f, %.4f, %.4f) quat=(%.6f, %.6f, %.6f, %.6f)" %
                (rx, ry, rz, quat.x, quat.y, quat.z, quat.w)
            )

            resp.success = True
            resp.pick_pose = pose
            resp.object_class = best["name"]

        except Exception as e:
            resp.success = False
            resp.message = str(e)

        return resp

    def spin(self):
        rospy.spin()


if __name__ == "__main__":
    VisionNode().spin()
