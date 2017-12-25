import pygame
import random
import Person

width = 150
height = 20

stair_list = []
border_size = 31
class Stair:
    def __init__(self, main_width, count):
        """ Initialize Stairs """  
        # Generate random type      
        self.x = random.randint(border_size, main_width - width - border_size)  

        type_number = random.randint(0, 13)
        if 0 <= type_number <= 4:
            self.type = "Normal"
        elif type_number <= 7:
            self.type = "Spike"
        elif type_number <= 10:
            self.type = "Cloud"
        elif type_number <= 13:
            self.type = "Moving"
            self.horizontal_movement = 90
            self.left_bound = random.randint(border_size, main_width - width - border_size - self.horizontal_movement)
            self.move_direction = random.randint(0, 2)
            self.x = random.randint(self.left_bound, self.left_bound + self.horizontal_movement)
            if random.randint(0, 1) == 0 :
                self.move_direction *= -1

        self.y = 640 - 75 * (8 - count)
        self.fall_through = False
            
    def Update(self):
        """ Stair Update Function (Constantly moving up) """
        self.y -= 2

        if self.type == "Moving":
            self.MovingStair()
    
    def HitStair(self, person):
        """ Checks for collision with person """
        if self.y + height > (person.y + Person.height - 2) > self.y and\
           self.x <= (person.x + Person.width) <= (self.x + width + Person.width):         
            person.HitStair(self)

    def MovingStair(self):
        """ Handles moving stair movement """
        self.x += self.move_direction
        if self.x < self.left_bound or self.x > self.left_bound + self.horizontal_movement:
            self.move_direction *= -1
    


