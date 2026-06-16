; Auto-generated. Do not edit!


(cl:in-package hoofdprogramma-srv)


;//! \htmlinclude ConveyorControl-request.msg.html

(cl:defclass <ConveyorControl-request> (roslisp-msg-protocol:ros-message)
  ((run
    :reader run
    :initarg :run
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass ConveyorControl-request (<ConveyorControl-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ConveyorControl-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ConveyorControl-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<ConveyorControl-request> is deprecated: use hoofdprogramma-srv:ConveyorControl-request instead.")))

(cl:ensure-generic-function 'run-val :lambda-list '(m))
(cl:defmethod run-val ((m <ConveyorControl-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:run-val is deprecated.  Use hoofdprogramma-srv:run instead.")
  (run m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ConveyorControl-request>) ostream)
  "Serializes a message object of type '<ConveyorControl-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'run) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ConveyorControl-request>) istream)
  "Deserializes a message object of type '<ConveyorControl-request>"
    (cl:setf (cl:slot-value msg 'run) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ConveyorControl-request>)))
  "Returns string type for a service object of type '<ConveyorControl-request>"
  "hoofdprogramma/ConveyorControlRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ConveyorControl-request)))
  "Returns string type for a service object of type 'ConveyorControl-request"
  "hoofdprogramma/ConveyorControlRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ConveyorControl-request>)))
  "Returns md5sum for a message object of type '<ConveyorControl-request>"
  "ab9233f15f98750719655c215d2e9e94")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ConveyorControl-request)))
  "Returns md5sum for a message object of type 'ConveyorControl-request"
  "ab9233f15f98750719655c215d2e9e94")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ConveyorControl-request>)))
  "Returns full string definition for message of type '<ConveyorControl-request>"
  (cl:format cl:nil "bool run~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ConveyorControl-request)))
  "Returns full string definition for message of type 'ConveyorControl-request"
  (cl:format cl:nil "bool run~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ConveyorControl-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ConveyorControl-request>))
  "Converts a ROS message object to a list"
  (cl:list 'ConveyorControl-request
    (cl:cons ':run (run msg))
))
;//! \htmlinclude ConveyorControl-response.msg.html

(cl:defclass <ConveyorControl-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform "")
   (state
    :reader state
    :initarg :state
    :type cl:string
    :initform ""))
)

(cl:defclass ConveyorControl-response (<ConveyorControl-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ConveyorControl-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ConveyorControl-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<ConveyorControl-response> is deprecated: use hoofdprogramma-srv:ConveyorControl-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <ConveyorControl-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:success-val is deprecated.  Use hoofdprogramma-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <ConveyorControl-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:message-val is deprecated.  Use hoofdprogramma-srv:message instead.")
  (message m))

(cl:ensure-generic-function 'state-val :lambda-list '(m))
(cl:defmethod state-val ((m <ConveyorControl-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:state-val is deprecated.  Use hoofdprogramma-srv:state instead.")
  (state m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ConveyorControl-response>) ostream)
  "Serializes a message object of type '<ConveyorControl-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'state))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'state))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ConveyorControl-response>) istream)
  "Deserializes a message object of type '<ConveyorControl-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'state) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'state) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ConveyorControl-response>)))
  "Returns string type for a service object of type '<ConveyorControl-response>"
  "hoofdprogramma/ConveyorControlResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ConveyorControl-response)))
  "Returns string type for a service object of type 'ConveyorControl-response"
  "hoofdprogramma/ConveyorControlResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ConveyorControl-response>)))
  "Returns md5sum for a message object of type '<ConveyorControl-response>"
  "ab9233f15f98750719655c215d2e9e94")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ConveyorControl-response)))
  "Returns md5sum for a message object of type 'ConveyorControl-response"
  "ab9233f15f98750719655c215d2e9e94")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ConveyorControl-response>)))
  "Returns full string definition for message of type '<ConveyorControl-response>"
  (cl:format cl:nil "bool success~%string message~%string state~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ConveyorControl-response)))
  "Returns full string definition for message of type 'ConveyorControl-response"
  (cl:format cl:nil "bool success~%string message~%string state~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ConveyorControl-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
     4 (cl:length (cl:slot-value msg 'state))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ConveyorControl-response>))
  "Converts a ROS message object to a list"
  (cl:list 'ConveyorControl-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
    (cl:cons ':state (state msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'ConveyorControl)))
  'ConveyorControl-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'ConveyorControl)))
  'ConveyorControl-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ConveyorControl)))
  "Returns string type for a service object of type '<ConveyorControl>"
  "hoofdprogramma/ConveyorControl")