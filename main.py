"""
Orchestrates all major activities for sucesfull mining
"""

import time

from automations import ore_finder, inv_mover, idling
from datetime import datetime
from pyautogui import ImageNotFoundException


if __name__ == "__main__":

    # Create a idle tracker
    idler = idling.Idler()

    # Keep looping untill indicated to stop
    while True:
        try:
            time.sleep(4)
            idler.rest()

            # Handles mining operations
            ore_finder.mine(retriever=True)

            # Handles inventory transfer form ship to refinery operations
            inv_mover.items_to_refinery()

        # Handles exceptions
        except ImageNotFoundException as e:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Faced an exception on {time}. \nError:{e}")
            break
        except Exception as e:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Faced an exception on {time}. \nError:{e}")
            break
