import pyautogui
import time
import os

def test():
    image_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\Dense_Veldspar_Text.png"
    #image_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\test.png"
    time.sleep(3)
    if os.path.exists(image_path):
        print(f"Image found at: {image_path}")
    print("Locating")
    x, y = pyautogui.locateCenterOnScreen(image_path)
    print("Moving mouse")
    pyautogui.moveTo(x, y, duration=2)