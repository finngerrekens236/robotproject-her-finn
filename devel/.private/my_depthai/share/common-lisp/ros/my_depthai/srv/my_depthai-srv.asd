
(cl:in-package :asdf)

(defsystem "my_depthai-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "DetectObject" :depends-on ("_package_DetectObject"))
    (:file "_package_DetectObject" :depends-on ("_package"))
  ))