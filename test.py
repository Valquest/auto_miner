import time
from automations import ore_finder, idling
import pyautogui
from config import config


time.sleep(4)

"""
Minimises idle time when ship is traveling in between asteroids
"""

counter = 0
approach_time = 180 

target_image_bigger = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Target_Locked_In_Bigger.png"
target_image_smaller = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Target_Locked_In_Smaller.png"
too_far_to_mine_img = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\strip_miner_too_far.png"

while counter < approach_time:
    try:
        print("looking for targets")
        targeted = pyautogui.locateOnScreen(target_image_bigger, confidence=0.90)
        if targeted:
            print("found target")
            break
    except:
        try:
            target = pyautogui.locateOnScreen(target_image_smaller, confidence=0.90)
            if target:
                print("found target")
                break
        except:
            print("Trying to target")
            time.sleep(10)
            pyautogui.press('ctrl')
            counter += 1

while counter < approach_time:
    try:
        pyautogui.press('f1')
        time.sleep(2)
        target = pyautogui.locateOnScreen(too_far_to_mine_img, confidence=0.80)
        if target:
            print("Too far to mine")
            time.sleep(15)
            counter += 1
    except:
        print("Can mine, within reach")
        pyautogui.press('f1')
        break


print("Next asteroid is in reach")