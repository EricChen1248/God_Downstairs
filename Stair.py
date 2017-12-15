import pygame
import random
import Person

width = 150
height = 20

stair_list = []

class Stair:
    def __init__(self, main_width, count):
        """ Initialize Stairs """  
        # Generate random type      
        type_number = random.randint(0, 10)
        if 0 <= type_number <= 4:
            self.type = "Normal"
        elif 5 <= type_number <= 7:
            self.type = "Spike"
        else:
            self.type = "Cloud"

        self.x = random.randint(31, main_width - width - 31)  
        self.y = 640 - 75 * (8 - count)
        self.fall_through = False
            
    def Update(self):
        """ Stair Update Function (Constantly moving up) """
        self.y -= 2
    
    def HitStair(self, person):
        """ Checks for collision with person """
        if self.y + height > (person.y + Person.height - 2) > self.y and\
           self.x <= (person.x + Person.width) <= (self.x + width + Person.width):         
            person.HitStair(self)
