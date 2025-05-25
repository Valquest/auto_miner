import pyautogui
import time
import random

def mine():
    image_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\mining_tab.png"
    warp_image_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\warp_to_within.png"
    home_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\home.png"
    random_num = round(random.randint(3, 5))
    time.sleep(1)
    print("Locating")
    x, y = pyautogui.locateCenterOnScreen(image_path, confidence=0.85)
    print("Moving mouse")
    pyautogui.moveTo(x, y, duration=random_num)
    time.sleep(0.5)
    pyautogui.move(0, 50, duration=0.5)
    time.sleep
    pyautogui.rightClick()
    time.sleep(1)
    x, y = pyautogui.locateCenterOnScreen(warp_image_path, confidence=0.85)
    pyautogui.click(x + random_num, y, duration=0.5)
    time.sleep(2)
    time.sleep(17)
    pyautogui.press("ctrl")
    time.sleep(2.5)
    pyautogui.press("f1")
    time.sleep(0.5)
    pyautogui.press("f2")
    timer = 0
    asteroid_depleted = False
    asteroid_depleted_img_path = "C:\\Users\\Dovyd\\Coding\\auto_miner\\screenshots\\ore_finder\\depleted.png"
    while timer < 865 and not asteroid_depleted:
        try:
            coords = pyautogui.locateCenterOnScreen(asteroid_depleted_img_path, confidence=0.7)
            if coords:  # If image is found
                asteroid_depleted = True
        except pyautogui.ImageNotFoundException:
            timer += 1
            time.sleep(1)
            print(f"Timer at: {timer}")
    print("Done mining")
    x, y = pyautogui.locateCenterOnScreen(home_path, confidence=0.85)
    pyautogui.moveTo(x + random_num, y, duration=1.5)
    time.sleep(0.5)
    pyautogui.rightClick()
    time.sleep(random_num)
    x, y = pyautogui.locateCenterOnScreen(warp_image_path, confidence=0.85)
    pyautogui.moveTo(x + random_num, y, duration=0.5)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(17)
