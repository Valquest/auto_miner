from datetime import datetime
import random

class Idler():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Idler, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.start_time = datetime.now()
        self.start_of_the_rest_time = datetime.time(hour=11, minute=random.randint(1, 59), second=random.randint(1, 59))
        self.end_of_the_rest_time = datetime.time(hour=14, minute=random.randint(1, 59), second=random.randint(1, 59))

    def is_time_to_rest(self)-> bool:
        """
        Checks if it is time to rest
        """
        now = datetime.now().time()
        return now > self.start_of_the_rest_time and now < self.end_of_the_rest_time
    
    def set_new_time_boundaries(self):
        self.start_of_the_rest_time = datetime.time(hour=11, minute=random.randint(1, 59), second=random.randint(1, 59))
        self.end_of_the_rest_time = datetime.time(hour=14, minute=random.randint(1, 59), second=random.randint(1, 59))

    def rest_in(self)-> list[int]:
        """
        return:
            Hours and minutes until rest
        """
        if self.is_time_to_rest():
                return [0, 0]
            
        now = datetime.now().time()
        now_total_minutes = now.hour * 60 + now.minute
        rest_total_minutes = self.start_of_the_rest_time.hour * 60 + self.start_of_the_rest_time.minute
        
        if now_total_minutes > rest_total_minutes:
            return [0, 0]
        
        wait_time = rest_total_minutes - now_total_minutes
        hours_to_wait = wait_time // 60
        minutes_to_wait = wait_time % 60
        
        return [hours_to_wait, minutes_to_wait]
