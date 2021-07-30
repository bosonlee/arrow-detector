;; Auto-generated. Do not edit!


(when (boundp 'test::detector)
  (if (not (find-package "TEST"))
    (make-package "TEST"))
  (shadow 'detector (find-package "TEST")))
(unless (find-package "TEST::DETECTOR")
  (make-package "TEST::DETECTOR"))

(in-package "ROS")
;;//! \htmlinclude detector.msg.html


(defclass test::detector
  :super ros::object
  :slots (_x _y _height _width _arrow ))

(defmethod test::detector
  (:init
   (&key
    ((:x __x) 0)
    ((:y __y) 0)
    ((:height __height) 0)
    ((:width __width) 0)
    ((:arrow __arrow) 0)
    )
   (send-super :init)
   (setq _x (round __x))
   (setq _y (round __y))
   (setq _height (round __height))
   (setq _width (round __width))
   (setq _arrow (round __arrow))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:height
   (&optional __height)
   (if __height (setq _height __height)) _height)
  (:width
   (&optional __width)
   (if __width (setq _width __width)) _width)
  (:arrow
   (&optional __arrow)
   (if __arrow (setq _arrow __arrow)) _arrow)
  (:serialization-length
   ()
   (+
    ;; int32 _x
    4
    ;; int32 _y
    4
    ;; int32 _height
    4
    ;; int32 _width
    4
    ;; int32 _arrow
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _x
       (write-long _x s)
     ;; int32 _y
       (write-long _y s)
     ;; int32 _height
       (write-long _height s)
     ;; int32 _width
       (write-long _width s)
     ;; int32 _arrow
       (write-long _arrow s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _x
     (setq _x (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _y
     (setq _y (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _height
     (setq _height (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _width
     (setq _width (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _arrow
     (setq _arrow (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get test::detector :md5sum-) "ee01ea2a195a728d9a98b72b946d52d6")
(setf (get test::detector :datatype-) "test/detector")
(setf (get test::detector :definition-)
      "int32 x
int32 y
int32 height
int32 width
int32 arrow

")



(provide :test/detector "ee01ea2a195a728d9a98b72b946d52d6")


