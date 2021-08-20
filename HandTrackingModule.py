import time
import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self, image_mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.image_mode = image_mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.image_mode, self.max_hands, self.detection_confidence, self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def detect_hands(self, img, draw=True):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if draw:
            if self.results.multi_hand_landmarks:
                for handLandmarks in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    def get_landmarks(self, img, hand_no=0):

        landmarks = []
        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[hand_no]
            for lm_id, landmark in enumerate(hand_landmarks.landmark):
                height, width, channels = img.shape
                # c: landmark center
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                # print(id, cx, cy)
                # if id == 4:
                #     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                landmarks.append([lm_id, cx, cy])

        return landmarks


def main():
    previous_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while cap.isOpened():
        success, img = cap.read()
        if success:
            img = detector.detect_hands(img)
            landmarks = detector.get_landmarks(img)
            if len(landmarks) != 0:
                print(landmarks[4])
            current_time = time.time()
            fps = 1 / (current_time - previous_time)
            previous_time = current_time
            cv2.putText(img, text=str(int(fps)), org=(5, 60), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                        color=(144, 12, 63), thickness=3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
