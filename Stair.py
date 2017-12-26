import pygame
import random
import Person

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
    
        self.width = 150   #假設圖片寬度是150
        self.height = 20  #假設圖片長度是20
        self.x = random.uniform(border, main_width - border - self.width)
        self.y = 640 - 75 * (8 - count)
        self.count = 0
        if self.type == "moving":
            self.original_x = random.randint(border, main_width - border - self.width - 90)

            self.x = random.randint(self.original_x, self.original_x + 90)

            self.hit_count = random.randint(0, 1) 
    
    def MovingStair_x(self, main_width):
        '''move right and left'''
        
        def GelGroup(self):
            if self.hit_count == 0:
                if self.x + 0.8 < self.original_x + 90:
                    self.x += 0.8
                else:
                    self.hit_count = 1
            elif self.hit_count == 1:
                if self.x - 0.8 > self.original_x:
                    self.x -= 0.8
                else:
                    self.hit_count = 0

        GelGroup(self)
        
    

    def Update(self, main_width):
        """be touched or not and its reaction"""
        self.y -= 2    #所有樓梯不斷上升
        if self.type == "moving":
            self.MovingStair_x(main_width)               

    def HitPersonUpdate(self, person):
        if self.y + self.height > (person.y + Person.height - 1) > self.y and (self.x + 15) <= (person.x + Person.width) <= (self.x + self.width + Person.width - 15): #小朋友至少要有15像素在樓梯上上         
            adjust_y = person.y + Person.height - self.y + 3        #小朋友插入梯子的深度，3是調整數
                       
            if self.type == "general":
                person.General(self, adjust_y)
            elif self.type == "hurt":
                person.Hurt(self, adjust_y)
            elif self.type == "cloud":
                self.count += 1
                person.Cloud(self, self.count, self.x)
            elif self.type == "moving":
                person.Moving(self, self.hit_count, adjust_y)
            elif self.type == "blackhole":
                person.Blackhole(self, adjust_y)