; Auto-generated. Do not edit!


(cl:in-package hoofdprogramma-srv)


;//! \htmlinclude StartCyclus-request.msg.html

(cl:defclass <StartCyclus-request> (roslisp-msg-protocol:ros-message)
  ((object_type
    :reader object_type
    :initarg :object_type
    :type cl:string
    :initform "")
   (reset
    :reader reset
    :initarg :reset
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass StartCyclus-request (<StartCyclus-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StartCyclus-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StartCyclus-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<StartCyclus-request> is deprecated: use hoofdprogramma-srv:StartCyclus-request instead.")))

(cl:ensure-generic-function 'object_type-val :lambda-list '(m))
(cl:defmethod object_type-val ((m <StartCyclus-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:object_type-val is deprecated.  Use hoofdprogramma-srv:object_type instead.")
  (object_type m))

(cl:ensure-generic-function 'reset-val :lambda-list '(m))
(cl:defmethod reset-val ((m <StartCyclus-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:reset-val is deprecated.  Use hoofdprogramma-srv:reset instead.")
  (reset m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StartCyclus-request>) ostream)
  "Serializes a message object of type '<StartCyclus-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'object_type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'object_type))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'reset) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StartCyclus-request>) istream)
  "Deserializes a message object of type '<StartCyclus-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'object_type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'object_type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:slot-value msg 'reset) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StartCyclus-request>)))
  "Returns string type for a service object of type '<StartCyclus-request>"
  "hoofdprogramma/StartCyclusRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StartCyclus-request)))
  "Returns string type for a service object of type 'StartCyclus-request"
  "hoofdprogramma/StartCyclusRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StartCyclus-request>)))
  "Returns md5sum for a message object of type '<StartCyclus-request>"
  "51224950c96b81351ba7f238527c827f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StartCyclus-request)))
  "Returns md5sum for a message object of type 'StartCyclus-request"
  "51224950c96b81351ba7f238527c827f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StartCyclus-request>)))
  "Returns full string definition for message of type '<StartCyclus-request>"
  (cl:format cl:nil "string object_type~%bool reset~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StartCyclus-request)))
  "Returns full string definition for message of type 'StartCyclus-request"
  (cl:format cl:nil "string object_type~%bool reset~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StartCyclus-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'object_type))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StartCyclus-request>))
  "Converts a ROS message object to a list"
  (cl:list 'StartCyclus-request
    (cl:cons ':object_type (object_type msg))
    (cl:cons ':reset (reset msg))
))
;//! \htmlinclude StartCyclus-response.msg.html

(cl:defclass <StartCyclus-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform ""))
)

(cl:defclass StartCyclus-response (<StartCyclus-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StartCyclus-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StartCyclus-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<StartCyclus-response> is deprecated: use hoofdprogramma-srv:StartCyclus-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <StartCyclus-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:success-val is deprecated.  Use hoofdprogramma-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <StartCyclus-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:message-val is deprecated.  Use hoofdprogramma-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StartCyclus-response>) ostream)
  "Serializes a message object of type '<StartCyclus-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StartCyclus-response>) istream)
  "Deserializes a message object of type '<StartCyclus-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StartCyclus-response>)))
  "Returns string type for a service object of type '<StartCyclus-response>"
  "hoofdprogramma/StartCyclusResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StartCyclus-response)))
  "Returns string type for a service object of type 'StartCyclus-response"
  "hoofdprogramma/StartCyclusResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StartCyclus-response>)))
  "Returns md5sum for a message object of type '<StartCyclus-response>"
  "51224950c96b81351ba7f238527c827f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StartCyclus-response)))
  "Returns md5sum for a message object of type 'StartCyclus-response"
  "51224950c96b81351ba7f238527c827f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StartCyclus-response>)))
  "Returns full string definition for message of type '<StartCyclus-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StartCyclus-response)))
  "Returns full string definition for message of type 'StartCyclus-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StartCyclus-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StartCyclus-response>))
  "Converts a ROS message object to a list"
  (cl:list 'StartCyclus-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'StartCyclus)))
  'StartCyclus-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'StartCyclus)))
  'StartCyclus-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StartCyclus)))
  "Returns string type for a service object of type '<StartCyclus>"
  "hoofdprogramma/StartCyclus")