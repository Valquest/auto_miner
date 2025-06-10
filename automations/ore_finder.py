"""
Handles operations needed to navigate to asteroid belt and back to refinery, navigate in asteroid belt,
handle mining and mining state checks, trigering end of mining.
"""

import pyautogui
import random
import time

from automations import drones
from config import config
from assets.image_loader import Image_loader
from pyautogui import ImageNotFoundException

# Instantiate classes
imgs = Image_loader()
drone = drones.Drones()

def approach_closest_asteroid(retriever=False)->None:
    """
    Handle navigation towards next target asteroid
    args:
        retriever: Flag that defines if ship is of "Retriever" type
    return:
        None
    """
    # Select first asteroid form the summary console
    mouse_action(imgs.mining_tab_img, "click", offset_y=50, confidence=0.95)

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

    # Event based delay for when ship is traveling for extended times. Delay adjusts
    # based on distance ship needs to fly
    traveling(retriever=retriever)

    # Turn off boosters
    pyautogui.keyDown("alt")
    pyautogui.press("f2")
    pyautogui.keyUp("alt")

def enter_orbit_cam_view()->None:
    """
    Returns back to orbit view
    return:
        None
    """
    pyautogui.keyDown("alt")
    pyautogui.press("2")
    pyautogui.keyUp("alt")

def enter_tactical_cam_view()->None:
    """
    Handles accessing tactical cam view
    return:
        None
    """
    # Accesses tactical view
    pyautogui.keyDown("alt")
    pyautogui.press("1")
    pyautogui.keyUp("alt")

    time.sleep(1)

    # Zooms out to avoid clicking any asteroids when rotating screen
    pyautogui.scroll(1500)

def locate_indicators(indicator_img, confidence=0.90, orbit=True, retries=6, wait_for_absence=False)->bool:
    """
    Attempts to find provided vissual indicator. Orbits arround the ship to have more success
    when looking for vissual indications
    args:
        indicator_img: image to look for,
        confidence: how confident should indicator be when locating images,
        orbit: flag used to toggle screen orbiting,
        retries: number of times function should try to locate the image,
        wait_for_absence: in case you want to wait for indicator_img to dissapear as opposed to appear on screen
    return:
        bool: Boolean value if desired action was achieved 
    """
    # Define core variables
    times_found = 0
    total_atempts = 0

    if orbit:
        # Turns tactical cam view on
        enter_tactical_cam_view()

    # Loop while times image was located is less than 2 times and not exceeding expected ammount of retries
    # we locate image multiple times as sometimes, lower confidence level indications would find the wrong image
    while times_found < 2 and total_atempts < retries:
        try:
            # Try to find the image
            pyautogui.locateOnScreen(indicator_img, confidence=confidence)
            # If found, increment variable
            times_found += 1

            # If times found already at 2, exit tactical view by entering orbit cam and quit function
            if times_found == 2 and not wait_for_absence:
                if orbit:
                    # Exit tactical view by entering orbit view
                    enter_orbit_cam_view()
                print("Found target")
                return True
            # In case wait for absence flag is True, we reset time found to 0. Desired outcome is that pyautogui locator will fail
            # to find the image and exception will handle the ablsence logic
            elif wait_for_absence:
                times_found = 0
        except:
            # Absence achieved. Exit function
            if wait_for_absence:
                print("Target no longer present")
                # Exit tactical view
                enter_orbit_cam_view()
                return True
            # If failed to find, but was looking for an image, rotate view to a different area.
            # rotaion needs to happen in order to change background for space as it is colorul and
            # confuses identifiers
            if orbit:
                orbit_screen_once()
            
            # Decrement times found if failed to find requiring more checks for ambiquous cases
            if times_found > 0:
                times_found -= 1
            total_atempts += 1

    # If failed to find after multiple retries, return to the right view and function returns False
    if orbit:            
        enter_orbit_cam_view()
    print("Failed to find the target")
    return False

def mine(retriever=False)-> None:
    """
    Handles mining execution by calling each mining process step in a right order
    """

    # Clicks the asteroid belt location shortcut
    mouse_action(imgs.asteroid_belt_btn, "rightClick")

    # Click warp button to start warping to destination
    mouse_action(imgs.warp_btn, "click", offset_x=round(random.randint(1, 60)), 
              offset_y=round(random.randint(1, 3)))

    # Event driven delay that idles execution based on distance being warped
    warp_rest_timer()

    # Locate asteroid to mine again (in case it was not marked the first time 
    # as targeting only works if is marked in Overview window)
    approach_closest_asteroid(retriever=retriever)

    mine_in_asteroid_belt(retriever=retriever)

    # Return home by right clicking the refinery location
    mouse_action(imgs.refinery_btn, "rightClick", offset_x=round(random.randint(1,80)), offset_y=round(random.randint(1,5)))

    # Click warp button to start warping
    mouse_action(imgs.warp_btn, "click")

    # Event driven delay that ideles execution absed on distance being warped
    warp_rest_timer()

