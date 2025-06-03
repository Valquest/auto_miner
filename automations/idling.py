from datetime import datetime, time as Time
import random
import pyautogui
from automations.ore_finder import mining_lasers_off, mouse_action, warp
from config import config
import time

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

    @staticmethod
    def log_off():
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

        quit_radian_btn = f"{config.root_path}\\auto_miner\\screenshots\\resting\\quit.png"
        mouse_action(quit_radian_btn, "click", offset_x=-26, offset_y=-25)

        time.sleep(30)

    @staticmethod
    def log_in():
        """
        Logs user in
        """
        try:
            eve_launcher_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\eve_icon.png"
            mouse_action(eve_launcher_img, "click")

            play_now_btn_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\play_now.png"
            mouse_action(play_now_btn_img, "click")
        except:
            print("Failed to start the game. Either play now button or eve icon is not vissible on the screen.")
            exit(1)

        time.sleep(22)

        try:
            claim_gift_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\claim_gift.png"
            mouse_action(claim_gift_img, "click")
            close_gift_window_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\close_gift_window.png"
            mouse_action(close_gift_window_img, "click")
        except:
            try:
                print("Looking for an exit button for \"Claim your gift window\"")
                exit_gift_window_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\exit_gift_window.png"
                mouse_action(exit_gift_window_img, "click")
            except:
                print("Didnt find exit button, passing")
                pass

        player_character_img = f"{config.root_path}\\auto_miner\\screenshots\\resting\\character_selection.png"
        mouse_action(player_character_img, "click", offset_x=-283, offset_y=-471)

        # Check if warping
        warp()

    def anti_computer_sleep(self):
        try:
            pyautogui.moveTo(1000, 500)
            time.sleep(500)
            pyautogui.moveTo(1050, 500)
            time.sleep(500)
            print(f"Next log in at: {self.end_of_the_rest_time.hour}:{self.end_of_the_rest_time.minute}")
        except:
            print("Failed to move the mouse")
            return

