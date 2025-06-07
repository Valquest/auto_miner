import pyautogui
import time
import random
from config import config
from pyautogui import ImageNotFoundException
from automations import drones
from assets.image_loader import Image_loader

# Instantiate classes
imgs = Image_loader()
drone = drones.Drones()

# Load image paths
mining_tab_image_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\mining_tab.png"
warp_image_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\warp_to_within.png"
asteroid_belt_img_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\asteroid_belt.png"
warping_text = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\warping.png"
mining_completed_img = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Mining_Completed.png"
mining_completed_retriever_img = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\mining_completed_retriever.png"


def mine(retriever=False):

    mouse_action(asteroid_belt_img_path, "rightClick")

    mouse_action(warp_image_path, "click", offset_x=round(random.randint(1, 60)), 
              offset_y=round(random.randint(1, 3)))

    warp()

    # Locate asteroid to mine again (in case it was not marked the first time 
    # as targeting only works if is marked in Overview window)
    approach_closest_asteroid(retriever=retriever)

    mine_in_asteroid_belt(retriever=retriever)

    # Return home
    mouse_action(imgs.refinery_btn, "rightClick", offset_x=round(random.randint(1,80)), offset_y=round(random.randint(1,5)))

    mouse_action(warp_image_path, "click")

    warp()

def random_movement(points:int=1)-> None:
    """
    Adds random movement that do not add value to automation, but
    mimics more random human like behavior.
    args:
        points: An integer number of points mouse should visit
    return: 
        None
    """
    screen_width = 1500
    screen_height = 800

    for _ in range(points):
        rand_x = round(random.randint(400,screen_width))
        rand_y = round(random.randint(200,screen_height))
        pyautogui.moveTo(rand_x, rand_y, duration=0.5)

def mouse_action(img:str, click_type:str, offset_x:int=0, offset_y:int=0, rand_moves=3, confidence=0.85)-> None:
    random_delay = round(random.uniform(0.5, 1))
    random_number_of_random_movements = random.randint(0, rand_moves)
    try:
        random_movement(random_number_of_random_movements)
        x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence)
        x += offset_x
        y += offset_y
        print(f"Moving mouse to: \"{img}\" image")
        pyautogui.moveTo(x, y, duration=random_delay, tween=pyautogui.easeInOutQuad)
        time.sleep(random_delay)
        match click_type:
            case "click":
                pyautogui.click()
            case "rightClick":
                pyautogui.rightClick()
            case "move":
                return
            case _:
                return
    except ImageNotFoundException as e:
        print(f"error: {e}")
        try:
            pyautogui.screenshot(f"{config.root_path}\\auto_miner\\error_screenshots\\screenshot.png")
        except:
            print("Failed capturing a screenshot")
    

    time.sleep(random_delay)

def mine_in_asteroid_belt(retriever=False)-> None:
    """ 
    Start mining, check if asteroid is depleted if so, find another one to mind, when
    timer is done head back to offload
    return:
        None
    """
    mining_lasers_on()

    if retriever:
        drone.launch_drones()

    mining_corretly = False
    timer = 0
    asteroid_depleted = False
    asteroid_depleted_img_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\depleted.png"
    while timer < 1800: #865 for Venturer, 1800 for Retriever
        if asteroid_depleted:

            if retriever:
                drone.retrieve_drones()

            approach_closest_asteroid(retriever=retriever)

            mining_lasers_on()

            if retriever:
                drone.launch_drones()

            asteroid_depleted = False
        try:
            coords = pyautogui.locateCenterOnScreen(asteroid_depleted_img_path, confidence=0.7)
            if coords:  # If image is found
                asteroid_depleted = True
                coords = None
        except pyautogui.ImageNotFoundException:
            timer += 1
            time.sleep(1)
            if timer % 100 == 0:
                print(f"Timer at: {timer}")
        if not mining_corretly:
            try:
                time.sleep(5)
                mining_in_progress_img = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\in_mining_process.png"
                mining_correctly = pyautogui.locateOnScreen(mining_in_progress_img, confidence=0.7)
                if mining_correctly:
                    mining_corretly = True
                    pass
            except:
                approach_closest_asteroid()
                mining_lasers_on()
                drone.launch_drones()
        try:
            if retriever:
                mining_completed = pyautogui.locateCenterOnScreen(mining_completed_retriever_img, confidence=0.90)
                drone.retrieve_drones()
            else:
                mining_completed = pyautogui.locateCenterOnScreen(mining_completed_img, confidence=0.90)
            if mining_completed:
                print("Mining is completed")
                return
        except:
            pass
    drone.retrieve_drones()
    print("Done mining")

