import time
from automations import ore_finder, idling, drones
import pyautogui
from config import config
from assets import image_loader

imgs = image_loader.Image_loader()

time.sleep(2)

target = imgs.mining_in_progress_img

def locate_indicators(indicator_img, confidence=0.95, move_screen=True, retries=3)->None:
    times_found = 0
    num_of_tries = 0
    orbit_view = ore_finder.orbit_ui_in_space()

    while times_found <= retries or num_of_tries > 3:
        try:
            found_indicator = pyautogui.locateCenterOnScreen(indicator_img, confidence=confidence)
            if found_indicator:
                times_found += 1
                if times_found == retries:
                    print("Indicator located")
                    next(orbit_view)
                    break       
        except:
            if move_screen:
                try:
                    next(orbit_view)
                except:
                    pass
            # Reset counters and generator function
            times_found = 0
            orbit_view = ore_finder.orbit_ui_in_space()
            time.sleep(0.3)
            num_of_tries += 1

locate_indicators(target)