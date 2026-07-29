import cv2
import mediapipe as mp
import time
from esp32_simulator import encrypt_message, try_command

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

last_command = None
last_command_time = 0
COMMAND_COOLDOWN = 2


def count_extended_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    pip_joints = [6, 10, 14, 18]
    extended = 0

    for tip, pip in zip(tips, pip_joints):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            extended += 1

    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]

    if thumb_tip.x < thumb_ip.x:
        extended += 1

    return extended


while True:
    success, frame = cam.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    gesture_text = "No hand detected"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            finger_count = count_extended_fingers(hand_landmarks)
            current_time = time.time()

            if finger_count >= 4:
                gesture_text = "OPEN PALM -> unlock"

                if last_command != "unlock" or (
                    current_time - last_command_time
                ) > COMMAND_COOLDOWN:
                    print("ESP32:", try_command(encrypt_message("unlock")))
                    last_command = "unlock"
                    last_command_time = current_time

            elif finger_count == 0:
                gesture_text = "CLOSED FIST -> lock"

                if last_command != "lock" or (
                    current_time - last_command_time
                ) > COMMAND_COOLDOWN:
                    print("ESP32:", try_command(encrypt_message("lock")))
                    last_command = "lock"
                    last_command_time = current_time

            else:
                gesture_text = f"{finger_count} fingers up (no action)"

    cv2.putText(
        frame,
        gesture_text,
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("Gesture Lock Control", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
hands.close()
cv2.destroyAllWindows()