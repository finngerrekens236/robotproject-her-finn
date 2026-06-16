;; Auto-generated. Do not edit!


(when (boundp 'hoofdprogramma::ConveyorControl)
  (if (not (find-package "HOOFDPROGRAMMA"))
    (make-package "HOOFDPROGRAMMA"))
  (shadow 'ConveyorControl (find-package "HOOFDPROGRAMMA")))
(unless (find-package "HOOFDPROGRAMMA::CONVEYORCONTROL")
  (make-package "HOOFDPROGRAMMA::CONVEYORCONTROL"))
(unless (find-package "HOOFDPROGRAMMA::CONVEYORCONTROLREQUEST")
  (make-package "HOOFDPROGRAMMA::CONVEYORCONTROLREQUEST"))
(unless (find-package "HOOFDPROGRAMMA::CONVEYORCONTROLRESPONSE")
  (make-package "HOOFDPROGRAMMA::CONVEYORCONTROLRESPONSE"))

(in-package "ROS")





(defclass hoofdprogramma::ConveyorControlRequest
  :super ros::object
  :slots (_run ))

(defmethod hoofdprogramma::ConveyorControlRequest
  (:init
   (&key
    ((:run __run) nil)
    )
   (send-super :init)
   (setq _run __run)
   self)
  (:run
   (&optional __run)
   (if __run (setq _run __run)) _run)
  (:serialization-length
   ()
   (+
    ;; bool _run
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _run
       (if _run (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _run
     (setq _run (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass hoofdprogramma::ConveyorControlResponse
  :super ros::object
  :slots (_success _message _state ))

(defmethod hoofdprogramma::ConveyorControlResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    ((:state __state) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   (setq _state (string __state))
   self)
  (:success
   (&optional __success)
   (if __success (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ;; string _state
    4 (length _state)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;; string _state
       (write-long (length _state) s) (princ _state s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _state
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _state (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass hoofdprogramma::ConveyorControl
  :super ros::object
  :slots ())

(setf (get hoofdprogramma::ConveyorControl :md5sum-) "ab9233f15f98750719655c215d2e9e94")
(setf (get hoofdprogramma::ConveyorControl :datatype-) "hoofdprogramma/ConveyorControl")
(setf (get hoofdprogramma::ConveyorControl :request) hoofdprogramma::ConveyorControlRequest)
(setf (get hoofdprogramma::ConveyorControl :response) hoofdprogramma::ConveyorControlResponse)

(defmethod hoofdprogramma::ConveyorControlRequest
  (:response () (instance hoofdprogramma::ConveyorControlResponse :init)))

(setf (get hoofdprogramma::ConveyorControlRequest :md5sum-) "ab9233f15f98750719655c215d2e9e94")
(setf (get hoofdprogramma::ConveyorControlRequest :datatype-) "hoofdprogramma/ConveyorControlRequest")
(setf (get hoofdprogramma::ConveyorControlRequest :definition-)
      "bool run
---
bool success
string message
string state

")

(setf (get hoofdprogramma::ConveyorControlResponse :md5sum-) "ab9233f15f98750719655c215d2e9e94")
(setf (get hoofdprogramma::ConveyorControlResponse :datatype-) "hoofdprogramma/ConveyorControlResponse")
(setf (get hoofdprogramma::ConveyorControlResponse :definition-)
      "bool run
---
bool success
string message
string state

")



(provide :hoofdprogramma/ConveyorControl "ab9233f15f98750719655c215d2e9e94")


