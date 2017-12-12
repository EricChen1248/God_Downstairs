import random

class Stair:
    
    def __init__(self, main_width):
        """attributes of stair"""        
        type_number = random.randint(0, 2)
        if type_number == 0:
            self.type = "general"
            self.photo = "xxx.png"     #連結到不同樓梯的圖
        elif type_number == 1:
            self.type = "hurt"
            self.photo = "xxx.png"
        else:
            self.type = "cloud"
            self.photo = "xxx.png"
        
        self.width = 25   #假設圖片寬度是25
        self.height = 10  #假設圖片長度是10
        self.x = random.randint(0, main_width - self.width)  
        self.y = self.length
            
    def Update():
        """be touched or not and its reaction"""
        y -= 10    #所有樓梯不斷上升
        if (Person.y + Person.height) == self.y and self.x <= (Person.x + Person.width) <= (self.x + self.width + Person.width):         
            if self.type = "general":
                Person.General()
            elif self.type = "hurt":
                Person.Hurt()
    