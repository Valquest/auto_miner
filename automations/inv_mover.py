import pyautogui
import time
import random

def move():
    random_num = round(random.randint(3, 5))
    time.sleep(2)
    refinery_img_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\inv_mover\\refinery.png"
    x, y = pyautogui.locateCenterOnScreen(refinery_img_path, confidence=0.85)
    pyautogui.moveTo(x + random_num, y, duration=random_num)
    time.sleep(1)
    pyautogui.rightClick()
    time.sleep(2)
    open_cargo_img_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\inv_mover\\open_cargo.png"
    x, y = pyautogui.locateCenterOnScreen(open_cargo_img_path, confidence=0.85)
    time.sleep(0.5)
    pyautogui.moveTo(x + random_num, y, duration=random_num)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    veldspar_inv_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\inv_mover\\mining_hold.png"
    x, y = pyautogui.locateCenterOnScreen(veldspar_inv_path, confidence=0.85)
    pyautogui.moveTo(x, y, duration=random_num)
    time.sleep(0.5)
    pyautogui.move(120, 0, duration=random_num)
    time.sleep(1)
    refinery_inv_img_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\inv_mover\\drop_items_here.png"
    x, y = pyautogui.locateCenterOnScreen(refinery_inv_img_path, confidence=0.85)
    pyautogui.dragTo(x, y - 200 + random_num, duration=random_num, button='left')
    time.sleep(1)
    transfer_image_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\inv_mover\\transfer.png"
    x, y = pyautogui.locateCenterOnScreen(transfer_image_path, confidence=0.85)
    pyautogui.moveTo(x + random_num, y, duration=0.5)
    time.sleep(0.5)
    pyautogui.click()