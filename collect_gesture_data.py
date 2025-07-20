
import cv2
import mediapipe as mp
import csv
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

label = input("Enter gesture label: ")
os.makedirs("gesture_data", exist_ok=True)
file = open(f"gesture_data/{label}.csv", 'w', newline='')
writer = csv.writer(file)

print("Collecting data... Press 'q' to stop.")
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            data = []
            for lm in hand.landmark:
                data.extend([lm.x, lm.y, lm.z])
            writer.writerow(data)
    cv2.imshow("Collecting", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
file.close()
cv2.destroyAllWindows()
