import pyautogui
import time
import random
from automations import ore_finder, idling
from config import config
from assets.image_loader import Image_loader

imgs = Image_loader()

def items_to_refinery():

    time.sleep(2)

    # Right click refinery button
    ore_finder.mouse_action(imgs.refinery_btn, "rightClick")

    # Click cargo button
    ore_finder.mouse_action(imgs.open_cargo_btn, "click")

    # Define transfer items button (to refinery)
    transfer_image_path = f"{config.root_path}\\auto_miner\\screenshots\\inv_mover\\transfer.png"

    # Drag items from ships inv to refineries inv
    no_more_items_img = f"{config.root_path}\\auto_miner\\screenshots\\inv_mover\\no_more_items.png"
    while True:
        try:
            pyautogui.locateOnScreen(no_more_items_img, confidence=0.90)
            break
        except:
            # Stack items to refresh order in inventory
            stack_items()

            # Move mouse to item in ships inv.
            ore_finder.mouse_action(imgs.mining_hold_btn, "move", offset_x=120, rand_moves=0)

            # Drag item to transfering window
            drag_items_to_refinery_inv()

            # Click 'Transfer' button
            ore_finder.mouse_action(transfer_image_path, "click", rand_moves=0)
            

def stack_items():
    """
    Stacks items in ships inventory
    """
    stack_all_inv_path = f"{config.root_path}\\auto_miner\\screenshots\\inv_mover\\stack_all.png"

    ore_finder.mouse_action(imgs.mining_hold_btn, "rightClick", offset_x=175, rand_moves=0)
    ore_finder.mouse_action(stack_all_inv_path, "click", rand_moves=1)

def drag_items_to_refinery_inv():
    random_num = round(random.uniform(0.5, 1.5))
    refinery_inv_img_path = f"{config.root_path}\\auto_miner\\screenshots\\inv_mover\\drop_items_here.png"
    x, y = pyautogui.locateCenterOnScreen(refinery_inv_img_path, confidence=0.85)
    pyautogui.dragTo(x, y - 200 + random_num, duration=random_num, button='left')
    time.sleep(1)
