"""
Handles actions needed to move inventory from ship to refinery
"""

import pyautogui
import random
import time

from automations import ore_finder
from assets.image_loader import Image_loader
from pyautogui import ImageNotFoundException

# Create an image loader instance to access image paths
imgs = Image_loader()

def drag_items_to_refinery_inv()->None:
    """
    Item icon draging from one inv. to another
    return:
        None
    """
    # Add randomness in where mouse click each time to avoid robot like behavior
    random_num = round(random.uniform(0.5, 1.5))
    try:
        x, y = pyautogui.locateCenterOnScreen(imgs.item_drop_destination, confidence=0.85)
        pyautogui.dragTo(x, y - 200 + random_num, duration=random_num, button='left')
    except ImageNotFoundException:
        print("Failed to drag items from ships inv. to refineries inv. Failed to locate image: {imgs.item_drop_destination}")

def items_to_refinery()->None:
    """
    Handles action chain for moving ships inventory to refineries inventory
    return:
        None
    """
    # TODO: Remove pre-sleep from action chain
    time.sleep(2)

    # Right click refinery button
    ore_finder.mouse_action(imgs.refinery_btn, "rightClick")

    # Click cargo button
    ore_finder.mouse_action(imgs.open_cargo_btn, "click")

    # Stack items to refresh order in inventory
    stack_items()
    
    # Loops inventory moving based on number of different ores there are
    while True:
        try:
            # Check if all items were already moved, if yes, exit while loop
            pyautogui.locateOnScreen(imgs.empty_inv_indicator, confidence=0.90)
            break
        except:
            # Move mouse to item in ships inv.
            ore_finder.mouse_action(imgs.mining_hold_btn, "move", offset_x=120, rand_moves=0)

            # Click and drag item to transfering window
            drag_items_to_refinery_inv()

            # Give some time for "Transfer" buttons animation to load button in       
            time.sleep(1)

            # Click 'Transfer' button
            ore_finder.mouse_action(imgs.transfer_btn, "click", rand_moves=0)

def stack_items()->None:
    """
    Stacks items in ships inventory
    return:
        None
    """
    ore_finder.mouse_action(imgs.mining_hold_btn, "rightClick", offset_x=175, rand_moves=0)
    ore_finder.mouse_action(imgs.stack_all_btn, "click", rand_moves=1)
