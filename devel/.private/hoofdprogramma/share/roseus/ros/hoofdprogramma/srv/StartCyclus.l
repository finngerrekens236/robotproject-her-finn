;; Auto-generated. Do not edit!


(when (boundp 'hoofdprogramma::StartCyclus)
  (if (not (find-package "HOOFDPROGRAMMA"))
    (make-package "HOOFDPROGRAMMA"))
  (shadow 'StartCyclus (find-package "HOOFDPROGRAMMA")))
(unless (find-package "HOOFDPROGRAMMA::STARTCYCLUS")
  (make-package "HOOFDPROGRAMMA::STARTCYCLUS"))
(unless (find-package "HOOFDPROGRAMMA::STARTCYCLUSREQUEST")
  (make-package "HOOFDPROGRAMMA::STARTCYCLUSREQUEST"))
(unless (find-package "HOOFDPROGRAMMA::STARTCYCLUSRESPONSE")
  (make-package "HOOFDPROGRAMMA::STARTCYCLUSRESPONSE"))

(in-package "ROS")





(defclass hoofdprogramma::StartCyclusRequest
  :super ros::object
  :slots (_start ))

(defmethod hoofdprogramma::StartCyclusRequest
  (:init
   (&key
    ((:start __start) nil)
    )
   (send-super :init)
   (setq _start __start)
   self)
  (:start
   (&optional __start)
   (if __start (setq _start __start)) _start)
  (:serialization-length
   ()
   (+
    ;; bool _start
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _start
       (if _start (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _start
     (setq _start (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass hoofdprogramma::StartCyclusResponse
  :super ros::object
  :slots (_success _message ))

(defmethod hoofdprogramma::StartCyclusResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional __success)
   (if __success (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass hoofdprogramma::StartCyclus
  :super ros::object
  :slots ())

(setf (get hoofdprogramma::StartCyclus :md5sum-) "570b7d04f9d3b17893f17c4fdcf5ca06")
(setf (get hoofdprogramma::StartCyclus :datatype-) "hoofdprogramma/StartCyclus")
(setf (get hoofdprogramma::StartCyclus :request) hoofdprogramma::StartCyclusRequest)
(setf (get hoofdprogramma::StartCyclus :response) hoofdprogramma::StartCyclusResponse)

(defmethod hoofdprogramma::StartCyclusRequest
  (:response () (instance hoofdprogramma::StartCyclusResponse :init)))

(setf (get hoofdprogramma::StartCyclusRequest :md5sum-) "570b7d04f9d3b17893f17c4fdcf5ca06")
(setf (get hoofdprogramma::StartCyclusRequest :datatype-) "hoofdprogramma/StartCyclusRequest")
(setf (get hoofdprogramma::StartCyclusRequest :definition-)
      "bool start
---
bool success
string message

")

(setf (get hoofdprogramma::StartCyclusResponse :md5sum-) "570b7d04f9d3b17893f17c4fdcf5ca06")
(setf (get hoofdprogramma::StartCyclusResponse :datatype-) "hoofdprogramma/StartCyclusResponse")
(setf (get hoofdprogramma::StartCyclusResponse :definition-)
      "bool start
---
bool success
string message

")



(provide :hoofdprogramma/StartCyclus "570b7d04f9d3b17893f17c4fdcf5ca06")


