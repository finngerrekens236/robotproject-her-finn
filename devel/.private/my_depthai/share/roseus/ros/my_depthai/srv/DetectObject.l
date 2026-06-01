;; Auto-generated. Do not edit!


(when (boundp 'my_depthai::DetectObject)
  (if (not (find-package "MY_DEPTHAI"))
    (make-package "MY_DEPTHAI"))
  (shadow 'DetectObject (find-package "MY_DEPTHAI")))
(unless (find-package "MY_DEPTHAI::DETECTOBJECT")
  (make-package "MY_DEPTHAI::DETECTOBJECT"))
(unless (find-package "MY_DEPTHAI::DETECTOBJECTREQUEST")
  (make-package "MY_DEPTHAI::DETECTOBJECTREQUEST"))
(unless (find-package "MY_DEPTHAI::DETECTOBJECTRESPONSE")
  (make-package "MY_DEPTHAI::DETECTOBJECTRESPONSE"))

(in-package "ROS")



(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass my_depthai::DetectObjectRequest
  :super ros::object
  :slots ())

(defmethod my_depthai::DetectObjectRequest
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass my_depthai::DetectObjectResponse
  :super ros::object
  :slots (_success _object_class _message _pick_pose ))

(defmethod my_depthai::DetectObjectResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:object_class __object_class) "")
    ((:message __message) "")
    ((:pick_pose __pick_pose) (instance geometry_msgs::PoseStamped :init))
    )
   (send-super :init)
   (setq _success __success)
   (setq _object_class (string __object_class))
   (setq _message (string __message))
   (setq _pick_pose __pick_pose)
   self)
  (:success
   (&optional __success)
   (if __success (setq _success __success)) _success)
  (:object_class
   (&optional __object_class)
   (if __object_class (setq _object_class __object_class)) _object_class)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:pick_pose
   (&rest __pick_pose)
   (if (keywordp (car __pick_pose))
       (send* _pick_pose __pick_pose)
     (progn
       (if __pick_pose (setq _pick_pose (car __pick_pose)))
       _pick_pose)))
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _object_class
    4 (length _object_class)
    ;; string _message
    4 (length _message)
    ;; geometry_msgs/PoseStamped _pick_pose
    (send _pick_pose :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _object_class
       (write-long (length _object_class) s) (princ _object_class s)
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;; geometry_msgs/PoseStamped _pick_pose
       (send _pick_pose :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _object_class
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _object_class (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; geometry_msgs/PoseStamped _pick_pose
     (send _pick_pose :deserialize buf ptr-) (incf ptr- (send _pick_pose :serialization-length))
   ;;
   self)
  )

(defclass my_depthai::DetectObject
  :super ros::object
  :slots ())

(setf (get my_depthai::DetectObject :md5sum-) "b95455854c5d28811eaccdf7054b9b90")
(setf (get my_depthai::DetectObject :datatype-) "my_depthai/DetectObject")
(setf (get my_depthai::DetectObject :request) my_depthai::DetectObjectRequest)
(setf (get my_depthai::DetectObject :response) my_depthai::DetectObjectResponse)

(defmethod my_depthai::DetectObjectRequest
  (:response () (instance my_depthai::DetectObjectResponse :init)))

(setf (get my_depthai::DetectObjectRequest :md5sum-) "b95455854c5d28811eaccdf7054b9b90")
(setf (get my_depthai::DetectObjectRequest :datatype-) "my_depthai/DetectObjectRequest")
(setf (get my_depthai::DetectObjectRequest :definition-)
      "# Request: leeg — gewoon triggeren is genoeg
---
# Response
bool success
string object_class
string message
geometry_msgs/PoseStamped pick_pose


================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
")

(setf (get my_depthai::DetectObjectResponse :md5sum-) "b95455854c5d28811eaccdf7054b9b90")
(setf (get my_depthai::DetectObjectResponse :datatype-) "my_depthai/DetectObjectResponse")
(setf (get my_depthai::DetectObjectResponse :definition-)
      "# Request: leeg — gewoon triggeren is genoeg
---
# Response
bool success
string object_class
string message
geometry_msgs/PoseStamped pick_pose


================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
")



(provide :my_depthai/DetectObject "b95455854c5d28811eaccdf7054b9b90")


