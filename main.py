from automations import ore_finder, inv_mover
import time
import random
from pyautogui import ImageNotFoundException
from datetime import datetime

if __name__ == "__main__":
    while True:
        try:
            time.sleep(4)
            sleep_checker = 0
            ore_finder.excavate()
            inv_mover.move()
            if sleep_checker / 8 == 1:
                random_sleep_time = round(random.randint(500, 1500))
                print("Starting long sleep: {random_sleep_time} seconds")
                time.sleep(random_sleep_time)
                sleep_checker = 0
            else:
                sleep_checker += 1
        except Exception as e:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Faced an exception on {time}. \nError:{e}")
            break
