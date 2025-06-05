import time
from automations import ore_finder, idling, drones
import pyautogui
from config import config


time.sleep(4)

drone = drones.Drones()

try:
    mining_in_progress_img = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\in_mining_process.png"
    mining_correctly = pyautogui.locateOnScreen(mining_in_progress_img, confidence=0.7)
    if mining_correctly:
        print("mining correctly")
        pass
except:
    print("Mining incorrectly")
    ore_finder.mining_lasers_on()
    drone.launch_drones()