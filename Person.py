import pygame
import Helper
import Stair

display_width = None
display_height = None

width = 40
height = 40

dead_count = 2
class Person:

    def Hurt(self, stair):
        ''' 人碰到刺刺梯子時 '''
        if self.stair is not stair:
            self.UpdateLife(-6)

    def Cloud(self, stair):
        ''' 人碰到消失梯子 '''
        # If cloud was not the same cloud as last time, reset count
        if self.stair is not stair:
            self.cloud_count = 5
        else:
            # Reduce count and check if below threshold
            self.cloud_count -= 1
            if self.cloud_count <= 0:
                stair.fall_through = True

    def HitStair(self, stair):
        self.y = stair.y - height
        if self.stair is not stair:
            self.UpdateLife(1)
        self.stair_reaction[stair.type](stair)

        self.stair = stair

    def UpdateLife(self, reduce = -5):            
        self.life_count += reduce                   # 命減5
        if self.life_count > 12:
            self.life_count = 12
        if self.life_count <= 0:                    # 檢查是否死掉，死了就GameEnd
            self.Death()
        Helper.UpdateLife()

    def __init__(self, x, y, player_number):
        self.alive = True
        self.x = x
        self.y = y    
        self.life_count = 12
        self.stair = None
        self.cloud_count = 5
        self.stair_reaction = {'general': Helper.EmptyFunction, 'hurt':self.Hurt, 'cloud':self.Cloud }
        if player_number == 1:
            self.left = pygame.K_a
            self.right = pygame.K_d
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
        
        self.direction = [0]
        
    '''
    def Photo(self):
        if i = 1:
            return picture1
        if i = 2: 
            return picture2 
    '''

    def Update(self, events):
        if self.alive == False:
            return
        ''' Update person's moving and life '''

        # Event Handling
        for event in events:
            if event.type == pygame.KEYDOWN:            # 若按鍵被按下
                if event.key == self.left:              # 按左鍵
                    self.direction.append(-5)
                if event.key == self.right:             # 按右鍵
                    self.direction.append(+5)
            if event.type == pygame.KEYUP:              # 若按鍵放開就不動
                if event.key == self.left:
                    self.direction.remove(-5)
                if event.key == self.right:
                    self.direction.remove(+5)
        
        self.x += self.direction[-1]

        # Check horizontal bounds
        if self.x < 31:                                 # 碰到左邊邊線不動
            self.x = 31
        if self.x + width > display_width * 0.6 - 31:       # 碰到右邊邊線不動
            self.x = display_width * 0.6 - width - 31

        # Handles vertical Movement
        self.y += 5                                     # 自然落下
        if self.y > display_height:                     # 落下超過下邊線就GameEnd
            self.Death()

        if self.y <= 40:                                # 若頭刺到上面刺刺
            Stair.stair_list[0].fall_through = True
            self.UpdateLife()

    def Death(self):
        self.alive = False
        global dead_count
        self.life_count = 0
        dead_count -= 1
        if dead_count <= 0:
            Helper.GameEnd()



