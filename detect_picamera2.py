# -*- coding: utf-8 -*- 

from picamera2 import Picamera2
import cv2
import mediapipe as mp

# Picamera2 초기화
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'format': 'RGB888', 'size': (640, 480)}))
picam2.start()

# Mediapipe 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

def count_fingers(hand_landmarks):
    fingers = []

    # 엄지: 엄지의 끝이 엄지의 관절보다 오른쪽에 있는지 확인 (오른손 기준)
    if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_tip - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 나머지 네 손가락: 각 손가락 끝이 손가락의 시작 부분보다 위에 있는지 확인
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

while True:

    frame = picam2.capture_array()

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            if landmarks[thumb_tip].x < landmarks[thumb_tip - 1].x:
                finger_count += 1

            for tip in finger_tips:
                if landmarks[tip].y < landmarks[tip - 2].y:
                    finger_count += 1

    # 손가락 개수와 함께 "Finger Counter" 텍스트를 화면에 표시
    cv2.putText(frame, 'Finger Counter:', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'{finger_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Finger Count', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
