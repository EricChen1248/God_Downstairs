import pygame
import random
import Person

stair_list = None
border = 31
class Stair:
    
    def __init__(self, main_width, count):
        """attributes of stair"""        
        type_number = random.randint(1, 21)
        if 1 <= type_number <= 10:
            self.type = "general"
        elif 11 <= type_number <= 14:
            self.type = "hurt"
        elif 15 <= type_number <= 17:
            self.type = "cloud"
        elif 18 <= type_number <= 20:
            self.type = "moving"
        else:
            self.type = "blackhole"
    
        self.pass_through = False
        self.width = 150   #假設圖片寬度是150
        self.height = 20  #假設圖片長度是20
        self.x = random.uniform(border, main_width - border - self.width)
        self.y = 640 - 75 * (8 - count)
        if self.type == "moving":
            self.original_x = random.randint(border, main_width - border - self.width - 90)

            self.stair_speed = random.randint(10, 20) / 10
            self.x = random.randint(self.original_x, self.original_x + 90)

            self.hit_count = random.randint(0, 1) 
            if self.hit_count == 0:
                self.hit_count = -1
    
    def MovingStair_x(self, main_width):
        '''move right and left'''
        self.x += self.stair_speed * self.hit_count
        if self.x < self.original_x or self.x > self.original_x + 90:
            self.hit_count *= -1

    

    def Update(self, main_width):
        """be touched or not and its reaction"""
        self.y -= 2    #所有樓梯不斷上升
        if self.type == "moving":
            self.MovingStair_x(main_width)               

    def HitPersonUpdate(self, person):
        if self.pass_through:
            return

        if self.y + self.height > (person.y + Person.height - 1) > self.y and (self.x + 15) <= (person.x + Person.width) <= (self.x + self.width + Person.width - 15): #小朋友至少要有15像素在樓梯上                
            if self.type == "general":
                person.General(self)
            elif self.type == "hurt":
                person.Hurt(self)
            elif self.type == "cloud":
                person.Cloud(self)
            elif self.type == "moving":
                person.Moving(self)
            elif self.type == "blackhole":
                person.Blackhole(self)