import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandDetector:
    def __init__(self, model_path="hand_landmarker.task", cam_id=None):
        
        if cam_id is None:
            cam_id = find_working_camera()

        self.cap = cv2.VideoCapture(cam_id)

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.7,
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def get_hand_up(self, threshold=150):
        success, frame = self.cap.read()
        if not success:
            return False, None

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        timestamp = int(time.time() * 1000)
        result = self.detector.detect_for_video(mp_image, timestamp)

        hand_up = False
        hand_y = None

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            index_tip = hand[8]

            y = int(index_tip.y * h)
            hand_y = y

            if y < threshold:   # hand is raised
                hand_up = True

            # small visual dot for debugging
            cv2.circle(frame, 
                       (int(index_tip.x * w), y),
                       10, (0,255,0), -1)

        cv2.imshow("Hand Tracking", frame)
        cv2.waitKey(1)

        return hand_up, hand_y

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

def find_working_camera(max_cams=5):
    for i in range(max_cams):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            return i
    return 0 
