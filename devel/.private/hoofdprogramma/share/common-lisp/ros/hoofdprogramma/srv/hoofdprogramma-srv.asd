
(cl:in-package :asdf)

(defsystem "hoofdprogramma-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "StartCyclus" :depends-on ("_package_StartCyclus"))
    (:file "_package_StartCyclus" :depends-on ("_package"))
  ))