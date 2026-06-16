;; Auto-generated. Do not edit!


(when (boundp 'hoofdprogramma::StopCyclus)
  (if (not (find-package "HOOFDPROGRAMMA"))
    (make-package "HOOFDPROGRAMMA"))
  (shadow 'StopCyclus (find-package "HOOFDPROGRAMMA")))
(unless (find-package "HOOFDPROGRAMMA::STOPCYCLUS")
  (make-package "HOOFDPROGRAMMA::STOPCYCLUS"))
(unless (find-package "HOOFDPROGRAMMA::STOPCYCLUSREQUEST")
  (make-package "HOOFDPROGRAMMA::STOPCYCLUSREQUEST"))
(unless (find-package "HOOFDPROGRAMMA::STOPCYCLUSRESPONSE")
  (make-package "HOOFDPROGRAMMA::STOPCYCLUSRESPONSE"))

(in-package "ROS")





(defclass hoofdprogramma::StopCyclusRequest
  :super ros::object
  :slots (_stop ))

(defmethod hoofdprogramma::StopCyclusRequest
  (:init
   (&key
    ((:stop __stop) nil)
    )
   (send-super :init)
   (setq _stop __stop)
   self)
  (:stop
   (&optional __stop)
   (if __stop (setq _stop __stop)) _stop)
  (:serialization-length
   ()
   (+
    ;; bool _stop
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _stop
       (if _stop (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _stop
     (setq _stop (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass hoofdprogramma::StopCyclusResponse
  :super ros::object
  :slots (_success _message ))

(defmethod hoofdprogramma::StopCyclusResponse
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

(defclass hoofdprogramma::StopCyclus
  :super ros::object
  :slots ())

(setf (get hoofdprogramma::StopCyclus :md5sum-) "7d3aaec1ad97cf89d115490df578ba5b")
(setf (get hoofdprogramma::StopCyclus :datatype-) "hoofdprogramma/StopCyclus")
(setf (get hoofdprogramma::StopCyclus :request) hoofdprogramma::StopCyclusRequest)
(setf (get hoofdprogramma::StopCyclus :response) hoofdprogramma::StopCyclusResponse)

(defmethod hoofdprogramma::StopCyclusRequest
  (:response () (instance hoofdprogramma::StopCyclusResponse :init)))

(setf (get hoofdprogramma::StopCyclusRequest :md5sum-) "7d3aaec1ad97cf89d115490df578ba5b")
(setf (get hoofdprogramma::StopCyclusRequest :datatype-) "hoofdprogramma/StopCyclusRequest")
(setf (get hoofdprogramma::StopCyclusRequest :definition-)
      "bool stop
---
bool success
string message

")

(setf (get hoofdprogramma::StopCyclusResponse :md5sum-) "7d3aaec1ad97cf89d115490df578ba5b")
(setf (get hoofdprogramma::StopCyclusResponse :datatype-) "hoofdprogramma/StopCyclusResponse")
(setf (get hoofdprogramma::StopCyclusResponse :definition-)
      "bool stop
---
bool success
string message

")



(provide :hoofdprogramma/StopCyclus "7d3aaec1ad97cf89d115490df578ba5b")


