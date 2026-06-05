; Auto-generated. Do not edit!


(cl:in-package hoofdprogramma-msg)


;//! \htmlinclude objectDetection.msg.html

(cl:defclass <objectDetection> (roslisp-msg-protocol:ros-message)
  ((object_type
    :reader object_type
    :initarg :object_type
    :type cl:string
    :initform "")
   (pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (confidence
    :reader confidence
    :initarg :confidence
    :type cl:float
    :initform 0.0))
)

(cl:defclass objectDetection (<objectDetection>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <objectDetection>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'objectDetection)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-msg:<objectDetection> is deprecated: use hoofdprogramma-msg:objectDetection instead.")))

(cl:ensure-generic-function 'object_type-val :lambda-list '(m))
(cl:defmethod object_type-val ((m <objectDetection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-msg:object_type-val is deprecated.  Use hoofdprogramma-msg:object_type instead.")
  (object_type m))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <objectDetection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-msg:pose-val is deprecated.  Use hoofdprogramma-msg:pose instead.")
  (pose m))

(cl:ensure-generic-function 'confidence-val :lambda-list '(m))
(cl:defmethod confidence-val ((m <objectDetection>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-msg:confidence-val is deprecated.  Use hoofdprogramma-msg:confidence instead.")
  (confidence m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <objectDetection>) ostream)
  "Serializes a message object of type '<objectDetection>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'object_type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'object_type))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'confidence))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <objectDetection>) istream)
  "Deserializes a message object of type '<objectDetection>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'object_type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'object_type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'confidence) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<objectDetection>)))
  "Returns string type for a message object of type '<objectDetection>"
  "hoofdprogramma/objectDetection")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'objectDetection)))
  "Returns string type for a message object of type 'objectDetection"
  "hoofdprogramma/objectDetection")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<objectDetection>)))
  "Returns md5sum for a message object of type '<objectDetection>"
  "51cf1d8d3850a43ca6b509aa1916ae48")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'objectDetection)))
  "Returns md5sum for a message object of type 'objectDetection"
  "51cf1d8d3850a43ca6b509aa1916ae48")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<objectDetection>)))
  "Returns full string definition for message of type '<objectDetection>"
  (cl:format cl:nil "string object_type~%geometry_msgs/Pose pose~%float32 confidence~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'objectDetection)))
  "Returns full string definition for message of type 'objectDetection"
  (cl:format cl:nil "string object_type~%geometry_msgs/Pose pose~%float32 confidence~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <objectDetection>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'object_type))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <objectDetection>))
  "Converts a ROS message object to a list"
  (cl:list 'objectDetection
    (cl:cons ':object_type (object_type msg))
    (cl:cons ':pose (pose msg))
    (cl:cons ':confidence (confidence msg))
))
