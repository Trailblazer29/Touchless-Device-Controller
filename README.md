# Gesture Desktop Controller

As a Gesture Recognition application, this project aims at simulating a completely touchless device (i.e., only a camera and a hand are required to control it). 

* To start with, we have to detect the hand, and get its position and landmarks. This task will be done by a [Hand Tracking Module](https://github.com/Trailblazer29/Gesture-Desktop-Controller/blob/main/HandTrackingModule.py) that detects hands' landmarks (illustrated in the below figure) with their respective coordinates, using [MediaPipe](https://mediapipe.dev/). This module can be solicited in many Computer Vision tasks that require hand tracking.

![Hand Landmarks](hand_landmarks.png)

* The second functionlity of this project is to adjust the volume of the device (increase, decrease, mute and unmute sound) using the device's camera (distance [Volume Controller](https://github.com/Trailblazer29/Gesture-Desktop-Controller/blob/main/volume_control.py)). 

*More functionalities will be added soon...*
