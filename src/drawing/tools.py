import time

_prev_time = time.time()

def is_finger_up(hand_landmarks, finger_tip_index, finger_pip_index):
    return hand_landmarks.landmark[finger_tip_index].y < hand_landmarks.landmark[finger_pip_index].y

def get_fps():
    global _prev_time
    now = time.time()
    fps = 1.0/max(1e-6, (now - _prev_time))
    _prev_time = now
    return fps
