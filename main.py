from automations import ore_finder, inv_mover, idling
import time
import random
from pyautogui import ImageNotFoundException
from datetime import datetime

if __name__ == "__main__":

    # Create a idle tracker
    idler = idling.Idler()

    while True:
        try:
            time.sleep(4)
            idler.rest()
            ore_finder.mine(retriever=True)
            inv_mover.items_to_refinery()
        except ImageNotFoundException as e:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Faced an exception on {time}. \nError:{e}")
            break
        except Exception as e:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Faced an exception on {time}. \nError:{e}")
            break
