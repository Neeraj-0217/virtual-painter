import time
import cv2

from config import (
    CAMERA_INDEX,
    MIN_DET_CONF,
    MIN_TRACK_CONF,
    MAX_HANDS,
    DRAW_LANDMARKS,
    WINDOW_NAME,
    SWIPE_THRESHOLD,
    SWIPE_COOLDOWN
)
from hand_tracking.tracker import HandTracker
from drawing.canvas import Canvas
from drawing.tools import is_finger_up, get_fps

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Could not open camera")
        return
    
    tracker = HandTracker(
        max_hands=MAX_HANDS,
        min_det_conf=MIN_DET_CONF,
        min_track_conf=MIN_TRACK_CONF,
        draw_landmarks=DRAW_LANDMARKS
    )
    success, frame = cap.read()
    canvas = Canvas(frame.shape[1], frame.shape[0])

    prev_x, prev_y = 0, 0
    prev_point = None
    prev_swipe_x = None
    last_swipe_time = 0

    # Brush settings
    brush_thickness = 5

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Empty frame from camera.")
                break

            # Mirror for natural UX
            frame = cv2.flip(frame, 1)

            # Detect hands
            results = tracker.process(frame)

            # Draw landmarks if configured
            if DRAW_LANDMARKS:
                frame = tracker.annotate(frame, results)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                x, y = tracker.to_pixel(hand_landmarks, frame.shape, 8) # Index fingertip
                
                index_up = is_finger_up(hand_landmarks, 8, 6)
                middle_up = is_finger_up(hand_landmarks, 12, 10)
                all_up = all(is_finger_up(hand_landmarks, tip, tip-2) for tip in [4, 8, 12, 16, 20])

                # Extract wrist landmark
                wrist_x, wrist_y = tracker.to_pixel(hand_landmarks, frame.shape, 0)

                if index_up and not middle_up:  # Drawing mode
                    print("Drawing Mode")
                    if canvas.check_toolbar_selection(x, y):
                        prev_point = None
                    else:
                        if prev_point is None:  
                            prev_point = (x, y)
                        canvas.draw_line(prev_point, (x, y), thickness=brush_thickness)
                        prev_point = (x, y)
                elif index_up and middle_up and not all_up:    # Selection mode
                    print("Selection Mode")
                    prev_point = None
                    if canvas.check_toolbar_selection(x, y):
                        pass
                elif all_up:    # Erase Mode
                    print("Erase Mode")
                    if prev_point is None:
                        prev_point = (x, y)
                    canvas.erase(prev_point, (x, y), thickness=brush_thickness*10)
                    prev_point = (x, y)
                else:
                    prev_point = None
                    prev_swipe_x = None

                
            output = canvas.overlay_on(frame)                

            # FPS
            fps = get_fps()
            h, w, _ = output.shape
            cv2.putText(output, f"FPS: {fps:.1f}", (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow(WINDOW_NAME, output)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord('c'):
                canvas.reset()
            elif key in [ord('1'), ord('2'), ord('3'), ord('4')]:
                color_idx = int(chr(key)) - 1
            elif key == ord('+'):
                brush_thickness += 1
            elif key == ord('-') and brush_thickness > 1:
                brush_thickness -= 1
            elif key == ord('s'):
                canvas.save(f"drawing_{int(time.time())}.png")
    
    finally:
        tracker.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()