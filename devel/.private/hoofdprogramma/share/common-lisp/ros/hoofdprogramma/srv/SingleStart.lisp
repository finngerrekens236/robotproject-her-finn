; Auto-generated. Do not edit!


(cl:in-package hoofdprogramma-srv)


;//! \htmlinclude SingleStart-request.msg.html

(cl:defclass <SingleStart-request> (roslisp-msg-protocol:ros-message)
  ((start
    :reader start
    :initarg :start
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass SingleStart-request (<SingleStart-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SingleStart-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SingleStart-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<SingleStart-request> is deprecated: use hoofdprogramma-srv:SingleStart-request instead.")))

(cl:ensure-generic-function 'start-val :lambda-list '(m))
(cl:defmethod start-val ((m <SingleStart-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:start-val is deprecated.  Use hoofdprogramma-srv:start instead.")
  (start m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SingleStart-request>) ostream)
  "Serializes a message object of type '<SingleStart-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'start) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SingleStart-request>) istream)
  "Deserializes a message object of type '<SingleStart-request>"
    (cl:setf (cl:slot-value msg 'start) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SingleStart-request>)))
  "Returns string type for a service object of type '<SingleStart-request>"
  "hoofdprogramma/SingleStartRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SingleStart-request)))
  "Returns string type for a service object of type 'SingleStart-request"
  "hoofdprogramma/SingleStartRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SingleStart-request>)))
  "Returns md5sum for a message object of type '<SingleStart-request>"
  "570b7d04f9d3b17893f17c4fdcf5ca06")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SingleStart-request)))
  "Returns md5sum for a message object of type 'SingleStart-request"
  "570b7d04f9d3b17893f17c4fdcf5ca06")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SingleStart-request>)))
  "Returns full string definition for message of type '<SingleStart-request>"
  (cl:format cl:nil "bool start~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SingleStart-request)))
  "Returns full string definition for message of type 'SingleStart-request"
  (cl:format cl:nil "bool start~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SingleStart-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SingleStart-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SingleStart-request
    (cl:cons ':start (start msg))
))
;//! \htmlinclude SingleStart-response.msg.html

(cl:defclass <SingleStart-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass SingleStart-response (<SingleStart-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SingleStart-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SingleStart-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hoofdprogramma-srv:<SingleStart-response> is deprecated: use hoofdprogramma-srv:SingleStart-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <SingleStart-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:success-val is deprecated.  Use hoofdprogramma-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <SingleStart-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hoofdprogramma-srv:message-val is deprecated.  Use hoofdprogramma-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SingleStart-response>) ostream)
  "Serializes a message object of type '<SingleStart-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SingleStart-response>) istream)
  "Deserializes a message object of type '<SingleStart-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SingleStart-response>)))
  "Returns string type for a service object of type '<SingleStart-response>"
  "hoofdprogramma/SingleStartResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SingleStart-response)))
  "Returns string type for a service object of type 'SingleStart-response"
  "hoofdprogramma/SingleStartResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SingleStart-response>)))
  "Returns md5sum for a message object of type '<SingleStart-response>"
  "570b7d04f9d3b17893f17c4fdcf5ca06")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SingleStart-response)))
  "Returns md5sum for a message object of type 'SingleStart-response"
  "570b7d04f9d3b17893f17c4fdcf5ca06")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SingleStart-response>)))
  "Returns full string definition for message of type '<SingleStart-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SingleStart-response)))
  "Returns full string definition for message of type 'SingleStart-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SingleStart-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SingleStart-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SingleStart-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SingleStart)))
  'SingleStart-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SingleStart)))
  'SingleStart-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SingleStart)))
  "Returns string type for a service object of type '<SingleStart>"
  "hoofdprogramma/SingleStart")