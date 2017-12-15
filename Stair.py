import pygame
import random

class Stair:
    
    def __init__(self, main_width, count):
        """attributes of stair"""        
        type_number = random.randint(1, 20)
        if 1 <= type_number <= 11:
            self.type = "general"
        elif 12 <= type_number <= 15:
            self.type = "hurt"
        '''elif 16 <= type_number <= 20:
            self.type = "Moving" ''' 
        else:
            self.type = "cloud"

        
        self.width = 150   #假設圖片寬度是150
        self.height = 20  #假設圖片長度是20
        self.x = random.randint(19, main_width - self.width - 19) #19為背景圖的藍色邊寬 
        self.y = 640 - 75 * (8 - count)
        self.count = 0
    
    '''
    讓移動梯子左右移動
    def Moveing_x():
    '''

    def Update(self, person):
        """be touched or not and its reaction"""
        self.y -= 2    #所有樓梯不斷上升
        
        if self.y + self.height > (person.y + person.height - 2) > self.y and (self.x + 15) <= (person.x + person.width) <= (self.x + self.width + person.width - 15): #小朋友至少要有15像素在樓梯上上         
            if self.type == "general":
                self.count += 1
                person.General(self.count)
            elif self.type == "hurt":
                self.count += 1
                person.Hurt(self.count)
            '''elif self.type == "Moving":
                self.count += 1
                person.Moving(self.count)'''
            elif self.type == "cloud":
                    self.count += 1
                person.Cloud(self.count)
