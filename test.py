import time
from automations import ore_finder, idling
import pyautogui
from config import config


time.sleep(2)

pyautogui.keyDown("shift")
pyautogui.write("f")
pyautogui.keyUp("shift")
time.sleep(3)
pyautogui.write("f")