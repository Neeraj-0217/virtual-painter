import cv2
import mediapipe as mp

class HandTracker:
    """
    Wraper around MediaPipe Hands for clean usage.

    Methods:
        process(frame_bgr) -> results
        annotate(frame_bgr, results) -> frame_bgr
        to_pixel(hand_landmarks, image_shape, landmark_index) -> (x, y)
        close()
    """

    def __init__(self, max_hands: int = 1, min_det_conf: float = 0.7,  min_track_conf: float = 0.5, draw_landmarks: bool = True):
        self.draw_landmarks = draw_landmarks
        self._mp_hands = mp.solutions.hands
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_styles = mp.solutions.drawing_styles

        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            model_complexity=1,
            min_detection_confidence=min_det_conf,
            min_tracking_confidence=min_track_conf,
        )

    def process(self, frame_bgr):
        # MediaPipe expects RGB and prefers non-writeable for perf
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self._hands.process(rgb)
        rgb.flags.writeable = True
        return results
    
    def annotate(self, frame_bgr, results):
        if not results or not results.multi_hand_landmarks:
            return frame_bgr
        for hand_landmarks in results.multi_hand_landmarks:
            self._mp_drawing.draw_landmarks(
                frame_bgr,
                hand_landmarks,
                self._mp_hands.HAND_CONNECTIONS,
                self._mp_styles.get_default_hand_landmarks_style(),
                self._mp_styles.get_default_hand_connections_style(),
            )
        return frame_bgr
    
    @staticmethod
    def to_pixel(hand_landmarks, image_shape, landmark_index: int):
        h, w = image_shape[:2]
        lm = hand_landmarks.landmark[landmark_index]
        return int(lm.x * w), int(lm.y * h)
    
    def close(self):
        self._hands.close()


    
