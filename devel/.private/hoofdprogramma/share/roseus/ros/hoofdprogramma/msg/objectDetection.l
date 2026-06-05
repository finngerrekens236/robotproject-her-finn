;; Auto-generated. Do not edit!


(when (boundp 'hoofdprogramma::objectDetection)
  (if (not (find-package "HOOFDPROGRAMMA"))
    (make-package "HOOFDPROGRAMMA"))
  (shadow 'objectDetection (find-package "HOOFDPROGRAMMA")))
(unless (find-package "HOOFDPROGRAMMA::OBJECTDETECTION")
  (make-package "HOOFDPROGRAMMA::OBJECTDETECTION"))

(in-package "ROS")
;;//! \htmlinclude objectDetection.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass hoofdprogramma::objectDetection
  :super ros::object
  :slots (_object_type _pose _confidence ))

(defmethod hoofdprogramma::objectDetection
  (:init
   (&key
    ((:object_type __object_type) "")
    ((:pose __pose) (instance geometry_msgs::Pose :init))
    ((:confidence __confidence) 0.0)
    )
   (send-super :init)
   (setq _object_type (string __object_type))
   (setq _pose __pose)
   (setq _confidence (float __confidence))
   self)
  (:object_type
   (&optional __object_type)
   (if __object_type (setq _object_type __object_type)) _object_type)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:confidence
   (&optional __confidence)
   (if __confidence (setq _confidence __confidence)) _confidence)
  (:serialization-length
   ()
   (+
    ;; string _object_type
    4 (length _object_type)
    ;; geometry_msgs/Pose _pose
    (send _pose :serialization-length)
    ;; float32 _confidence
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _object_type
       (write-long (length _object_type) s) (princ _object_type s)
     ;; geometry_msgs/Pose _pose
       (send _pose :serialize s)
     ;; float32 _confidence
       (sys::poke _confidence (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _object_type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _object_type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; geometry_msgs/Pose _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;; float32 _confidence
     (setq _confidence (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get hoofdprogramma::objectDetection :md5sum-) "51cf1d8d3850a43ca6b509aa1916ae48")
(setf (get hoofdprogramma::objectDetection :datatype-) "hoofdprogramma/objectDetection")
(setf (get hoofdprogramma::objectDetection :definition-)
      "string object_type
geometry_msgs/Pose pose
float32 confidence

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



(provide :hoofdprogramma/objectDetection "51cf1d8d3850a43ca6b509aa1916ae48")


