import time
from automations import ore_finder, idling, drones
import pyautogui
from config import config
from assets import image_loader

imgs = image_loader.Image_loader()

time.sleep(2)

target = imgs.warping_text

def find_indicator(indicator_img, confidence=0.90)->bool:
    times_found = 0
    ore_finder.enter_tactical_cam_view()

    while times_found < 2:
        try:
            pyautogui.locateOnScreen(indicator_img, confidence=confidence)
            times_found += 1
            if times_found == 2:
                ore_finder.enter_orbit_cam_view()
                print("Found target")
                return True
        except:
            ore_finder.orbit_screen_once()
            if times_found > 0:
                times_found -= 1
    ore_finder.enter_orbit_cam_view()
    print("Failed to find the target")
    return False
        
find_indicator(target)