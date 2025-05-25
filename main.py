from automations import ore_finder, inv_mover
import time
import random

if __name__ == "__main__":
    while True:
        sleep_checker = 0
        ore_finder.mine()
        inv_mover.move()
        if sleep_checker / 8 == 1:
            random_sleep_time = round(random.randint(500, 1500))
            print("Starting long sleep: {random_sleep_time} seconds")
            time.sleep(random_sleep_time)
            sleep_checker = 0
        else:
            sleep_checker += 1