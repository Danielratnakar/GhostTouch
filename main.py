import cv2
import mediapipe as mp
import time
import math

# Webcam setup
cap = cv2.VideoCapture(0)

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# States
devices = {
    "Light": False,
    "TV": False,
    "AC": False,
    "Door Lock": False
}
light_brightness = 50
ac_temp = 22
system_active = False

# Modes
light_adjust_mode = False
ac_adjust_mode = False

# For rotation detection
last_angle = None
angle_threshold = 5

finger_tips = [4, 8, 12, 16, 20]
last_toggle_time = 0
cooldown = 1.2

def fingers_up(hand):
    fingers = []
    if hand.landmark[finger_tips[0]].x < hand.landmark[finger_tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1, 5):
        if hand.landmark[finger_tips[id]].y < hand.landmark[finger_tips[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def get_wrist_angle(hand):
    wrist = hand.landmark[0]
    index_mcp = hand.landmark[5]
    dx = index_mcp.x - wrist.x
    dy = index_mcp.y - wrist.y
    return math.degrees(math.atan2(dy, dx))

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    current_time = time.time()

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
        fingers = fingers_up(handLms)

        # Master ON/OFF
        if fingers == [0,1,0,0,1] and current_time - last_toggle_time > cooldown:
            system_active = not system_active
            light_adjust_mode = False
            ac_adjust_mode = False
            last_toggle_time = current_time
            last_angle = None

        if system_active and current_time - last_toggle_time > cooldown:

            # TV toggle
            if fingers == [1,1,1,1,1]:
                devices["TV"] = not devices["TV"]
                light_adjust_mode = False
                ac_adjust_mode = False
                last_toggle_time = current_time

            # Door Lock toggle
            elif fingers == [0,0,0,0,1]:
                devices["Door Lock"] = not devices["Door Lock"]
                light_adjust_mode = False
                ac_adjust_mode = False
                last_toggle_time = current_time

            # ✌️ Light gesture logic
            elif fingers == [0,1,1,0,0]:
                if not devices["Light"]:
                    devices["Light"] = True
                    light_adjust_mode = True
                elif devices["Light"] and not light_adjust_mode:
                    light_adjust_mode = True
                elif light_adjust_mode:
                    devices["Light"] = False
                    light_adjust_mode = False
                last_toggle_time = current_time
                last_angle = None

            # 👍 AC gesture logic
            elif fingers == [1,0,0,0,0]:
                if not devices["AC"]:
                    devices["AC"] = True
                    ac_adjust_mode = True
                elif devices["AC"] and not ac_adjust_mode:
                    ac_adjust_mode = True
                elif ac_adjust_mode:
                    devices["AC"] = False
                    ac_adjust_mode = False
                last_toggle_time = current_time
                last_angle = None

            # Rotation-based adjustment
            if light_adjust_mode and devices["Light"]:
                angle = get_wrist_angle(handLms)
                if last_angle is not None:
                    delta = angle - last_angle
                    if delta > 180: delta -= 360
                    if delta < -180: delta += 360
                    if abs(delta) > angle_threshold:
                        if delta > 0:
                            light_brightness = min(100, light_brightness + 1)
                        else:
                            light_brightness = max(0, light_brightness - 1)
                        last_toggle_time = current_time
                last_angle = angle

            elif ac_adjust_mode and devices["AC"]:
                angle = get_wrist_angle(handLms)
                if last_angle is not None:
                    delta = angle - last_angle
                    if delta > 180: delta -= 360
                    if delta < -180: delta += 360
                    if abs(delta) > angle_threshold:
                        if delta > 0:
                            ac_temp = min(30, ac_temp + 0.5)
                        else:
                            ac_temp = max(16, ac_temp - 0.5)
                        last_toggle_time = current_time
                last_angle = angle

            # Exit adjustment mode if any unrelated gesture is shown
            if fingers not in ([0,1,1,0,0], [1,0,0,0,0]):
                light_adjust_mode = False
                ac_adjust_mode = False
                last_angle = None

    else:
        light_adjust_mode = False
        ac_adjust_mode = False
        last_angle = None

    # UI
    y = 30
    cv2.putText(img, f"System: {'ACTIVE' if system_active else 'INACTIVE'}", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) if system_active else (0,0,255), 2)
    y += 50

    for device, status in devices.items():
        color = (0,255,0) if status else (0,0,255)
        text = f"{device}: {'ON ✅' if status else 'OFF ❌'}"
        cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        y += 40

    if devices["Light"]:
        cv2.putText(img, f"Brightness: {int(light_brightness)}%", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
        y += 35
    if devices["AC"]:
        cv2.putText(img, f"AC Temp: {ac_temp:.1f}°C", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
        y += 35

    cv2.imshow("Gesture Smart Home", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
