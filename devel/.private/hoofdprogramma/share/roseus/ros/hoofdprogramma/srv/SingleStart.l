;; Auto-generated. Do not edit!


(when (boundp 'hoofdprogramma::SingleStart)
  (if (not (find-package "HOOFDPROGRAMMA"))
    (make-package "HOOFDPROGRAMMA"))
  (shadow 'SingleStart (find-package "HOOFDPROGRAMMA")))
(unless (find-package "HOOFDPROGRAMMA::SINGLESTART")
  (make-package "HOOFDPROGRAMMA::SINGLESTART"))
(unless (find-package "HOOFDPROGRAMMA::SINGLESTARTREQUEST")
  (make-package "HOOFDPROGRAMMA::SINGLESTARTREQUEST"))
(unless (find-package "HOOFDPROGRAMMA::SINGLESTARTRESPONSE")
  (make-package "HOOFDPROGRAMMA::SINGLESTARTRESPONSE"))

(in-package "ROS")





(defclass hoofdprogramma::SingleStartRequest
  :super ros::object
  :slots (_start ))

(defmethod hoofdprogramma::SingleStartRequest
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

(defclass hoofdprogramma::SingleStartResponse
  :super ros::object
  :slots (_success _message ))

(defmethod hoofdprogramma::SingleStartResponse
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

(defclass hoofdprogramma::SingleStart
  :super ros::object
  :slots ())

(setf (get hoofdprogramma::SingleStart :md5sum-) "570b7d04f9d3b17893f17c4fdcf5ca06")
(setf (get hoofdprogramma::SingleStart :datatype-) "hoofdprogramma/SingleStart")
(setf (get hoofdprogramma::SingleStart :request) hoofdprogramma::SingleStartRequest)
(setf (get hoofdprogramma::SingleStart :response) hoofdprogramma::SingleStartResponse)

(defmethod hoofdprogramma::SingleStartRequest
  (:response () (instance hoofdprogramma::SingleStartResponse :init)))

(setf (get hoofdprogramma::SingleStartRequest :md5sum-) "570b7d04f9d3b17893f17c4fdcf5ca06")
(setf (get hoofdprogramma::SingleStartRequest :datatype-) "hoofdprogramma/SingleStartRequest")
(setf (get hoofdprogramma::SingleStartRequest :definition-)
      "bool start
---
bool success
string message

")

(setf (get hoofdprogramma::SingleStartResponse :md5sum-) "570b7d04f9d3b17893f17c4fdcf5ca06")
(setf (get hoofdprogramma::SingleStartResponse :datatype-) "hoofdprogramma/SingleStartResponse")
(setf (get hoofdprogramma::SingleStartResponse :definition-)
      "bool start
---
bool success
string message

")



(provide :hoofdprogramma/SingleStart "570b7d04f9d3b17893f17c4fdcf5ca06")


