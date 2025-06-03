import pyautogui
import time

class Drones():
    def __init__(self):
        return

    def launch_drones(self):
        pyautogui.keyDown("shift")
        pyautogui.write("f")
        pyautogui.keyUp("shift")
        time.sleep(3)
        pyautogui.write("f")

    def retrieve_drones(self):
        pyautogui.keyDown("shift")
        time.sleep(0.5)
        pyautogui.write("r")
        pyautogui.keyUp("shift")
        time.sleep(20)

    