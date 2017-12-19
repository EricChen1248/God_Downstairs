import pygame
import Tool
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

        
        for event in events:
            if event.type == pygame.KEYDOWN:            # 若按鍵被按下
                if who == 1:
                    if event.key == pygame.K_LEFT:          # 按左鍵
                        self.direction.append(-5)
                    if event.key == pygame. K_RIGHT:        # 按右鍵
                        self.direction.append(5)
                if who == 2:
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
                if who == 2:
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
        if self.x <= 0:                                 # 碰到左邊邊線不動
            self.x = 0
        if self.x + width >= self.display_width * 0.6:  # 碰到右邊邊線不動
            self.x = self.display_width * 0.6 - width

        # Handles verticla Movement
        self.y += 5                                    # 自然落下
        if self.y > self.display_height:               # 落下超過下邊線就GameEnd
            Tool.GameEnd()
        if self.y <= 40:                                 # 若頭刺到上面刺刺
            self.y += 25                                # 繼續自然落下(從梯子上面被擠下)
            self.life_count += -5                       # 命減5
            if self.life_count <= 0:                    # 檢查是否死掉，死了就GameEnd
                Tool.GameEnd()

    def General(self,count):
        ''' 人碰到一般梯子時 '''
        self.y += -7                                   # 若梯子是-10往上，要抵銷自然落下就要-20
        if count == 1:
            if self.life_count < 12:                        # 若沒滿血就加一
                self.life_count += 1
            
    def Hurt(self, count):
        ''' 人碰到刺刺梯子時 '''
        self.y += -7
        if count == 1:
            self.life_count += -5                           # 命減5
            if self.life_count <= 0:                       # 檢查是否死掉，死了就GameEnd
                Tool.GameEnd()

    def Cloud(self, count):
        ''' 人碰到消失梯子 '''
        if count == 1:
            if self.life_count < 12:                        # 若沒滿血就加一
                self.life_count += 1

        if count <= 10:
            self.y += -7
    def Moving(self, count, hit_count):
        self.x += 0.8 - hit_count * 1.6                     # hit_count用來決定向左或向右
        self.y += -7
        if count == 1:                                      # 若沒滿血就加一
            if self.life_count < 12:                        
                self.life_count += 1

    


