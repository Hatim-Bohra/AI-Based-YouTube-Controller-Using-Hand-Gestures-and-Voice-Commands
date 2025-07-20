import speech_recognition as sr
import pyautogui
import time

def listen_and_execute():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Say a command (pause, next, previous, volume up, volume down)...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {command}")

        if "pause" in command:
            pyautogui.press('space')
            print("⏸️ Paused")
        elif "next" in command:
            pyautogui.hotkey('shift', 'n')
            print("⏭️ Next")
        elif "previous" in command:
            pyautogui.hotkey('ctrl', 'left')
            print("⏮️ Previous")
        elif "volume up" in command:
            pyautogui.press('up')
            print("🔊 Volume Up")
        elif "volume down" in command:
            pyautogui.press('down')
            print("🔉 Volume Down")
        else:
            print("❓ Unknown command. Try again.")

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ Google API error: {e}")

# 🔁 Keep listening in loop
print("📢 Voice control started. Press Ctrl + C to exit.")
try:
    while True:
        listen_and_execute()     
        time.sleep(1)  # Small delay to prevent overlapping
except KeyboardInterrupt:     
    print("\n🛑 Voice control stopped.")
 