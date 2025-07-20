
import cv2
import mediapipe as mp
import pyautogui
import time
import joblib
from tkinter import *
from PIL import Image, ImageTk

import os
model = joblib.load(os.path.join(os.path.dirname(__file__), "..", "gesture_model.pkl"))

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture GUI")
        self.label = Label(root)
        self.label.pack()
        self.status = Label(root, text="Loading...", font=("Arial", 14))
        self.status.pack()
        self.cap = cv2.VideoCapture(0)
        self.last_action = time.time()
        self.cooldown = 1.5
        self.running = True
        self.update()

    def update(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                data = [lm.x for lm in hand.landmark] + [lm.y for lm in hand.landmark] + [lm.z for lm in hand.landmark]
                if time.time() - self.last_action > self.cooldown:
                    try:
                        gesture = model.predict([data])[0]
                        self.status.config(text=f"Detected: {gesture}")
                        self.control(gesture)
                        self.last_action = time.time()
                    except Exception as e:
                        self.status.config(text=f"Prediction error: {e}")
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.config(image=imgtk)
        if self.running:
            self.root.after(10, self.update)

    def control(self, gesture):
        if gesture == "pause":
            pyautogui.press('space')
        elif gesture == "next":
            pyautogui.hotkey('shift', 'n')
        elif gesture == "previous":
            pyautogui.hotkey('ctrl', 'left')
        elif gesture == "volumeup":
            pyautogui.press('up')
        elif gesture == "volumedown":
            pyautogui.press('down')

    def stop(self):
        self.running = False
        self.cap.release()
        self.root.destroy()

root = Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.stop)
root.mainloop()
