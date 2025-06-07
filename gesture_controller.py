import cv2
import mediapipe as mp

class GestureController:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(max_num_hands=2)  # Increased to detect two hands
        self.mp_draw = mp.solutions.drawing_utils

    def get_hand_landmarks(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        hands_data = []
        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, hand_info in zip(result.multi_hand_landmarks, result.multi_handedness):
                self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                hand_label = hand_info.classification[0].label  # "Right" or "Left"
                hands_data.append((landmarks, hand_label))
        return hands_data  # Returns list of (landmarks, hand_label) tuples