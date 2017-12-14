import pygame
import random
import Person

width = 150
height = 20
class Stair:
    
    def __init__(self, main_width, count):
        """ Attributes of stair """        
        type_number = random.randint(0, 10)
        if 0 <= type_number <= 4:
            self.type = "general"
        elif 5 <= type_number <= 7:
            self.type = "hurt"
        else:
            self.type = "cloud"

        
        self.width = width      # 假設圖片寬度是150
        self.height = height    # 假設圖片長度是20
        self.x = random.randint(0, main_width - self.width)  
        self.y = 640 - 75 * (8 - count)
        self.count = 0
            
    def Update(self):
        """ be touched or not and its reaction """
        self.y -= 2             # 所有樓梯不斷上升
    
    def HitStair(self, person):
        if self.y + self.height > (person.y + Person.height - 2) > self.y and self.x <= (person.x + Person.width) <= (self.x + self.width + Person.width):         
            person.HitStair(self)
