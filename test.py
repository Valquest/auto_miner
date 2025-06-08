import time
from automations import ore_finder, idling, drones
import pyautogui
from config import config
from assets import image_loader

imgs = image_loader.Image_loader()

time.sleep(2)

target = imgs.warping_text
drone = drones.Drones()

def warp_rest_timer(handle_drones=True)-> None:
    """
    Manages warping rest time. Rests while warp. Solves issue with fixed warp time, where
    ship would wait till general time.sleep would end for short warps
    """
    # Retrieve drones before warping if possible
    if handle_drones:
        drone.retrieve_drones()

    ore_finder.locate_indicators(imgs.warping_text, confidence=0.9)

    time.sleep(2)
    print("Warping")

    ore_finder.locate_indicators(imgs.warping_text, confidence=0.9, orbit=False, retries=30, wait_for_absence=True)
        
    print("Arriving to your destination")

    time.sleep(5)

    print("Warping completed")

warp_rest_timer()