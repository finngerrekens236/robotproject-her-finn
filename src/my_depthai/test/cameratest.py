"""
Simpele OAK-D RGB Camera Viewer
Druk op 'q' om te stoppen.
"""

import depthai as dai
import cv2

pipeline = dai.Pipeline()
cam = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
videoOut = cam.requestOutput((640, 480), type=dai.ImgFrame.Type.BGR888p)
queue = videoOut.createOutputQueue(maxSize=4, blocking=False)

pipeline.start()
print("OAK-D camera gestart. Druk op 'q' om te stoppen.")

while pipeline.isRunning():
    frame = queue.tryGet()
    if frame is not None:
        cv2.imshow("OAK-D RGB", frame.getCvFrame())
    if cv2.waitKey(1) == ord('q'):
        pipeline.stop()
        break

cv2.destroyAllWindows()
