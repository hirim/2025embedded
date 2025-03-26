from picamera2 import Picamera2
import cv2
import mediapipe as mp


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'format': 'RGB888', 'size': (640, 480)}))
picam2.start()


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


finger_tips = [8, 12, 16, 20]
thumb_tip = 4

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

    
    cv2.putText(frame, f'Finger Count: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    
    cv2.imshow('Finger Count', frame)


    if cv2.waitKey(1) & 0xFF == 27:
        break

