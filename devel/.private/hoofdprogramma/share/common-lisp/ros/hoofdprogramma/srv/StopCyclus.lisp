; Auto-generated. Do not edit!


(cl:in-package hoofdprogramma-srv)


;//! \htmlinclude StopCyclus-request.msg.html

(cl:defclass <StopCyclus-request> (roslisp-msg-protocol:ros-message)
  ((stop
    :reader stop
    :initarg :stop
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass StopCyclus-request (<StopCyclus-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StopCyclus-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StopCyclus-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<StopCyclus-request> is deprecated: use hoofdprogramma-srv:StopCyclus-request instead.")))

(cl:ensure-generic-function 'stop-val :lambda-list '(m))
(cl:defmethod stop-val ((m <StopCyclus-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:stop-val is deprecated.  Use hoofdprogramma-srv:stop instead.")
  (stop m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StopCyclus-request>) ostream)
  "Serializes a message object of type '<StopCyclus-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'stop) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StopCyclus-request>) istream)
  "Deserializes a message object of type '<StopCyclus-request>"
    (cl:setf (cl:slot-value msg 'stop) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StopCyclus-request>)))
  "Returns string type for a service object of type '<StopCyclus-request>"
  "hoofdprogramma/StopCyclusRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StopCyclus-request)))
  "Returns string type for a service object of type 'StopCyclus-request"
  "hoofdprogramma/StopCyclusRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StopCyclus-request>)))
  "Returns md5sum for a message object of type '<StopCyclus-request>"
  "7d3aaec1ad97cf89d115490df578ba5b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StopCyclus-request)))
  "Returns md5sum for a message object of type 'StopCyclus-request"
  "7d3aaec1ad97cf89d115490df578ba5b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StopCyclus-request>)))
  "Returns full string definition for message of type '<StopCyclus-request>"
  (cl:format cl:nil "bool stop~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StopCyclus-request)))
  "Returns full string definition for message of type 'StopCyclus-request"
  (cl:format cl:nil "bool stop~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StopCyclus-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StopCyclus-request>))
  "Converts a ROS message object to a list"
  (cl:list 'StopCyclus-request
    (cl:cons ':stop (stop msg))
))
;//! \htmlinclude StopCyclus-response.msg.html

(cl:defclass <StopCyclus-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass StopCyclus-response (<StopCyclus-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StopCyclus-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StopCyclus-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<StopCyclus-response> is deprecated: use hoofdprogramma-srv:StopCyclus-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <StopCyclus-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:success-val is deprecated.  Use hoofdprogramma-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <StopCyclus-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:message-val is deprecated.  Use hoofdprogramma-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StopCyclus-response>) ostream)
  "Serializes a message object of type '<StopCyclus-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StopCyclus-response>) istream)
  "Deserializes a message object of type '<StopCyclus-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StopCyclus-response>)))
  "Returns string type for a service object of type '<StopCyclus-response>"
  "hoofdprogramma/StopCyclusResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StopCyclus-response)))
  "Returns string type for a service object of type 'StopCyclus-response"
  "hoofdprogramma/StopCyclusResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StopCyclus-response>)))
  "Returns md5sum for a message object of type '<StopCyclus-response>"
  "7d3aaec1ad97cf89d115490df578ba5b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StopCyclus-response)))
  "Returns md5sum for a message object of type 'StopCyclus-response"
  "7d3aaec1ad97cf89d115490df578ba5b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StopCyclus-response>)))
  "Returns full string definition for message of type '<StopCyclus-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StopCyclus-response)))
  "Returns full string definition for message of type 'StopCyclus-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StopCyclus-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StopCyclus-response>))
  "Converts a ROS message object to a list"
  (cl:list 'StopCyclus-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'StopCyclus)))
  'StopCyclus-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'StopCyclus)))
  'StopCyclus-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StopCyclus)))
  "Returns string type for a service object of type '<StopCyclus>"
  "hoofdprogramma/StopCyclus")