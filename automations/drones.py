"""
Defines a Drones class that handles drone operations
"""

import pyautogui
import time

class Drones():
    def __init__(self):
        return

    def launch_drones(self)->None:
        """
        Launches drones
        return:
            None
        """
        pyautogui.keyDown("shift")
        pyautogui.write("f")
        pyautogui.keyUp("shift")
        time.sleep(3)
        pyautogui.write("f")

    def retrieve_drones(self)->None:
        """
        Retrieves drones
        return:
            None
        """
        print("Retrieving drones")
        time.sleep(2)
        pyautogui.keyDown("shiftleft")
        time.sleep(0.5)
        pyautogui.write("r")
        time.sleep(0.5)
        pyautogui.keyUp("shiftleft")
        time.sleep(10)
