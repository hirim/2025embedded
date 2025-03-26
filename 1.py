from picamera2 import Picamera2
import cv2
import mediapipe as mp

# Picamera2 setting 
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'format': 'RGB888', 'size': (640, 480)}))
picam2.start()

# Mediapipe 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

while True:
    # Picamera2 Setting 
    frame = picam2.capture_array()
    
    # OpenCV
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Mediapipe 
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    cv2.imshow('Hand Tracking', frame)

    #
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