def mine_in_asteroid_belt(retriever=False)-> None:
    """ 
    Start mining, check if asteroid is depleted if so, find another one to mind, when
    timer is done head back to offload
    args:
        retriever: True of False value to define if ship of type "Retriever" is being used. As some
        indicators are ship specific, especially during mining time, this has to be case specific and
        needs identifying
    return:
        None
    """
    # Set base variables
    mining_corretly = False
    timer = 0
    asteroid_depleted = False

    # Turn on mining lasers
    mining_lasers_on()

    # If available, turn on mining drones
    if retriever:
        drone.launch_drones()
    
    # Define a fixed ammount of configurable mining time for cases where other vissual indicators
    # fail to define end of mining
    while timer < config.mining_time:
        
        # Check if asteroid, which was being mined is now depleted
        if asteroid_depleted:

            # Retract drones if available
            if retriever:
                drone.retrieve_drones()

            # Navigation towards next asteroid
            approach_closest_asteroid(retriever=retriever)

            # Turning mining lasers on
            mining_lasers_on()

            # Launching drones if applicable
            if retriever:
                drone.launch_drones()

            # Reset flag
            asteroid_depleted = False

        try:
            # Check if asteroid is depleted
            pyautogui.locateCenterOnScreen(imgs.asteroid_depleted_img, confidence=0.7)

            # If first line of this try block did not fail and throw an error, means it found the image and flag
            # should be set to True    
            asteroid_depleted = True
            
        except pyautogui.ImageNotFoundException:

            # If failed to located "asteroid_depleted_img"
            timer += 1
            time.sleep(1)

            # Every 100th counter count log progress information
            if timer % 100 == 0:
                print(f"Timer at: {timer}")

        # If mining is False, which is always starts of like False
        if not mining_corretly:
            try:
                # Delay for second operation, not to click UI too fast as it updates after first click
                time.sleep(1.5)

                # Tries to locate image, that confirms if mining correclt and based on that sets flag or goes to exception
                pyautogui.locateOnScreen(imgs.mining_in_progress_img, confidence=0.7)
                mining_corretly = True
            except:
                # If was not mining correctly (not all lasers are on or drones were not turned on)
                # Approach closest asteroid
                approach_closest_asteroid()

                # Turns mining laser on
                mining_lasers_on()

                # Launch drones
                if (retriever):
                    drone.launch_drones()
        # Do different checks for different ship types. If inventory full, 
        try:
            if retriever:
                # If mining is done, retrieve drones and exit function
                pyautogui.locateCenterOnScreen(imgs.mining_completed_retriever_img, confidence=0.90)
                drone.retrieve_drones()
                print("Mining is completed")
                return
            else:
                # If not a retriever, try to locate different "Full inv." image and exit this function
                pyautogui.locateCenterOnScreen(imgs.mining_completed_img, confidence=0.90)
                print("Mining is completed")
                return
        except:
            pass
    # In case timer ends, retrieve drones and end mining function
    drone.retrieve_drones()
    print("Mining is completed")

def mining_lasers_off()->None:
    """
    Turn off mining lasers
    return:
        None
    """

    # Define base variables
    x = -100
    y = 50

    # Try to locate laser mining icos
    # TODO: Add different laser icons for different lasr types
    while True:
        try:
            # Try locating and clicking lasers, if no lasers found, break the loop
            print("Clicking lasers")
            mouse_action(imgs.mining_laser, "click", rand_moves=0, offset_x=x, offset_y=y)
            time.sleep(1)
            mouse_action(imgs.mining_laser, "click", rand_moves=0, offset_x=x, offset_y=y)
            print("Clicked lasers")
            break
        except:
            print("No lasers on")
            break

def mining_lasers_on()->None:
    """
    Handles modules and tools user for mining operations. Clears "Ghost mining" where lasers would 
    mine depleted asteroid and prevent correct laser initiation for next mining round. Handles
    drone operations
    return:
        None
    """

    # Turns off mining lasers if they are on (by clicking icons next to asteroid if available)
    mining_lasers_off()

    # Retrieves drones
    drone.retrieve_drones()

    # Reselect asteroid in case some other was selected while function tried to turn off lasers
    # and none where on
    mouse_action(imgs.mining_tab_img, "click", offset_y=50, confidence=0.95)

    # Locking in target and starting lasers
    pyautogui.press("ctrl")
    time.sleep(0.5)
    pyautogui.press("f1")
    time.sleep(1)
    pyautogui.press("f2")

