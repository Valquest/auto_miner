import time
from automations import ore_finder
import pyautogui
from config import config


time.sleep(2)
target_image = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Target_Locked_In.png"

while True:
    try:
        targeted = pyautogui.locateCenterOnScreen(target_image, confidence=0.95)
        if targeted:
            print("found")
            x, y = targeted
            print(f"x: {x}, y: {y}")
            time.sleep(0.3)
    except:
        print("Didnt find")
        time.sleep(0.3)


