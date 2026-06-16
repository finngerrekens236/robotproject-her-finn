; Auto-generated. Do not edit!


(cl:in-package hoofdprogramma-srv)


;//! \htmlinclude ResetCyclus-request.msg.html

(cl:defclass <ResetCyclus-request> (roslisp-msg-protocol:ros-message)
  ((reset
    :reader reset
    :initarg :reset
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass ResetCyclus-request (<ResetCyclus-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ResetCyclus-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ResetCyclus-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<ResetCyclus-request> is deprecated: use hoofdprogramma-srv:ResetCyclus-request instead.")))

(cl:ensure-generic-function 'reset-val :lambda-list '(m))
(cl:defmethod reset-val ((m <ResetCyclus-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:reset-val is deprecated.  Use hoofdprogramma-srv:reset instead.")
  (reset m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ResetCyclus-request>) ostream)
  "Serializes a message object of type '<ResetCyclus-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'reset) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ResetCyclus-request>) istream)
  "Deserializes a message object of type '<ResetCyclus-request>"
    (cl:setf (cl:slot-value msg 'reset) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ResetCyclus-request>)))
  "Returns string type for a service object of type '<ResetCyclus-request>"
  "hoofdprogramma/ResetCyclusRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ResetCyclus-request)))
  "Returns string type for a service object of type 'ResetCyclus-request"
  "hoofdprogramma/ResetCyclusRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ResetCyclus-request>)))
  "Returns md5sum for a message object of type '<ResetCyclus-request>"
  "51cbeac084f3f5882dc2b7d6b3318d43")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ResetCyclus-request)))
  "Returns md5sum for a message object of type 'ResetCyclus-request"
  "51cbeac084f3f5882dc2b7d6b3318d43")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ResetCyclus-request>)))
  "Returns full string definition for message of type '<ResetCyclus-request>"
  (cl:format cl:nil "bool reset~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ResetCyclus-request)))
  "Returns full string definition for message of type 'ResetCyclus-request"
  (cl:format cl:nil "bool reset~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ResetCyclus-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ResetCyclus-request>))
  "Converts a ROS message object to a list"
  (cl:list 'ResetCyclus-request
    (cl:cons ':reset (reset msg))
))
;//! \htmlinclude ResetCyclus-response.msg.html

(cl:defclass <ResetCyclus-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass ResetCyclus-response (<ResetCyclus-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ResetCyclus-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ResetCyclus-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<ResetCyclus-response> is deprecated: use hoofdprogramma-srv:ResetCyclus-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <ResetCyclus-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:success-val is deprecated.  Use hoofdprogramma-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <ResetCyclus-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:message-val is deprecated.  Use hoofdprogramma-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ResetCyclus-response>) ostream)
  "Serializes a message object of type '<ResetCyclus-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ResetCyclus-response>) istream)
  "Deserializes a message object of type '<ResetCyclus-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ResetCyclus-response>)))
  "Returns string type for a service object of type '<ResetCyclus-response>"
  "hoofdprogramma/ResetCyclusResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ResetCyclus-response)))
  "Returns string type for a service object of type 'ResetCyclus-response"
  "hoofdprogramma/ResetCyclusResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ResetCyclus-response>)))
  "Returns md5sum for a message object of type '<ResetCyclus-response>"
  "51cbeac084f3f5882dc2b7d6b3318d43")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ResetCyclus-response)))
  "Returns md5sum for a message object of type 'ResetCyclus-response"
  "51cbeac084f3f5882dc2b7d6b3318d43")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ResetCyclus-response>)))
  "Returns full string definition for message of type '<ResetCyclus-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ResetCyclus-response)))
  "Returns full string definition for message of type 'ResetCyclus-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ResetCyclus-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ResetCyclus-response>))
  "Converts a ROS message object to a list"
  (cl:list 'ResetCyclus-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'ResetCyclus)))
  'ResetCyclus-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'ResetCyclus)))
  'ResetCyclus-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ResetCyclus)))
  "Returns string type for a service object of type '<ResetCyclus>"
  "hoofdprogramma/ResetCyclus")