def mouse_action(img:str, click_type:str, offset_x:int=0, offset_y:int=0, rand_moves=3, confidence=0.85)-> None:
    """
    Handles click, rightClick and move mouse actions by adding error handling,
    try checks.
    args:
        img: path of an image to look for,
        click_type: what click type to use on the image,
        offset_x: offsets x mouse position from images center, defauilt 0,
        offset_y: offsets y mouse position from images center, defauilt 0,
        rand_moves: maximum number of random mouse movements, default 3,
        confidence: how confident in image should identifier be, default 0.85
    return:
        None    
    """
    # To implement randomnes in how fast mouse moves in various situations
    random_delay = round(random.uniform(0.5, 1))

    # Random number of random movements, to keep things random
    random_number_of_random_movements = random.randint(0, rand_moves)
    try:
        # Move mouse randomly ammount of time it should run randomly
        random_movement(random_number_of_random_movements)

        # Locate coordinates
        x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence)

        # Add offset if any
        x += offset_x
        y += offset_y

        # Information printing
        print(f"Moving mouse to: \"{img}\" image")

        # Move mouse to target position, easing in and out when moving
        pyautogui.moveTo(x, y, duration=random_delay, tween=pyautogui.easeInOutQuad)

        # Random delay not to click button right away
        time.sleep(random_delay)

        # For different click_type do different action
        match click_type:
            case "click":
                pyautogui.click()
            case "rightClick":
                pyautogui.rightClick()
            case "move":
                return
            case _:
                return
        
    # Exception handling
    except ImageNotFoundException as e:
        print(f"error: {e}")
        try:
            # Try to capture a screenshot if possible
            pyautogui.screenshot(f"{config.root_path}\\auto_miner\\error_screenshots\\screenshot.png")
        except:
            print("Failed capturing a screenshot")

    # Additional idle time
    time.sleep(random_delay)

def orbit_screen_once(drag_by=80)->None:
    """
    Handles actions needed to rotate screen view in space
    args:
        drag_by: How much should rotate the screen
    return:
        None
    """

    # Where to move mouse to initially
    starting_x = 950
    starting_y = 100

    # Move mouse and drag it
    pyautogui.moveTo(starting_x, starting_y, duration=0.3, tween=pyautogui.easeInOutQuad)
    pyautogui.dragTo(starting_x - drag_by, starting_y, duration=0.3, button="left")

    time.sleep(1)

def random_movement(points:int=1)-> None:
    """
    Adds random movement that do not add value to automation, but
    mimics more random human like behavior.
    args:
        points: An integer number of points mouse should visit
    return: 
        None
    """
    # Defines area in which to move mouse
    screen_width = 1500
    screen_height = 800

    # Move mouse as many times as presented in arguments
    for _ in range(points):
        # Defining next target coordinates
        rand_x = round(random.randint(400,screen_width))
        rand_y = round(random.randint(200,screen_height))
        # Movement
        pyautogui.moveTo(rand_x, rand_y, duration=0.5)

def traveling(retriever=False)-> None:
    """
    Minimises idle time when ship is traveling in between asteroids
    args:
        retriever: Flag that determines if user uses "Retriever" type of ship
    return:
        None
    """
    # Define basic variables
    approach_time = 60
    counter = 0

    if retriever:
        approach_time = 180 

    # Initial wait before flying speed is appearing on the screen
    time.sleep(10)

    # Have a fixed ammount of maximum travel time to break infinite loops in case indication fails
    while counter < approach_time:
        try:
            # Checks console window to see if any asteroids are targeted
            print("looking for target marks")
            targeted = pyautogui.locateOnScreen(imgs.target_image_bigger, confidence=0.90)

            # if target mark found, exit loop
            if targeted:
                print("found target mark")
                break
        except:
            try:
                # If failed to find target mark, try to find a different target mark icon
                target = pyautogui.locateOnScreen(imgs.target_image_smaller, confidence=0.90)
                if target:
                    print("found target mark")
                    break
            except:
                # If failed to find any of the marks, try to target the asteroid
                print("Trying to target asteroid")
                pyautogui.press('ctrl')
                counter += 1
                time.sleep(4)

    # When target mark is achieved, next we check if laser can reach
    while counter < approach_time:
        try:
            # Try to toggle laser 1
            pyautogui.press('f1')
            
            # Small delay for information window to appear on failure to mine due to large distance
            time.sleep(2)

            # If message box appears, wait for 15 seconds, increment timer and try again
            pyautogui.locateOnScreen(imgs.too_far_to_mine_img, confidence=0.80)
            time.sleep(15)
            counter += 1
        except:
            # If failed to locate error message, means laser is on, so turning it off and exiting the loop
            pyautogui.press('f1')
            break

    print("Next asteroid is in reach")

def warp_rest_timer(handle_drones=True)-> None:
    """
    Manages warping rest time. Rests while warp. Solves issue with fixed warp time, where
    ship would wait till general time.sleep would end for short warps
    return:
        None
    """
    # Retrieve drones before warping if possible
    if handle_drones:
        drone.retrieve_drones()

    # First check for indicator is to see if ship has started warping
    # in some cases ships are stuck begind asteroids and initiating warp drive
    # takes minutes
    if not locate_indicators(imgs.warping_text, confidence=0.9):
        print("Failed to see the \"warping\" indicator")

    # After ship is in warping state, check when this state ends
    while not locate_indicators(imgs.warping_text, confidence=0.9):
        print("Warping")

    # Some indicators are located when ships "Warping" text is gone, but ship is still
    # exiting warping state and script cant make further actions, so we need this delay
    # to account for that
    time.sleep(5)

    print("Warping completed")
