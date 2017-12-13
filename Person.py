import pygame
import Helper

display_width = None
display_height = None

class Person:

    def Hurt(self, stair):
        ''' 人碰到刺刺梯子時 '''
        if self.stair is not stair:
            self.ReduceLife()

    def Cloud(self, stair):
        ''' 人碰到消失梯子 '''
        # If cloud was not the same cloud as last time, reset count
        if self.stair is not stair:
            self.cloud_count = 5
        else:
            # Reduce count and check if below threshold
            self.cloud_count -= 1
            if self.cloud_count <= 0:
                self.y += 14

    def HitStair(self, stair):
        self.y += -7
        if self.stair is not stair:
            if self.life_count < 12:
                self.life_count += 1
        self.stair_reaction[stair.type](stair)

        self.stair = stair

    def ReduceLife(self, reduce = 5):            
        self.life_count -= reduce                   # 命減5
        if self.life_count <= 0:                    # 檢查是否死掉，死了就GameEnd
            Helper.GameEnd()

    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.x_change = 0     
        self.life_count = 12
        self.stair = None
        self.cloud_count = 5
        self.stair_reaction = {'general': Helper.EmptyFunction, 'hurt':self.Hurt, 'cloud':self.Cloud }
        
    '''
    def Photo(self):
        if i = 1:
            return picture1
        if i = 2: 
            return picture2 
    '''

    def Update(self, events):
        ''' Update person's moving and life '''
        # Event Handling
        for event in events:
            if event.type == pygame.KEYDOWN:            # 若按鍵被按下
                if event.key == pygame.K_LEFT:          # 按左鍵
                    self.x_change += -5
                if event.key == pygame. K_RIGHT:        # 按右鍵
                    self.x_change += 5
            if event.type == pygame.KEYUP:              # 若按鍵放開就不動
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.x_change = 0
        
        # Handles horizontal movements
        self.x += self.x_change
        # Check horizontal bounds
        if self.x <= 0:                                 # 碰到左邊邊線不動
            self.x = 0
        if self.x + self.width >= display_width * 0.6:  # 碰到右邊邊線不動
            self.x = display_width * 0.6 - self.width

        # Handles vertical Movement
        self.y += 5                                    # 自然落下
        if self.y > display_height:               # 落下超過下邊線就GameEnd
            Helper.GameEnd()

        if self.y <= 40:                                 # 若頭刺到上面刺刺
            self.y += 25                                # 繼續自然落下(從梯子上面被擠下)
            self.ReduceLife()

           


