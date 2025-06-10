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
        self.transfer_btn = self.inv_mover_path + "transfer.png"
        self.empty_inv_indicator = self.inv_mover_path + "no_more_items.png"
        self.stack_all_btn = self.inv_mover_path + "stack_all.png"
        self.item_drop_destination = self.inv_mover_path + "drop_items_here.png"

        # Defining ore finder directory paths
        self.mining_tab_img = self.ore_finder_path + "mining_tab.png"
        self.warp_btn = self.ore_finder_path + "warp_to_within.png"
        self.asteroid_belt_btn = self.ore_finder_path + "asteroid_belt.png"
        self.warping_text = self.ore_finder_path + "warping_text.png"
        self.mining_completed_img = self.ore_finder_path + "mining_completed.png"
        self.mining_completed_retriever_img = self.ore_finder_path + "mining_completed_retriever.png"
        self.asteroid_depleted_img = self.ore_finder_path + "depleted.png"
        self.mining_in_progress_img = self.ore_finder_path + "in_mining_process.png"
        self.target_image_bigger = self.ore_finder_path + "Target_Locked_In_Bigger.png"
        self.target_image_smaller = self.ore_finder_path + "Target_Locked_In_Smaller.png"
        self.too_far_to_mine_img = self.ore_finder_path + "strip_miner_too_far.png"
        self.mining_laser = self.ore_finder_path + "mining_laser_starting_point.png"

        # Defining resting directory image paths
        self.eve_launcher_btn = self.resting_path + "eve_icon.png"
        self.play_now_btn = self.resting_path + "play_now.png"
        self.claim_gift_btn = self.resting_path + "claim_gift.png"
        self.close_gift_window_btn = self.resting_path + "close_gift_window.png"
        self.exit_gift_window_btn = self.resting_path + "exit_gift_window.png"
        self.player_character_img_btn = self.resting_path + "character_selection.png"
        self.quit_radian_btn = self.resting_path + "quit.png"
