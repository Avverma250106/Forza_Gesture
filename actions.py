from window_utils import focus_forza_window
import pydirectinput
import time

pydirectinput.PAUSE = 0.05
pydirectinput.FAILSAFE = True

# Track current gestures for each hand and last action time
current_gestures = {"Right": None, "Left": None}
last_action_time = 0
cooldown = 0.05  # Cooldown for non-held gestures

def map_gesture_to_action(gesture, hand_label):
    global current_gestures, last_action_time
    current_time = time.time()

    if gesture:
        with open('gestures.txt', 'a') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {hand_label} - {gesture}\n")
        print(f"{hand_label} Gesture detected: {gesture}")

    if not focus_forza_window():
        print("Failed to focus Forza Horizon 5, skipping action")
        return

    # Release held keys if gesture changes or no gesture for the respective hand
    if current_gestures[hand_label] in ["PALM", "PEACE", "FIST", "SWIPE_LEFT", "SWIPE_RIGHT"] and gesture != current_gestures[hand_label]:
        if current_gestures[hand_label] == "PALM":
            pydirectinput.keyUp('w')
            print(f"Action ({hand_label}): Released Accelerate (W)")
        elif current_gestures[hand_label] == "PEACE":
            pydirectinput.keyUp('s')
            print(f"Action ({hand_label}): Released Reverse (S)")
        elif current_gestures[hand_label] == "FIST":
            pydirectinput.keyUp('space')
            print(f"Action ({hand_label}): Released E-brake (Space)")
        elif current_gestures[hand_label] == "SWIPE_LEFT":
            pydirectinput.keyUp('a')
            print(f"Action ({hand_label}): Released Turn Left (A)")
        elif current_gestures[hand_label] == "SWIPE_RIGHT":
            pydirectinput.keyUp('d')
            print(f"Action ({hand_label}): Released Turn Right (D)")
        current_gestures[hand_label] = None

    # Handle gestures based on hand
    if hand_label == "Right":
        if gesture == "PALM" and current_gestures["Right"] != "PALM":
            # Release brake/reverse if active
            if current_gestures["Right"] in ["FIST", "PEACE"]:
                pydirectinput.keyUp('space' if current_gestures["Right"] == "FIST" else 's')
                print(f"Action (Right): Released {'E-brake (Space)' if current_gestures['Right'] == 'FIST' else 'Reverse (S)'}")
            pydirectinput.keyDown('w')
            print("Action (Right): Accelerate (W) - Holding")
            current_gestures["Right"] = gesture
        elif gesture == "PEACE" and current_gestures["Right"] != "PEACE":
            # Release throttle/brake if active
            if current_gestures["Right"] in ["PALM", "FIST"]:
                pydirectinput.keyUp('w' if current_gestures["Right"] == "PALM" else 'space')
                print(f"Action (Right): Released {'Accelerate (W)' if current_gestures['Right'] == 'PALM' else 'E-brake (Space)'}")
            pydirectinput.keyDown('s')
            print("Action (Right): Reverse (S) - Holding")
            current_gestures["Right"] = gesture
        elif gesture == "FIST" and current_gestures["Right"] != "FIST":
            # Release throttle/reverse if active
            if current_gestures["Right"] in ["PALM", "PEACE"]:
                pydirectinput.keyUp('w' if current_gestures["Right"] == "PALM" else 's')
                print(f"Action (Right): Released {'Accelerate (W)' if current_gestures['Right'] == 'PALM' else 'Reverse (S)'}")
            pydirectinput.keyDown('space')
            print("Action (Right): E-brake (Space) - Holding")
            current_gestures["Right"] = gesture
    elif hand_label == "Left":
        if gesture == "SWIPE_LEFT" and current_gestures["Left"] != "SWIPE_LEFT":
            pydirectinput.keyDown('a')
            print("Action (Left): Turn Left (A) - Holding")
            current_gestures["Left"] = gesture
        elif gesture == "SWIPE_RIGHT" and current_gestures["Left"] != "SWIPE_RIGHT":
            pydirectinput.keyDown('d')
            print("Action (Left): Turn Right (D) - Holding")
            current_gestures["Left"] = gesture

    # Handle THUMBS_DOWN (no action) and gesture clearing
    if gesture == "THUMBS_DOWN":
        print(f"Gesture ({hand_label}): THUMBS_DOWN detected but no action assigned")
        current_gestures[hand_label] = gesture
    elif gesture is None and current_gestures[hand_label]:
        # Release any held keys when no gesture is detected
        if current_gestures[hand_label] == "PALM":
            pydirectinput.keyUp('w')
            print(f"Action ({hand_label}): Released Accelerate (W)")
        elif current_gestures[hand_label] == "PEACE":
            pydirectinput.keyUp('s')
            print(f"Action ({hand_label}): Released Reverse (S)")
        elif current_gestures[hand_label] == "FIST":
            pydirectinput.keyUp('space')
            print(f"Action ({hand_label}): Released E-brake (Space)")
        elif current_gestures[hand_label] == "SWIPE_LEFT":
            pydirectinput.keyUp('a')
            print(f"Action ({hand_label}): Released Turn Left (A)")
        elif current_gestures[hand_label] == "SWIPE_RIGHT":
            pydirectinput.keyUp('d')
            print(f"Action ({hand_label}): Released Turn Right (D)")
        current_gestures[hand_label] = None