import cv2
import time
import HandTrackingModule as htm
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

video_capture = cv2.VideoCapture(0)

video_capture.set(3, 1200)  # 3 & 4 are the property IDs for capture width and height, respectively
video_capture.set(4, 2800)

previous_time = 0

hand_detector = htm.HandDetector()

# Connect to device speakers
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()[:2]

while True:
    try:
        success, img = video_capture.read()
        if success:
            img = hand_detector.detect_hands(img)
            landmarks = hand_detector.get_landmarks(img)
            if len(landmarks) != 0:
                # Thumb tip and index tip positions
                thumb_x, thumb_y = landmarks[4][1], landmarks[4][2]
                index_x, index_y = landmarks[8][1], landmarks[8][2]
                line_center_x, line_center_y = (thumb_x + index_x) // 2, (thumb_y + index_y) // 2
                cv2.circle(img, center=(line_center_x, line_center_y), radius=15, color=(0, 255, 0),
                           thickness=cv2.FILLED)
                cv2.circle(img, center=(thumb_x, thumb_y), radius=15, color=(0, 255, 0), thickness=cv2.FILLED)
                cv2.circle(img, center=(index_x, index_y), radius=15, color=(255, 0, 255), thickness=cv2.FILLED)
                cv2.line(img, pt1=(thumb_x, thumb_y), pt2=(index_x, index_y), color=(0, 0, 0), thickness=3)

                distance = math.hypot(thumb_x-index_x, thumb_y-index_y)  # Distance between thumb tip and index tip...

                min_distance = 40   # Distance when thumb and index tips touch
                max_distance = 350  # Max distance depends on hand size and distance to camera

                # Convert distance between fingers to volume range [-65, 0]
                vol = np.interp(distance, [min_distance, max_distance], volume_range)

                # Set new volume based on finger distance
                volume.SetMasterVolumeLevel(vol, None)

            current_time = time.time()
            fps = 1 / (current_time - previous_time)
            previous_time = current_time
            cv2.putText(img, text=str(int(fps))+" FPS", org=(5, 60), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                        color=(144, 12, 63), thickness=3)

            cv2.imshow("Camera", img)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        continue
