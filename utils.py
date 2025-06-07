import math

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def is_finger_extended(landmarks, tip_id, pip_id, hand_label):
    return landmarks[tip_id][1] < landmarks[pip_id][1]

def is_thumb_extended(landmarks, tip_id, pip_id, hand_label):
    if hand_label == "Right":
        return landmarks[tip_id][0] > landmarks[pip_id][0]
    elif hand_label == "Left":
        return landmarks[tip_id][0] < landmarks[pip_id][0]
    return False