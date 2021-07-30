
(cl:in-package :asdf)

(defsystem "test-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "detector" :depends-on ("_package_detector"))
    (:file "_package_detector" :depends-on ("_package"))
  ))