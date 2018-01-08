import pygame
import random
import Tool
import Stair

width = 40
height = 60
display_width = 0
display_height = 0

GODMODE = False
pass_through = False
class Person:
    def __init__(self, x, y, front, right1, right2, left1, left2, playerID):
        self.x = x
        self.y = y
        self.player_id = playerID

        self.InitializeFixedAttributes()
        self.InitializePhotos(right1, right2, left1, left2, front)

    def InitializeFixedAttributes(self):
        self.blackhole_size = 0
        self.life_count = 12
        self.direction = [0]
        self.alive = True
        self.animate_count = 0
        self.last_stair = None
        self.cloud_count = 0

    def InitializePhotos(self, right1, right2, left1, left2, front):
        self.right_photo_1 = right1
        self.right_photo_2 = right2
        self.left_photo_1 = left1
        self.left_photo_2 = left2
        self.front_photo = front
        
        self.photo = front  # 預設開始是 正面

    def Update(self, events):
        ''' Handles all update related functions for person '''

        # Don't run update functions if dead
        if self.alive == False:
            return 

        self.EventHandling(events)
        self.PhotoHandling()
        self.BoundaryChecks()

    def BoundaryChecks(self):
        ''' Checks and clamps the horizontal and vertical boundaries '''
        # Check horizontal bounds
        if self.x <= 31:                                 # 碰到左邊邊線不動
            self.x = 31
        if self.x + width >= display_width * 0.6 - 31:  # 碰到右邊邊線不動
            self.x = display_width * 0.6 - width - 31

        # Handles vertical Movement
        self.y += 5                                    # 自然落下
        if self.y - height > display_height:               # 落下超過下邊線就GameEnd
            self.Death()

        global pass_through
        pass_through = False
        if self.y <= 40:                                 # 若頭刺到上面刺刺
            Tool.sounds["Hurt"].play()
            pass_through = 20
            Stair.stair_list[0].pass_through = True     # 繼續自然落下(從梯子上面被擠下)
            self.life_count += -5                       # 命減5
            if self.life_count <= 0:                    # 檢查是否死掉，死了就GameEnd
                self.Death()

    def PhotoHandling(self):
        ''' Sets photo to the correct one based on direction and animation '''
        self.animate_count += 1
        # Handles horizontal movements
        self.x += self.direction[-1]
        if self.direction[-1] == 5:
            if self.animate_count > 10:
                self.photo = self.right_photo_1
                if self.animate_count > 20:
                    self.animate_count = 0
            else:
                self.photo = self.right_photo_2
        elif self.direction[-1] == -5:
            if self.animate_count > 10:
                self.photo = self.left_photo_1
                if self.animate_count > 20:
                    self.animate_count = 0
            else:
                self.photo = self.left_photo_2
        else:
            self.photo = self.front_photo

    def EventHandling(self, events):
        ''' Handles pygame events '''
        for event in events:
            if event.type == pygame.KEYDOWN:            # 若按鍵被按下
                if self.player_id == 1:
                    if event.key == pygame.K_LEFT:          # 按左鍵
                        self.direction.append(-5)
                    if event.key == pygame.K_RIGHT:        # 按右鍵
                        self.direction.append(5)
                elif self.player_id == 2:
                    if event.key == pygame.K_a:          # 按左鍵
                        self.direction.append(-5)
                    if event.key == pygame.K_d:        # 按右鍵
                        self.direction.append(5)
            if event.type == pygame.KEYUP:              # 若按鍵放開就不動
                if self.player_id == 1:
                    if event.key == pygame.K_LEFT:
                        self.direction.remove(-5)
                    elif event.key == pygame.K_RIGHT:
                        self.direction.remove(5)
                elif self.player_id == 2:
                    if event.key == pygame.K_a:
                        self.direction.remove(-5)
                    elif event.key == pygame.K_d:
                        self.direction.remove(5)

    def Death(self):
        if GODMODE:
            self.life_count = 12
            self.y = 40
        else:
            Tool.sounds["Death"].play()
            self.alive = False
            self.life_count = 0
            self.y = 1000
            Tool.GameEndCount()

    def General(self, current_stair):
        ''' 人碰到一般梯子時 '''                                
        self.y = current_stair.y - height
        if current_stair != self.last_stair:
            self.blackhole_size = 0
            self.last_stair = current_stair
            if self.life_count < 12:                        # 若沒滿血就加一
                self.life_count += 1                       # 若梯子是-10往上，要抵銷自然落下就要-20
           
    def Hurt(self, current_stair):
        ''' 人碰到刺刺梯子時 '''                    
        self.y = current_stair.y - height
        if current_stair != self.last_stair:
            Tool.sounds["Hurt"].play()
            self.life_count += -5                           # 命減5
            self.last_stair = current_stair
            if self.life_count <= 0:                       # 檢查是否死掉，死了就GameEnd
                self.Death()

    def Cloud(self, current_stair):
        ''' 人碰到消失梯子 '''
        self.cloud_count += 1
        if self.cloud_count <= 10:                    
            self.y = current_stair.y - height

        if current_stair != self.last_stair:
            self.last_stair = current_stair 
            self.cloud_count = 0
            if self.x <= current_stair.x + 3:
                self.y += 5
            else:
                self.y += 3
            if self.life_count < 12:                        # 若沒滿血就加一
                self.life_count += 1


    def Moving(self, current_stair):
        ''' 碰到移動樓梯的反應 '''                    
        self.y = current_stair.y - height
        self.x += current_stair.stair_speed * current_stair.hit_count
        if current_stair != self.last_stair:   
            self.last_stair = current_stair
            if self.life_count < 12:                        
                self.life_count += 1
    
    def Blackhole(self, current_stair):
        ''' 碰到黑洞 '''
        self.x -= self.direction[-1]
        self.blackhole_size += 1
        target_x = current_stair.x + current_stair.width // 2 - width // 2
        self.x += (target_x - self.x) / abs(target_x - self.x) * 2
        self.y = current_stair.y - height
        if self.blackhole_size == height / 2:
            self.blackhole_size = 0
            self.y = random.randint(80, display_height * 0.4)
            self.x = random.randint(60, display_width * 0.6 - 60)
        
        if current_stair != self.last_stair:
            self.last_stair = current_stair

def PersonInteraction(person_list):
    ''' 雙人版互動'''
    global pass_through
    if pass_through:
        Stair.stair_list[1].pass_through = True
        pass_through = False
        return
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