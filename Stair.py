import pygame
import random
import Person

border = 31
class Stair:
    
    def __init__(self, main_width, count):
        """attributes of stair"""        
        type_number = random.randint(1, 20)
        if 1 <= type_number <= 10:
            self.type = "general"
        elif 11 <= type_number <= 14:
            self.type = "hurt"
        elif 15 <= type_number <= 17:
            self.type = "cloud"
        else:
            self.type = "moving"

        
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
        def HitRightGroup(self):
            if self.hit_count == 0:
                #還沒撞到右邊邊線
                if self.x + self.width + 0.8 < main_width - border:
                    self.x += 0.8
                elif self.x + self.width + 0.8 >= main_width - border:
                    self.hit_count = 1
                
            elif self.hit_count == 1:
                #還沒撞到左邊邊線
                if self.x - 0.8 > self.original_x - 90: #左邊界線是初始位向左90
                    self.x -= 0.8
                elif self.x - 0.8 <= self.original_x:
                    self.hit_count = 0
        
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
        
        

    def Update(self, person, main_width):
        """be touched or not and its reaction"""
        self.y -= 2    #所有樓梯不斷上升
        if self.type == "moving":
            self.MovingStair_x(main_width)
                

        if self.y + self.height > (person.y + Person.height - 2) > self.y and (self.x + 15) <= (person.x + Person.width) <= (self.x + self.width + Person.width - 15): #小朋友至少要有15像素在樓梯上上         
            if self.type == "general":
                self.count += 1
                person.General(self.count)
            elif self.type == "hurt":
                self.count += 1
                person.Hurt(self.count)
            elif self.type == "cloud":
                self.count += 1
                person.Cloud(self.count)
            elif self.type == "moving":
                self.count += 1
                person.Moving(self.count, self.hit_count)
                #person.General(self.count)