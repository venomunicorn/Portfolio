import pyautogui
import time
import keyboard

clicking = False

print("Auto-clicker loaded.")
print("Press F6 to START clicking.")
print("Press F7 to STOP clicking.")
print("Press ESC to exit.")

def start_clicking():
    global clicking
    clicking = True
    print("Auto-clicking started...")
    while clicking:
        pyautogui.click()
        time.sleep(0.6)  # ⏱️ Matches full sword cooldown for max damage
        if keyboard.is_pressed("F7"):
            clicking = False
            print("Auto-clicking stopped.")
            break
        if keyboard.is_pressed("esc"):
            print("Exiting...")
            exit()

while True:
    if keyboard.is_pressed("F6"):
        start_clicking()
    elif keyboard.is_pressed("esc"):
        print("Exiting...")
        break
