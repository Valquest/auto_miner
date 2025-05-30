import pyautogui
import time
import random

mining_tab_image_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\mining_tab.png"
warp_image_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\warp_to_within.png"
home_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\general\\refinery.png"
asteroid_belt_img_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\asteroid_belt.png"
WARP_TIME = 40
APPROACH_TIME = 20

def excavate():

    mouse_action(asteroid_belt_img_path, "rightClick")

    mouse_action(warp_image_path, "click", offset_x=round(random.randint(1, 100)), 
              offset_y=round(random.randint(1, 5)))

    # Delay for ship to warp to an asteroid
    time.sleep(WARP_TIME)

    # Locate asteroid to mine again (in case it was not marked the first time 
    # as targeting only works if is marked in Overview window)
    approach_closest_asteroid()

    mine()

    # Return home
    mouse_action(home_path, "rightClick", offset_x=round(random.randint(1,150)), offset_y=round(random.randint(1,8)))

    mouse_action(warp_image_path, "click")
    # x, y = pyautogui.locateCenterOnScreen(warp_image_path, confidence=0.85)
    # pyautogui.moveTo(x + random_num, y, duration=0.5)
    # time.sleep(0.5)
    # pyautogui.click()

    time.sleep(WARP_TIME)

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

def mouse_action(img:str, click_type:str, offset_x:int=0, offset_y:int=0, rand_moves=3)-> None:
    random_delay = round(random.uniform(0.5, 1))
    random_number_of_random_movements = random.randint(0, rand_moves)
    random_movement(random_number_of_random_movements)
    x, y = pyautogui.locateCenterOnScreen(img, confidence=0.85)
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
    asteroid_depleted_img_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\depleted.png"
    while timer < 865: #865
        if asteroid_depleted:
            approach_closest_asteroid()
            # Allow lasers that are still cached on old asteroid to run out and
            # realise they are not mining anything
            time.sleep(20)
            mining_lasers_on()
            timer -= APPROACH_TIME
            asteroid_depleted = False
        try:
            coords = pyautogui.locateCenterOnScreen(asteroid_depleted_img_path, confidence=0.7)
            if coords:  # If image is found
                asteroid_depleted = True
                coords = None
        except pyautogui.ImageNotFoundException:
            timer += 1
            time.sleep(1)
            print(f"Timer at: {timer}")
    print("Done mining")

def approach_closest_asteroid():
    # Select first asteroid form the summary console
    mouse_action(mining_tab_image_path, "click", offset_y=50)

    # Approach asteroid by using keyboard shortcuts
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

    time.sleep(APPROACH_TIME)

def mining_lasers_on():
    # Locking in target and starting lasers
    pyautogui.press("ctrl")
    time.sleep(2)
    pyautogui.press("f1")
    time.sleep(1)
    pyautogui.press("f2")