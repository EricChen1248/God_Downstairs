import random

class Stair:
    
    def __init__(self, width):
        x = random.randint(0, width - 25)  #假設圖片的長度是25
        y = 0
        type_number = random.randint(0, 2)
        if type_number == 0:
            type = "general"
            photo_link = "xxx.png"     #連結到不同樓梯的圖
        elif type_number == 1:
            type = "hurt"
            photo_link = "xxx.png"
        else:
            type = "cloud"
            photo_link = "xxx.png"
            
    def Update():
        """be touched or not and its reaction"""
        if x <= Person.x <= (x + 25):
            if type = "cloud":
                y += 10            #樓梯繼續上升
            elif type = "general":
                reaction = Person.General()
            else:
                reaction = Person.Hurt()
        else:
            y += 10
    
