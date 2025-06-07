import cv2
import time
from utils import distance, is_finger_extended, is_thumb_extended
from actions import map_gesture_to_action
from gesture_controller import GestureController

def recognize_gesture(landmarks, hand_label, frame_width):
    if not landmarks or len(landmarks) < 21:
        return None

    tips = {'thumb': 4, 'index': 8, 'middle': 12, 'ring': 16, 'pinky': 20}
    pips = {'thumb': 3, 'index': 6, 'middle': 10, 'ring': 14, 'pinky': 18}

    finger_extended = {}
    for finger in ['index', 'middle', 'ring', 'pinky']:
        finger_extended[finger] = is_finger_extended(landmarks, tips[finger], pips[finger], hand_label)

    thumb_extended = is_thumb_extended(landmarks, tips['thumb'], pips['thumb'], hand_label)
    dist_index_middle = distance(landmarks[tips['index']], landmarks[tips['middle']])

    thumb_tip_y = landmarks[tips['thumb']][1]
    thumb_base_y = landmarks[pips['thumb']][1]
    thumb_is_down = thumb_tip_y > thumb_base_y

    # Gesture detection
    if all([thumb_extended] + list(finger_extended.values())):
        return "PALM"  # Right: Accelerate (W)
    if not any([thumb_extended] + list(finger_extended.values())):
        return "FIST"  # Right: E-brake (Space)
    if (finger_extended['index'] and finger_extended['middle'] and 
        not finger_extended['ring'] and not finger_extended['pinky'] and
        not thumb_extended and dist_index_middle > 0.05):  # Relaxed threshold
        return "PEACE"  # Right: Reverse (S)
    if landmarks[tips['index']][0] < 0.4:  # Left: Steer Left (A)
        return "SWIPE_LEFT"
    if landmarks[tips['index']][0] > 0.6:  # Left: Steer Right (D)
        return "SWIPE_RIGHT"
    if thumb_is_down and not any(finger_extended.values()):
        return "THUMBS_DOWN"  # No action

    return None

def main():
    # Note: Run this script as administrator to ensure proper input delivery to FH5
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open camera.")
        return

    controller = GestureController()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        frame_width = frame.shape[1]  # Get frame width for gesture normalization
        hands_data = controller.get_hand_landmarks(frame)
        for landmarks, hand_label in hands_data:
            gesture = recognize_gesture(landmarks, hand_label, frame_width)
            print(f"Frame width: {frame_width}, {hand_label} Hand Gesture: {gesture or 'None'}")
            map_gesture_to_action(gesture, hand_label)

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()