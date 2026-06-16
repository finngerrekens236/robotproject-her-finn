
(cl:in-package :asdf)

(defsystem "hoofdprogramma-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ConveyorControl" :depends-on ("_package_ConveyorControl"))
    (:file "_package_ConveyorControl" :depends-on ("_package"))
    (:file "ResetCyclus" :depends-on ("_package_ResetCyclus"))
    (:file "_package_ResetCyclus" :depends-on ("_package"))
    (:file "SingleStart" :depends-on ("_package_SingleStart"))
    (:file "_package_SingleStart" :depends-on ("_package"))
    (:file "StartCyclus" :depends-on ("_package_StartCyclus"))
    (:file "_package_StartCyclus" :depends-on ("_package"))
    (:file "StopCyclus" :depends-on ("_package_StopCyclus"))
    (:file "_package_StopCyclus" :depends-on ("_package"))
  ))