def approach_closest_asteroid(retriever=False):
    # Select first asteroid form the summary console
    mouse_action(mining_tab_image_path, "click", offset_y=50, confidence=0.95)

    # Approach asteroid by using keyboard shortcuts
    pyautogui.press("q")
    time.sleep(1)
    # Second click as sometimes first one does not trigger
    pyautogui.press("q")

    time.sleep(1)

    # Turn on boosters
    pyautogui.keyDown("alt")
    pyautogui.press("f2")
    pyautogui.keyUp("alt")

    traveling(retriever=retriever)

    # Turn off boosters
    pyautogui.keyDown("alt")
    pyautogui.press("f2")
    pyautogui.keyUp("alt")

def mining_lasers_on():

    mining_lasers_off()
    drone.retrieve_drones()

    # Reselect asteroid in case some other was selected while function tried to turn off lasers
    # and none where on
    mouse_action(mining_tab_image_path, "click", offset_y=50, confidence=0.95)

    # Locking in target and starting lasers
    pyautogui.press("ctrl")
    time.sleep(0.5)
    pyautogui.press("f1")
    time.sleep(1)
    pyautogui.press("f2")

def wait_for_end_of_warp()->None:
    """
    Checks if ship is in warp mode
    """
    while True:
        try:
            found_warp_text = pyautogui.locateCenterOnScreen(warping_text, confidence=0.75)
            if found_warp_text:
                print("Warp drive active")
                break
        except:
            time.sleep(1)

def warp()-> None:
    """
    Manages warping rest time. Rests while warp. Solves issue with fixed warp time, where
    ship would wait till general time.sleep would end for short warps
    """
    WARP_TIME = 40
    warp_ended_approval = 0

    # Retrieve drones before warping if possible
    drone.retrieve_drones()

    warping_text = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Warping_text.png"

    wait_for_end_of_warp()

    # Delay for ship to warp to an asteroid
    is_warping_check = 0

    while is_warping_check < WARP_TIME:
        try:
            warping = pyautogui.locateOnScreen(warping_text, confidence=0.75)    
            if warping:
                continue
        except:
            time.sleep(1)
            is_warping_check += 1
            warp_ended_approval += 1
            if warp_ended_approval == 3:
                break

    time.sleep(5)

    print("Warping completed")

def traveling(retriever=False)-> None:
    """
    Minimises idle time when ship is traveling in between asteroids
    """
    approach_time = 60
    counter = 0

    if retriever:
        approach_time = 180 

    # Initial wait before flying speed is appearing on the screen
    time.sleep(10)

    target_image_bigger = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Target_Locked_In_Bigger.png"
    target_image_smaller = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Target_Locked_In_Smaller.png"
    too_far_to_mine_img = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\strip_miner_too_far.png"

    while counter < approach_time:
        try:
            print("looking for target marks")
            targeted = pyautogui.locateOnScreen(target_image_bigger, confidence=0.90)
            if targeted:
                print("found target mark")
                break
        except:
            try:
                target = pyautogui.locateOnScreen(target_image_smaller, confidence=0.90)
                if target:
                    print("found target mark")
                    break
            except:
                print("Trying to target asteroid")
                time.sleep(10)
                pyautogui.press('ctrl')
                counter += 1

    while counter < approach_time:
        try:
            pyautogui.press('f1')
            time.sleep(2)
            target = pyautogui.locateOnScreen(too_far_to_mine_img, confidence=0.80)
            if target:
                time.sleep(15)
                counter += 1
        except:
            pyautogui.press('f1')
            break

    print("Next asteroid is in reach")

def mining_lasers_off():
    # pyautogui.press("f1")
    # time.sleep(1)
    # pyautogui.press("f2")
    # time.sleep(15)

    mining_laser = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\mining_laser_starting_point.png"
    x = -100
    y = 50

    while True:
        try:
            print("Clicking lasers")
            mouse_action(mining_laser, "click", rand_moves=0, offset_x=x, offset_y=y)
            time.sleep(1)
            mouse_action(mining_laser, "click", rand_moves=0, offset_x=x, offset_y=y)
            print("Clicked lasers")
            break
        except:
            print("No lasers on")
            break