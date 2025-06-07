"""
This module stores Image_loader class, which handles image path loading for other modules
"""

from config import config

class Image_loader():
    """
    This is a singleton class that stores all image paths required by pyautogui to
    navigate the UI. All image paths are loaded upon initial class setup and are loaded only one time.
    Images paths can be accessed by any module, saving memory and adding convenience.
    """
    def __new__(cls):
        """
        Singleton class pattern that prevents creating new instances of this class, but
        rather accesses one and only instance that already exists in memory.
        """
        # Check if class has atribute called "instance"
        if not hasattr(cls, "instance"):
            # If instance atribute does not exist, do create the first instance of this class by accessing
            # parent class through super() method and invocing new class.
            cls.instance = super(Image_loader, cls).__new__(cls)
        # If class has "instance" attribute, than simply return it, returning class instance
        return cls.instance
    
    def __init__(self):
        """
        Image paths and loading 
        """

        # Setting up each screenshot directory path variable
        self.general_path = config.imgs_general
        self.inv_mover_path = config.imgs_inv_mover
        self.ore_finder_path = config.imgs_ore_finder
        self.resting_path = config.imgs_resting

        # Defining general paths
        self.refinery_btn = self.general_path + "refinery.png"
        self.open_cargo_btn = self.general_path + "open_cargo.png"

        # Defining inventory movers image paths
        self.mining_hold_btn = self.inv_mover_path + "mining_hold.png"


        self.quit_radian_btn = self.resting_path + "quit.png"
