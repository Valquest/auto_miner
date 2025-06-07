from datetime import datetime, time as Time
import random
import pyautogui
from automations.ore_finder import mining_lasers_off, mouse_action, wait_for_end_of_warp
from config import config
import time
from assets.image_loader import Image_loader

class Idler():
    """
    Handles player character resting. Loggs of at certain time and re-logs in when needed
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Idler, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.start_time = datetime.now()
        self.start_of_the_rest_time = Time(hour=11, minute=random.randint(1, 59), second=random.randint(1, 59))
        self.end_of_the_rest_time = Time(hour=14, minute=random.randint(1, 59), second=random.randint(1, 59))
        self.imgs = Image_loader()

    def rest(self):
        if self.is_time_to_rest():
            self.log_off()
            while self.is_time_to_rest():
                self.anti_computer_sleep()
            self.log_in()
            self.set_new_time_boundaries()
            return
        else:
            hours, minutes = self.rest_in()
            print(f"Time until rest: {hours} hour/s {minutes} minute/s")
            return

    def is_time_to_rest(self)-> bool:
        """
        Checks if it is time to rest
        """
        now = datetime.now().time()
        return now > self.start_of_the_rest_time and now < self.end_of_the_rest_time
    
    def set_new_time_boundaries(self):
        self.start_of_the_rest_time = Time(hour=11, minute=random.randint(1, 59), second=random.randint(1, 59))
        self.end_of_the_rest_time = Time(hour=14, minute=random.randint(1, 59), second=random.randint(1, 59))

    def rest_in(self)-> list[int]:
        """
        return:
            Hours and minutes until rest
        """
        if self.is_time_to_rest():
                return [0, 0]
            
        now = datetime.now().time()
        now_total_minutes = now.hour * 60 + now.minute
        rest_total_minutes = self.start_of_the_rest_time.hour * 60 + self.start_of_the_rest_time.minute
        
        if now_total_minutes > rest_total_minutes:
            return [0, 0]
        
        wait_time = rest_total_minutes - now_total_minutes
        hours_to_wait = wait_time // 60
        minutes_to_wait = wait_time % 60
        
        return [hours_to_wait, minutes_to_wait]

    def log_off(self):
        """
        Clicks key combinations to turn off the game
        """
        pyautogui.keyDown("ctrl")
        pyautogui.press("space")
        pyautogui.keyUp("ctrl")

        time.sleep(2)

        pyautogui.keyDown("alt")
        pyautogui.keyDown("shift")
        pyautogui.press(".")
        pyautogui.keyUp("alt")
        pyautogui.keyUp("shift")

        quit_radian_btn = self.imgs.quit_radian_btn
        mouse_action(quit_radian_btn, "click", offset_x=-26, offset_y=-25)

        time.sleep(30)

    def log_in(self)->None:
        """
        Executes action chain to log user in to the game
        """
        print("Logging in")

        try:
            # Check if "Play Now" button is on screen. If not, EVE launcher might be hidden
            pyautogui.locateOnScreen(self.imgs.play_now_btn, confidence=0.90)

        except:
            # Click the game launcher button
            mouse_action(self.imgs.eve_launcher_btn, "click")

            # Click the play now button
            mouse_action(self.imgs.play_now_btn, "click")

        # Giving time to load the game and define the state
        load_timer = 30

        # Checks if gift window or login button appears first
        first_element_found = ""

        while load_timer >= 0:
            try:
                # Tries to find UI elements needed to login, if it fails, assume that gift popup window is open
                pyautogui.locateOnScreen(self.imgs.player_character_img_btn, confidence=0.90)
                first_element_found = "LOGIN"
                break
            except:
                pass

            try:
                pyautogui.locateOnScreen(self.imgs.exit_gift_window_btn, confidence=0.90)
                first_element_found = "CLAIM_GIFT"
                break
            except:
                pass

            # Decrement timer
            load_timer -= 1

        match first_element_found:
            case "LOGIN":
                mouse_action(self.imgs.player_character_img_btn, "click", offset_x=-283, offset_y=-471)
            case "CLAIM_GIFT":
                # Claim daily gift
                self.claim_daily_gift()
            case _:
                print("Could not click neither \"Claim gift\" nor login buttons")

        # Check if warping and wait until warping ends
        wait_for_end_of_warp()

    def claim_daily_gift(self)->None:
        # Try claiming gift. If not possible, try closing the gift window
        try:
            # Click the "Claim Gift" button if gift is ready for the day
            mouse_action(self.imgs.claim_gift_btn, "click")

            # Give time for buttons to load
            time.sleep(2)

            # After claiming, close the gift window
            mouse_action(self.imgs.close_gift_window_btn, "click")

        except:
            mouse_action(self.imgs.exit_gift_window_btn, "click")

    def anti_computer_sleep(self)->None:
        "Moves mouse left and right once"
        try:
            pyautogui.moveTo(1000, 500)
            time.sleep(500)
            pyautogui.moveTo(1050, 500)
            time.sleep(500)
            print(f"Next log in at: {self.end_of_the_rest_time.hour}:{self.end_of_the_rest_time.minute}")
        except:
            print("Failed to move the mouse")
            return

