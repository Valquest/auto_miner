import time
from automations import ore_finder, idling
import pyautogui
from config import config


time.sleep(4)

"""
Logs user in
"""
play_now_btn_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\play_now.png"
ore_finder.mouse_action(play_now_btn_img, "click")

time.sleep(22)

try:
    claim_gift_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\claim_gift.png"
    ore_finder.mouse_action(claim_gift_img, "click")
    close_gift_window_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\close_gift_window.png"
    ore_finder.mouse_action(close_gift_window_img, "click")
except:
    try:
        print("Looking for an exit button")
        exit_gift_window_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\exit_gift_window.png"
        ore_finder.mouse_action(exit_gift_window_img, "click")
    except:
        print("Didnt find exit button, passing")
        pass

player_character_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\character_selection.png"
ore_finder.mouse_action(player_character_img, "click", offset_x=-283, offset_y=-471)

# Check if warping
ore_finder.warp()