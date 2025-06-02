"""
Used as a utility tool for development. Allows me to find specific coordinates on where my mouse is, when I click space bar       
"""

from pynput import keyboard, mouse
import pyautogui

# Global variable to control the loop
stop_execution = False

# Define the keyboard event handler
def on_press(key):
    global stop_execution
    try:
        # Print mouse coordinates when spacebar is pressed
        if key == keyboard.Key.space:
            x, y = pyautogui.position()
            print(f"Mouse coordinates: ({x}, {y}) at {time.ctime()}")
            
        # Stop the loop when Ctrl is pressed (either left or right Ctrl)
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            print("Ctrl pressed. Stopping execution...")
            stop_execution = True
            return False  # Stop the listener
    except AttributeError:
        pass

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Infinite loop until Ctrl is pressed
print("Press spacebar to get mouse coordinates, Ctrl to stop.")
import time
while not stop_execution:
    time.sleep(0.1)  # Small delay to reduce CPU usage

# Cleanup
listener.stop()
print("Script stopped.")  