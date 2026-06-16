;; Auto-generated. Do not edit!


(when (boundp 'hoofdprogramma::ResetCyclus)
  (if (not (find-package "HOOFDPROGRAMMA"))
    (make-package "HOOFDPROGRAMMA"))
  (shadow 'ResetCyclus (find-package "HOOFDPROGRAMMA")))
(unless (find-package "HOOFDPROGRAMMA::RESETCYCLUS")
  (make-package "HOOFDPROGRAMMA::RESETCYCLUS"))
(unless (find-package "HOOFDPROGRAMMA::RESETCYCLUSREQUEST")
  (make-package "HOOFDPROGRAMMA::RESETCYCLUSREQUEST"))
(unless (find-package "HOOFDPROGRAMMA::RESETCYCLUSRESPONSE")
  (make-package "HOOFDPROGRAMMA::RESETCYCLUSRESPONSE"))

(in-package "ROS")





(defclass hoofdprogramma::ResetCyclusRequest
  :super ros::object
  :slots (_reset ))

(defmethod hoofdprogramma::ResetCyclusRequest
  (:init
   (&key
    ((:reset __reset) nil)
    )
   (send-super :init)
   (setq _reset __reset)
   self)
  (:reset
   (&optional __reset)
   (if __reset (setq _reset __reset)) _reset)
  (:serialization-length
   ()
   (+
    ;; bool _reset
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _reset
       (if _reset (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _reset
     (setq _reset (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass hoofdprogramma::ResetCyclusResponse
  :super ros::object
  :slots (_success _message ))

(defmethod hoofdprogramma::ResetCyclusResponse
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

(defclass hoofdprogramma::ResetCyclus
  :super ros::object
  :slots ())

(setf (get hoofdprogramma::ResetCyclus :md5sum-) "51cbeac084f3f5882dc2b7d6b3318d43")
(setf (get hoofdprogramma::ResetCyclus :datatype-) "hoofdprogramma/ResetCyclus")
(setf (get hoofdprogramma::ResetCyclus :request) hoofdprogramma::ResetCyclusRequest)
(setf (get hoofdprogramma::ResetCyclus :response) hoofdprogramma::ResetCyclusResponse)

(defmethod hoofdprogramma::ResetCyclusRequest
  (:response () (instance hoofdprogramma::ResetCyclusResponse :init)))

(setf (get hoofdprogramma::ResetCyclusRequest :md5sum-) "51cbeac084f3f5882dc2b7d6b3318d43")
(setf (get hoofdprogramma::ResetCyclusRequest :datatype-) "hoofdprogramma/ResetCyclusRequest")
(setf (get hoofdprogramma::ResetCyclusRequest :definition-)
      "bool reset
---
bool success
string message

")

(setf (get hoofdprogramma::ResetCyclusResponse :md5sum-) "51cbeac084f3f5882dc2b7d6b3318d43")
(setf (get hoofdprogramma::ResetCyclusResponse :datatype-) "hoofdprogramma/ResetCyclusResponse")
(setf (get hoofdprogramma::ResetCyclusResponse :definition-)
      "bool reset
---
bool success
string message

")



(provide :hoofdprogramma/ResetCyclus "51cbeac084f3f5882dc2b7d6b3318d43")


