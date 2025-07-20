import cv2
import mediapipe as mp
import pyautogui
import time
import joblib
from tkinter import *
from PIL import Image, ImageTk
import threading
import speech_recognition as sr

# Load ML gesture model
import os
model_path = os.path.join(os.path.NN dirname(__file__), "..", "gesture_model.pkl")
model = joblib.load(model_path)   


# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Voice control function (in separate thread)
def voice_control_loop():
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("\n🎤 Say a command (pause, next, previous, volume up, volume down)...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)

            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ You said: {command}")

            if "pause" in command:
                pyautogui.press('space')
            elif "next" in command:
                pyautogui.hotkey('shift', 'n')
            elif "previous" in command:
                pyautogui.hotkey('ctrl', 'left')
            elif "volume up" in command:
                pyautogui.press('up')
            elif "volume down" in command:
                pyautogui.press('down')
            else:
                print("❓ Unknown voice command.")
        except Exception as e:
            print(f"⚠️ Voice error: {e}")

# GUI with gesture recognition
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture + Voice Controller")
        self.root.geometry("800x600")
        self.label = Label(root)
        self.label.pack(pady=10)
        self.status = Label(root, text="Initializing camera...", font=("Arial", 14))
        self.status.pack(pady=10)
        self.exit_button = Button(root, text="Exit", command=self.stop, font=("Arial", 12), bg="red", fg="white")
        self.exit_button.pack(pady=10)
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
                        self.status.config(text=f"🖐️ Detected gesture: {gesture}")
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

# Main execution
if __name__ == "__main__":
    # Start voice recognition in background thread
    threading.Thread(target=voice_control_loop, daemon=True).start()

    # Start gesture GUI (main thread)
    root = Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.stop)
    root.mainloop()
