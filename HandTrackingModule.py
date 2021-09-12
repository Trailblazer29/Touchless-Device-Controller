import time
import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self, image_mode=False, max_num_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.image_mode = image_mode
        self.max_num_hands = max_num_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.image_mode, self.max_num_hands, self.detection_confidence, self.tracking_confidence)
        self.drawing = mp.solutions.drawing_utils

    def detect_hands(self, img, draw=True):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if draw:
            if self.results.multi_hand_landmarks:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    self.drawing.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmarks(self, img, hand_no=0):

        landmarks = []
        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[hand_no]
            for lm_id, landmark in enumerate(hand_landmarks.landmark):
                height, width, channels = img.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height) # C: Landmark Center
                landmarks.append([lm_id, cx, cy])

        return landmarks


def main():
    previous_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while cap.isOpened():
        try:
            success, img = cap.read()
            if success:
                img = detector.detect_hands(img)
                landmarks = detector.get_landmarks(img)
                current_time = time.time()
                fps = 1 / (current_time - previous_time)
                previous_time = current_time
                cv2.putText(img, text=str(int(fps)), org=(5, 60), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                            color=(144, 12, 63), thickness=3)
                cv2.imshow("Camera", img)
                cv2.waitKey(1)

        except KeyboardInterrupt:
            continue
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
