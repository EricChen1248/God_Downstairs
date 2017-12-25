import pygame
import Tool
import math
width = 40
height = 60

class Person:
    def __init__(self, x, y, display_width, display_height, front, right, left):
        self.x = x
        self.y = y
        self.x_change = 0      
        self.life_count = 12
        self.display_width = display_width
        self.display_height = display_height
        self.direction = [0]
        self.left_photo = left
        self.right_photo = right
        self.front_photo = front
        self.photo = front  # 預設開始是 正面
        self.alive = True
    '''
    def Photo(self):
        if i = 1:
            return picture1
        if i = 2: 
            return picture2 
    '''
        
    def Update(self, who, events):
        ''' Update person's moving and life '''
        # Event Handling
        if self.alive == False:
            return 
        for event in events:
            if event.type == pygame.KEYDOWN:            # 若按鍵被按下
                if who == 1:
                    if event.key == pygame.K_LEFT:          # 按左鍵
                        self.direction.append(-5)
                    if event.key == pygame. K_RIGHT:        # 按右鍵
                        self.direction.append(5)
                elif who == 2:
                    if event.key == pygame.K_a:          # 按左鍵
                        self.direction.append(-5)
                    if event.key == pygame. K_d:        # 按右鍵
                        self.direction.append(5)
            if event.type == pygame.KEYUP:              # 若按鍵放開就不動
                if who == 1:
                    if event.key == pygame.K_LEFT:
                        self.direction.remove(-5)
                    elif event.key == pygame.K_RIGHT:
                        self.direction.remove(5)
                elif who == 2:
                    if event.key == pygame.K_a:
                        self.direction.remove(-5)
                    elif event.key == pygame.K_d:
                        self.direction.remove(5)
                        
        # Handles horizontal movements
        self.x += self.direction[-1]
        if self.direction[-1] == 5:
            self.photo = self.right_photo
        elif self.direction[-1] == -5:
            self.photo = self.left_photo
        else:
            self.photo = self.front_photo

        # Check horizontal bounds
        if self.x <= 31:                                 # 碰到左邊邊線不動
            self.x = 31
        if self.x + width >= self.display_width * 0.6 - 31:  # 碰到右邊邊線不動
            self.x = self.display_width * 0.6 - width - 31

        # Handles verticla Movement
        self.y += 5                                    # 自然落下
        if self.y > self.display_height:               # 落下超過下邊線就GameEnd
            self.Death()
        if self.y <= 40:                                 # 若頭刺到上面刺刺
            Tool.sounds["Hurt"].play()
            self.y += 25                                # 繼續自然落下(從梯子上面被擠下)
            self.life_count += -5                       # 命減5
            if self.life_count <= 0:                    # 檢查是否死掉，死了就GameEnd
                self.Death()

    def Death(self):
        Tool.sounds["Death"].play()
        self.alive = False
        self.life_count = 0
        self.y = 1000
        Tool.GameEndCount()

    def General(self,count, adjust_y):
        ''' 人碰到一般梯子時 '''                                
        if count == 1:
            self.y -= adjust_y
            if self.life_count < 12:                        # 若沒滿血就加一
                self.life_count += 1
        else:
            self.y += -7                                     # 若梯子是-10往上，要抵銷自然落下就要-20
    
            
    def Hurt(self, count, adjust_y):
        ''' 人碰到刺刺梯子時 '''
        if count == 1:
            self.y -= adjust_y
            Tool.sounds["Hurt"].play()
            self.life_count += -5                           # 命減5
            if self.life_count <= 0:                       # 檢查是否死掉，死了就GameEnd
                self.Death()
        else:
            self.y += -7

    def Cloud(self, count, adjust_y):
        ''' 人碰到消失梯子 '''
        if count == 1:
            self.y += 3
            if self.life_count < 12:                        # 若沒滿血就加一
                self.life_count += 1

        if count <= 10:
            self.y += -7

    def Moving(self, count, hit_count, adjust_y):
        self.x += 0.8 - hit_count * 1.6                     # hit_count用來決定向左或向右
        if count == 1:                                      # 若沒滿血就加一
            self.y -= adjust_y
            if self.life_count < 12:                        
                self.life_count += 1
        else:
            self.y += -7
                
def PersonInteraction(person_list):
    ''' 雙人版互動'''
    '''
    dx = person_list[0].x - person_list[1].x
    dy = person_list[0].y - person_list[1].y
    
    if abs(dx) < width and height - 5 < abs(dy) < height + 5:
        if person_list[0].y < person_list[1].y:
            person_list[0].y = person_list[1].y - height
        else:
            person_list[1].y = person_list[0].y - height
    elif width - 5 < abs(dx) < width + 5 and abs(dy) < height:
        delta_x = dx + width
        person_list[0].x -= delta_x // 2
        person_list[1].x += (delta_x - delta_x // 2)
            



    if abs(dx) < width and abs(dy) < height:
    #有重疊到
        delta_x = dx + width
        delta_y = dy + height
        if abs(delta_x) >= abs(delta_y):
            person_list[0].x -= delta_x // 2
            person_list[1].x += (delta_x - delta_x // 2)
        else:
            person_list[0].y -= delta_y
    '''
    dx = person_list[0].x - person_list[1].x
    dy = person_list[0].y - person_list[1].y
    delta_x = abs(dx) - width
    delta_y = abs(dy) - height
    if abs(dx) < width and abs(dy) < height:
        if abs(dx) > abs(dy):
            if person_list[0].x < person_list[1].x:
                person_list[0].x += delta_x // 2
                person_list[1].x -= (delta_x - delta_x // 2)
            else:
                person_list[0].x -= delta_x // 2
                person_list[1].x += (delta_x - delta_x // 2)            
        else:
            if person_list[0].y < person_list[1].y:
                person_list[0].y += delta_y
            else:
                person_list[1].y += delta_y
            
            

    


