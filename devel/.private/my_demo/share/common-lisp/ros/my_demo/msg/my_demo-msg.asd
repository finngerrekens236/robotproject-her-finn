
(cl:in-package :asdf)

(defsystem "my_demo-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :actionlib_msgs-msg
               :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "PickPlaceAction" :depends-on ("_package_PickPlaceAction"))
    (:file "_package_PickPlaceAction" :depends-on ("_package"))
    (:file "PickPlaceActionFeedback" :depends-on ("_package_PickPlaceActionFeedback"))
    (:file "_package_PickPlaceActionFeedback" :depends-on ("_package"))
    (:file "PickPlaceActionGoal" :depends-on ("_package_PickPlaceActionGoal"))
    (:file "_package_PickPlaceActionGoal" :depends-on ("_package"))
    (:file "PickPlaceActionResult" :depends-on ("_package_PickPlaceActionResult"))
    (:file "_package_PickPlaceActionResult" :depends-on ("_package"))
    (:file "PickPlaceFeedback" :depends-on ("_package_PickPlaceFeedback"))
    (:file "_package_PickPlaceFeedback" :depends-on ("_package"))
    (:file "PickPlaceGoal" :depends-on ("_package_PickPlaceGoal"))
    (:file "_package_PickPlaceGoal" :depends-on ("_package"))
    (:file "PickPlaceResult" :depends-on ("_package_PickPlaceResult"))
    (:file "_package_PickPlaceResult" :depends-on ("_package"))
  ))