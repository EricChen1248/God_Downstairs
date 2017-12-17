import pygame
class Person:
    def __init__(self, width, height, x, y, photo, display_width, display_height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.x_change = 0
        self.photo = photo        
        self.life_count = 12
        self.display_width = display_width
        self.display_height = display_height
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
                    person_photo = pygame.image.load('小傑側面_左跨步.png')
                    self.photo = pygame.transform.scale(person_photo, (self.width, self.height))
                if event.key == pygame. K_RIGHT:        # 按右鍵
                    self.x_change += 5
                    person_photo = pygame.image.load('小傑側面_右跨步.png')
                    self.photo = pygame.transform.scale(person_photo, (self.width, self.height))
            if event.type == pygame.KEYUP:              # 若按鍵放開就不動
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.x_change = 0
                    person_photo = pygame.image.load('小傑正面.png')
                    self.photo = pygame.transform.scale(person_photo, (self.width, self.height))        
        # Handles horizontal movements
        self.x += self.x_change
        # Check horizontal bounds
        if self.x <= 0:                                 # 碰到左邊邊線不動
            self.x = 0
        if self.x + self.width >= self.display_width * 0.6:  # 碰到右邊邊線不動
            self.x = self.display_width * 0.6 - self.width

        # Handles verticla Movement
        self.y += 5                                    # 自然落下
        if self.y > self.display_height:               # 落下超過下邊線就GameEnd
            pass #GameEnd()
        if self.y <= 40:                                 # 若頭刺到上面刺刺
            self.y += 25                                # 繼續自然落下(從梯子上面被擠下)
            self.life_count += -5                       # 命減5
            if self.life_count <= 0:                    # 檢查是否死掉，死了就GameEnd
                pass#GameEnd()

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
                pass#GameEnd()

    def Cloud(self, count):
        ''' 人碰到消失梯子 '''
        if count == 1:
            if self.life_count < 12:                        # 若沒滿血就加一
                self.life_count += 1

        if count <= 5:
            self.y += -7

    


