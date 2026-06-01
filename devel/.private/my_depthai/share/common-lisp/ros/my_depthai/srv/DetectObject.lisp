; Auto-generated. Do not edit!


(cl:in-package my_depthai-srv)


;//! \htmlinclude DetectObject-request.msg.html

(cl:defclass <DetectObject-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass DetectObject-request (<DetectObject-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <DetectObject-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'DetectObject-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name my_depthai-srv:<DetectObject-request> is deprecated: use my_depthai-srv:DetectObject-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <DetectObject-request>) ostream)
  "Serializes a message object of type '<DetectObject-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <DetectObject-request>) istream)
  "Deserializes a message object of type '<DetectObject-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<DetectObject-request>)))
  "Returns string type for a service object of type '<DetectObject-request>"
  "my_depthai/DetectObjectRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'DetectObject-request)))
  "Returns string type for a service object of type 'DetectObject-request"
  "my_depthai/DetectObjectRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<DetectObject-request>)))
  "Returns md5sum for a message object of type '<DetectObject-request>"
  "b95455854c5d28811eaccdf7054b9b90")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'DetectObject-request)))
  "Returns md5sum for a message object of type 'DetectObject-request"
  "b95455854c5d28811eaccdf7054b9b90")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<DetectObject-request>)))
  "Returns full string definition for message of type '<DetectObject-request>"
  (cl:format cl:nil "# Request: leeg — gewoon triggeren is genoeg~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'DetectObject-request)))
  "Returns full string definition for message of type 'DetectObject-request"
  (cl:format cl:nil "# Request: leeg — gewoon triggeren is genoeg~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <DetectObject-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <DetectObject-request>))
  "Converts a ROS message object to a list"
  (cl:list 'DetectObject-request
))
;//! \htmlinclude DetectObject-response.msg.html

(cl:defclass <DetectObject-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (object_class
    :reader object_class
    :initarg :object_class
    :type cl:string
    :initform "")
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform "")
   (pick_pose
    :reader pick_pose
    :initarg :pick_pose
    :type geometry_msgs-msg:PoseStamped
    :initform (cl:make-instance 'geometry_msgs-msg:PoseStamped)))
)

(cl:defclass DetectObject-response (<DetectObject-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <DetectObject-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'DetectObject-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name my_depthai-srv:<DetectObject-response> is deprecated: use my_depthai-srv:DetectObject-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <DetectObject-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_depthai-srv:success-val is deprecated.  Use my_depthai-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'object_class-val :lambda-list '(m))
(cl:defmethod object_class-val ((m <DetectObject-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_depthai-srv:object_class-val is deprecated.  Use my_depthai-srv:object_class instead.")
  (object_class m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <DetectObject-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_depthai-srv:message-val is deprecated.  Use my_depthai-srv:message instead.")
  (message m))

(cl:ensure-generic-function 'pick_pose-val :lambda-list '(m))
(cl:defmethod pick_pose-val ((m <DetectObject-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_depthai-srv:pick_pose-val is deprecated.  Use my_depthai-srv:pick_pose instead.")
  (pick_pose m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <DetectObject-response>) ostream)
  "Serializes a message object of type '<DetectObject-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'object_class))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'object_class))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pick_pose) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <DetectObject-response>) istream)
  "Deserializes a message object of type '<DetectObject-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'object_class) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'object_class) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pick_pose) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<DetectObject-response>)))
  "Returns string type for a service object of type '<DetectObject-response>"
  "my_depthai/DetectObjectResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'DetectObject-response)))
  "Returns string type for a service object of type 'DetectObject-response"
  "my_depthai/DetectObjectResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<DetectObject-response>)))
  "Returns md5sum for a message object of type '<DetectObject-response>"
  "b95455854c5d28811eaccdf7054b9b90")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'DetectObject-response)))
  "Returns md5sum for a message object of type 'DetectObject-response"
  "b95455854c5d28811eaccdf7054b9b90")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<DetectObject-response>)))
  "Returns full string definition for message of type '<DetectObject-response>"
  (cl:format cl:nil "# Response~%bool success~%string object_class~%string message~%geometry_msgs/PoseStamped pick_pose~%~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'DetectObject-response)))
  "Returns full string definition for message of type 'DetectObject-response"
  (cl:format cl:nil "# Response~%bool success~%string object_class~%string message~%geometry_msgs/PoseStamped pick_pose~%~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <DetectObject-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'object_class))
     4 (cl:length (cl:slot-value msg 'message))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pick_pose))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <DetectObject-response>))
  "Converts a ROS message object to a list"
  (cl:list 'DetectObject-response
    (cl:cons ':success (success msg))
    (cl:cons ':object_class (object_class msg))
    (cl:cons ':message (message msg))
    (cl:cons ':pick_pose (pick_pose msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'DetectObject)))
  'DetectObject-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'DetectObject)))
  'DetectObject-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'DetectObject)))
  "Returns string type for a service object of type '<DetectObject>"
  "my_depthai/DetectObject")