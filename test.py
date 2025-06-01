import time
from automations import ore_finder
import pyautogui
from config import config


time.sleep(2)

while True:
    WARP_TIME = 35

    warping_text = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Warping_text.png"

    while True:
        try:
            found_warp_text = pyautogui.locateCenterOnScreen(warping_text, confidence=0.80)
            if found_warp_text:
                print("Warp drive active")
                break
        except:
            time.sleep(1)

    # Delay for ship to warp to an asteroid
    is_warping_check = 0

    while is_warping_check < WARP_TIME:
        try:
            warping = pyautogui.locateOnScreen(warping_text, confidence=0.80)    
            if warping:
                continue
        except:
            time.sleep(1)
            is_warping_check += 1
            break

    time.sleep(2)

    print("Warping completed")
    break