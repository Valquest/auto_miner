import pyautogui
import time
import random
from config import config

mining_tab_image_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\mining_tab.png"
warp_image_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\warp_to_within.png"
home_path = f"{config.root_path}\\auto_miner\\screenshots\\general\\refinery.png"
asteroid_belt_img_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\asteroid_belt.png"
warping_text = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\warping.png"
mining_completed_img = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Mining_Completed.png"


def excavate():

    mouse_action(asteroid_belt_img_path, "rightClick")

    mouse_action(warp_image_path, "click", offset_x=round(random.randint(1, 60)), 
              offset_y=round(random.randint(1, 3)))

    # Additional click on any of the asteroids in case refinery is selected
    # since refinery has word "mining" in it title, which disturbs following actions
    mouse_action(mining_tab_image_path, "click", offset_y=50, confidence=0.95)

    warp()

    # Locate asteroid to mine again (in case it was not marked the first time 
    # as targeting only works if is marked in Overview window)
    approach_closest_asteroid()

    mine()

    # Return home
    mouse_action(home_path, "rightClick", offset_x=round(random.randint(1,80)), offset_y=round(random.randint(1,5)))

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
    screen_width = 1900
    screen_height = 1000

    for point in range(points):
        print(f"Visiting random point #:{point}")
        rand_x = round(random.randint(0,screen_width))
        rand_y = round(random.randint(0,screen_height))
        pyautogui.moveTo(rand_x, rand_y, duration=0.5)

def mouse_action(img:str, click_type:str, offset_x:int=0, offset_y:int=0, rand_moves=3, confidence=0.85)-> None:
    random_delay = round(random.uniform(0.5, 1))
    random_number_of_random_movements = random.randint(0, rand_moves)
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

    time.sleep(random_delay)

def mine()-> None:
    """ 
    Start mining, check if asteroid is depleted if so, find another one to mind, when
    timer is done head back to offload
    return:
        None
    """
    mining_lasers_on()

    timer = 0
    asteroid_depleted = False
    asteroid_depleted_img_path = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\depleted.png"
    while timer < 900: #865
        if asteroid_depleted:

            # Turn off both lasers. If one of them is still on, nothing wrong happens
            pyautogui.press("f1")
            pyautogui.press("f2")

            approach_closest_asteroid()

            mining_lasers_on()

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
        try:
            mining_completed = pyautogui.locateCenterOnScreen(mining_completed_img, confidence=0.90)
            if mining_completed:
                print("Mining is completed")
                return
        except:
            pass
    print("Done mining")

def approach_closest_asteroid():
    # Select first asteroid form the summary console
    mouse_action(mining_tab_image_path, "click", offset_y=50)

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

    time.sleep(10)

    # Turn off boosters
    pyautogui.keyDown("alt")
    pyautogui.press("f2")
    pyautogui.keyUp("alt")

    traveling()

def mining_lasers_on():
    # Locking in target and starting lasers
    pyautogui.press("ctrl")
    time.sleep(0.5)
    pyautogui.press("f1")
    time.sleep(1)
    pyautogui.press("f2")

def warp()-> None:
    """
    Manages warping rest time. Rests while warp. Solves issue with fixed warp time, where
    ship would wait till general time.sleep would end for short warps
    """
    WARP_TIME = 40

    warping_text = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\warping2.png"

    # Initial delay for warp indicators to kick in on the screen
    time.sleep(5)

    # Delay for ship to warp to an asteroid
    is_warping_check = 0

    while is_warping_check < WARP_TIME:
        try:
            warping = pyautogui.locateOnScreen(warping_text, confidence=0.75)
            if warping:
                continue
        except:
            break
        time.sleep(3)
        is_warping_check += 1

    time.sleep(5)

    print("Warping completed")

def traveling()-> None:
    """
    Minimises idle time when ship is traveling in between asteroids
    """
    APPROACH_TIME = 60
    counter = 0

    # Initial wait before flying speed is appearing on the screen
    time.sleep(10)

    target_image = f"{config.root_path}\\auto_miner\\screenshots\\ore_finder\\Target_Locked_In.png"

    while counter < APPROACH_TIME:
        try:
            targeted = pyautogui.locateOnScreen(target_image, confidence=0.90)
            if targeted:
                break
        except:
            time.sleep(1)
            pyautogui.press('ctrl')
            counter += 1

    print("Next asteroid reached")
