import time
from automations import ore_finder, idling, drones
import pyautogui
from config import config
from assets import image_loader

imgs = image_loader.Image_loader()


def log_in()->None:
        """
        Executes action chain to log user in to the game
        """
        print("Logging in")

        try:
            # Check if "Play Now" button is on screen. If not, EVE launcher might be hidden
            pyautogui.locateOnScreen(imgs.play_now_btn, confidence=0.90)

            # Click the play now button
            ore_finder.mouse_action(imgs.play_now_btn, "click", rand_moves=0)

        except:
            # Click the game launcher button
            ore_finder.mouse_action(imgs.eve_launcher_btn, "click", rand_moves=0)

            # Click the play now button
            ore_finder.mouse_action(imgs.play_now_btn, "click", rand_moves=0)

        # Giving time to load the game and define the state
        load_timer = 30

        # Checks if gift window or login button appears first
        first_element_found = ""

        print("Starting game loading timer")

        while load_timer >= 0:
            try:
                print("Trying to find element 1")
                # Tries to find UI elements needed to login, if it fails, assume that gift popup window is open
                pyautogui.locateOnScreen(imgs.player_character_img_btn, confidence=0.90)
                print("Found")
                first_element_found = "LOGIN"
                break
            except:
                pass

            try:
                print("Trying to find element 2")
                pyautogui.locateOnScreen(imgs.claim_gift_btn, confidence=0.90)
                print("Found")
                first_element_found = "CLAIM_GIFT"
                break
            except:
                pass

            # Decrement timer
            load_timer -= 1
            time.sleep(1)

        match first_element_found:
            case "LOGIN":
                ore_finder.mouse_action(imgs.player_character_img_btn, "click", offset_x=-283, offset_y=-471, rand_moves=0)
            case "CLAIM_GIFT":
                # Claim daily gift
                claim_daily_gift()
            case _:
                print("Could not click neither \"Claim gift\" nor login buttons")

        # Check if warping and wait until warping ends
        ore_finder.wait_for_end_of_warp()

def claim_daily_gift()->None:
        # Try claiming gift. If not possible, try closing the gift window
        try:
            # Click the "Claim Gift" button if gift is ready for the day
            ore_finder.mouse_action(imgs.claim_gift_btn, "click")

            # Give time for buttons to load
            time.sleep(2)

            # After claiming, close the gift window
            ore_finder.mouse_action(imgs.close_gift_window_btn, "click")

        except:
            ore_finder.mouse_action(imgs.exit_gift_window_btn, "click")

time.sleep(4)

log_in()