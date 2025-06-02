import time
from automations import ore_finder, idling
import pyautogui
from config import config


time.sleep(2)

idling = idling.Idler()
while True:
    idling.rest()