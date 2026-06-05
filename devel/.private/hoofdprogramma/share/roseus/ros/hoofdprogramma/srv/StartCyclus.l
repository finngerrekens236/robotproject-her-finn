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
  :slots (_object_type _reset ))

(defmethod hoofdprogramma::StartCyclusRequest
  (:init
   (&key
    ((:object_type __object_type) "")
    ((:reset __reset) nil)
    )
   (send-super :init)
   (setq _object_type (string __object_type))
   (setq _reset __reset)
   self)
  (:object_type
   (&optional __object_type)
   (if __object_type (setq _object_type __object_type)) _object_type)
  (:reset
   (&optional __reset)
   (if __reset (setq _reset __reset)) _reset)
  (:serialization-length
   ()
   (+
    ;; string _object_type
    4 (length _object_type)
    ;; bool _reset
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _object_type
       (write-long (length _object_type) s) (princ _object_type s)
     ;; bool _reset
       (if _reset (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _object_type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _object_type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; bool _reset
     (setq _reset (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
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

(setf (get hoofdprogramma::StartCyclus :md5sum-) "51224950c96b81351ba7f238527c827f")
(setf (get hoofdprogramma::StartCyclus :datatype-) "hoofdprogramma/StartCyclus")
(setf (get hoofdprogramma::StartCyclus :request) hoofdprogramma::StartCyclusRequest)
(setf (get hoofdprogramma::StartCyclus :response) hoofdprogramma::StartCyclusResponse)

(defmethod hoofdprogramma::StartCyclusRequest
  (:response () (instance hoofdprogramma::StartCyclusResponse :init)))

(setf (get hoofdprogramma::StartCyclusRequest :md5sum-) "51224950c96b81351ba7f238527c827f")
(setf (get hoofdprogramma::StartCyclusRequest :datatype-) "hoofdprogramma/StartCyclusRequest")
(setf (get hoofdprogramma::StartCyclusRequest :definition-)
      "string object_type
bool reset
---
bool success
string message

")

(setf (get hoofdprogramma::StartCyclusResponse :md5sum-) "51224950c96b81351ba7f238527c827f")
(setf (get hoofdprogramma::StartCyclusResponse :datatype-) "hoofdprogramma/StartCyclusResponse")
(setf (get hoofdprogramma::StartCyclusResponse :definition-)
      "string object_type
bool reset
---
bool success
string message

")



(provide :hoofdprogramma/StartCyclus "51224950c96b81351ba7f238527c827f")


