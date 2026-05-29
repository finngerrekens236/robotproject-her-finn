"""
Simpele OAK-D RGB Camera Viewer
Druk op 'q' om te stoppen.
"""

import depthai as dai
import cv2

pipeline = dai.Pipeline()

camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setPreviewSize(640, 480)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("rgb")
camRgb.preview.link(xout.input)

with dai.Device(pipeline) as device:
    q = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    print("OAK-D camera gestart. Druk op 'q' om te stoppen.")
    while True:
        frame = q.get()
        cv2.imshow("OAK-D RGB", frame.getCvFrame())
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()
