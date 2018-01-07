import pygame
import time
import random
import Person
import Stair
import Score
import Tool
import gc
import os
import Exceptions


# Starting window position
os.environ['SDL_VIDEO_WINDOW_POS'] = '20,34'

# initiation and display
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init() 
display_width = 1200
display_height = 640
game_speed = 60
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('小傑下樓梯')
clock = pygame.time.Clock() 

person = None
background_photo = None
Person.GODMODE = False

def NonMovingBackgroundDisplay():
    """Not-moving objects display"""
    # background
    game_display.fill(Tool.white)
    game_display.blit(background_photo, [0, 0])

    # title
    game_font = pygame.font.Font('JT1-09U.TTF', 60)
    title_name, title_rect = Tool.TextObjects("小傑小銘下樓梯", game_font)
    title_rect.center = ((display_width * 0.8), (display_height * 0.05))
    game_display.blit(title_name, title_rect)

    # history highest score
    game_font = pygame.font.Font('msjhbd.ttc', 36)
    title_name, title_rect = Tool.TextObjects("歷史高分： " + str(Tool.highest_score), game_font)
    title_rect.center = ((display_width * 0.72), (display_height * 0.15))
    title_rect.x = display_width * 0.62
    game_display.blit(title_name, title_rect)

    # Current score
    game_font = pygame.font.Font('msjhbd.ttc', 48)
    title_name, title_rect = Tool.TextObjects("現在分數：", game_font)
    title_rect.center = ((display_width * 0.72), (display_height * 0.25))
    game_display.blit(title_name, title_rect)

    # User name and photo
    user_image = pygame.image.load('lckung.png')
    user_image_size = pygame.transform.scale(user_image, (int(display_width * 0.05), int(display_height * 0.1)))
    game_display.blit(user_image_size, [display_width * 0.62, display_height * 0.3])

    user_name, user_rect = Tool.TextObjects("小傑", game_font)
    user_rect.center = ((display_width * 0.72), (display_height * 0.35))
    game_display.blit(user_name, user_rect)

    if Tool.players == 2:
        user_image_2 = pygame.image.load('smlu.jpg')
        user_image_size = pygame.transform.scale(user_image_2, (int(display_width * 0.05), int(display_height * 0.1)))
        game_display.blit(user_image_size, [display_width * 0.62, display_height * 0.5])
        
        user_name, user_rect = Tool.TextObjects("小銘", game_font)
        user_rect.center = ((display_width * 0.72), (display_height * 0.55))
        game_display.blit(user_name, user_rect)

    # Life
    for j in range(Tool.players):
        title_name, title_rect = Tool.TextObjects("命：", game_font)
        title_rect.center = ((display_width * 0.65), (display_height * 0.45 + 120 * j))
        game_display.blit(title_name, title_rect)

        for i in range(12):
            pygame.draw.rect(game_display, Tool.black,[display_width*(0.7+0.0195*i), display_height*0.42 + 120 * j, display_width * 0.02 , display_height*0.06],1) 

def BackgroundDisplay():
    #截取背景部分圖覆蓋，不用整張背景覆蓋
    for person in person_list:
        game_display.blit(background_photo, [person.x, person.y - 5], [person.x, person.y - 5, Person.width, Person.height + 5])
    for stair in stair_list:
        game_display.blit(background_photo, [stair.x, stair.y], [stair.x, stair.y, 150, 40])

def Init():
    global background_photo
    background_photo = pygame.image.load('BackgroundIce.png')
    background_photo = pygame.transform.scale(background_photo, (int(display_width * 0.6), display_height))
    
    Tool.Init(game_display, display_width, display_height, clock)
    Tool.AddSound("Hurt", pygame.mixer.Sound('短慘叫.wav'))
    Tool.AddSound("Death", pygame.mixer.Sound('長慘叫.wav'))
    
""" Button Motion """ 

def Paused():
    global pause

    # Remove original button
    pygame.draw.rect(game_display, Tool.white,(display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1))
    pygame.draw.rect(game_display, Tool.white,(display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1))

    pause = True
    #pygame.draw.rect(game_display, red,[display_width*(0.7+0.0195*i) + 1, display_height*0.42 + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 
    large_text = pygame.font.Font("freesansbold.ttf",115)
    text_surf, text_rect = Tool.TextObjects("Paused", large_text, Tool.red)
    text_rect.center = ((display_width * 0.6 /2),(display_height * 0.4))
    
    while pause:
        game_display.blit(text_surf, text_rect)

        Tool.Button(game_display, "Continue",display_width * 0.05,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2, Tool.green,Tool.bright_green,Unpause)
        Tool.Button(game_display, "Quit",display_width * 0.38,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2, Tool.red,Tool.bright_red,QuitGame)

        for event in pygame.event.get():
            Tool.CheckAltF4(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Unpause()

            if event.type == pygame.QUIT:
                QuitGame()
                
        pygame.display.update()
        clock.tick(15)
    game_display.blit(background_photo, [0, 0])

def Unpause():
    global pause
    pause = False


def QuitGame():
    pygame.quit()
    quit()

def Restart():
    global game_exit
    game_exit = True

def InitializeStairPhotos():    
    global general_stair_photo
    general_stair_photo = pygame.image.load('Generalstairs_2.jpg')
    general_stair_photo = pygame.transform.scale(general_stair_photo, (150, 20))

    global hurt_stair_photo
    hurt_stair_photo = pygame.image.load('Stingstairs.png')
    hurt_stair_photo = pygame.transform.scale(hurt_stair_photo, (150, 20))

    global cloud_stair_photo
    cloud_stair_photo = pygame.image.load('Cloudstairs.png')
    cloud_stair_photo = pygame.transform.scale(cloud_stair_photo, (150, 40))

    global moving_stair_photo #放移動樓梯的圖片
    moving_stair_photo = pygame.image.load('Generalstairs_2.jpg')
    moving_stair_photo = pygame.transform.scale(moving_stair_photo, (150, 20))
    
    global blackhole_stair_photo #放移動樓梯的圖片
    blackhole_stair_photo = pygame.image.load('blackhole.png')
    blackhole_stair_photo = pygame.transform.scale(blackhole_stair_photo, (150, 40))


def GraphicDisplay():
    """Moving objects display"""
     
    #stairs
    StairMoving()
    for i in range(8):
        stair = stair_list[i]
        if stair.type == "general":
            stair_photo = general_stair_photo
        elif stair.type == "hurt":
            stair_photo = hurt_stair_photo
        elif stair.type == "cloud":
            stair_photo = cloud_stair_photo
        elif stair.type == "moving":
            stair_photo = moving_stair_photo
        elif stair.type == "blackhole":
            stair_photo = blackhole_stair_photo
        game_display.blit(stair_photo, [stair.x, stair.y])

    # person & life
    global person
    for j in range(Tool.players):
        person = person_list[j]
        if person.blackhole_size != 0:
            game_display.blit(pygame.transform.scale(person.photo, (Person.width - person.blackhole_size, Person.height - person.blackhole_size * 2)), [person.x + person.blackhole_size // 2, person.y - 5 + person.blackhole_size * 2])
        else:
            game_display.blit(person.photo, [person.x, person.y - 5])

        life = person.life_count
        for i in range(life): 
            pygame.draw.rect(game_display, Tool.red,[display_width*(0.7+0.0195*i) + 1, display_height*0.42 + 120 * j + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 
        for i in range(12 - life): 
            pygame.draw.rect(game_display, Tool.white,[display_width*(0.7+0.0195*(life + i)) + 1, display_height*0.42 + 120 * j + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 

    # Current score
    pygame.draw.rect(game_display, Tool.white,[display_width* 0.82, display_height * 0.2, 300, 60]) 
    
    game_font = pygame.font.Font('msjhbd.ttc', 48)
    title_name, title_rect = Tool.TextObjects(str(Score.Instance.current_score), game_font)
    title_rect.center = ((display_width * 0.85), (display_height * 0.25))
    title_rect.x = display_width * 0.82
    game_display.blit(title_name, title_rect)

    # Pause and Restart(Button)
    Tool.Button(game_display, "Pause!",display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1, Tool.green, Tool.bright_green,action = Paused)
    Tool.Button(game_display, "Restart!",display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1, Tool.red, Tool.bright_red,action = Restart)

def StairMoving():
    """Complicated moving about stairs"""
    #Just checking the first one
    if stair_list[0].y < 35:
        stair_list.pop(0)
        next_stair = Stair.Stair(display_width * 0.6, 8)
        stair_list.append(next_stair)
        gc.collect() # 優化

crashed = False 
pause = False

#LOOP(Logic of the game)
def GameLoop():
    global game_speed
    game_speed = 60
    global game_exit
    game_exit = False

    Init()
    NonMovingBackgroundDisplay()

    InitializeStairPhotos()

    #initial stair list
    global stair_list
    stair_list = []
    Stair.stair_list = stair_list
    for i in range(8):
        new_stair = Stair.Stair(display_width * 0.6, i)
        stair_list.append(new_stair)
    stair_list[4].x = 300
    stair_list[4].type = "general"

    jie_front = pygame.image.load('小傑正面.png')
    jie_right1 = pygame.image.load('小傑側面_右跨步.png')
    jie_right2 = pygame.image.load('小傑側面_右收步.png')
    jie_left1 = pygame.image.load('小傑側面_左跨步.png')
    jie_left2 = pygame.image.load('小傑側面_左收步.png')
    jie_front = pygame.transform.scale(jie_front, (Person.width, Person.height))
    jie_right1 = pygame.transform.scale(jie_right1, (Person.width, Person.height))
    jie_right2 = pygame.transform.scale(jie_right2, (Person.width, Person.height))
    jie_left1 = pygame.transform.scale(jie_left1, (Person.width, Person.height))
    jie_left2 = pygame.transform.scale(jie_left2, (Person.width, Person.height))
    
    ming_front = pygame.image.load('小銘正面.png')
    ming_right1 = pygame.image.load('小銘側面_右跨步.png')
    ming_right2 = pygame.image.load('小銘側面_右收步.png')
    ming_left1 = pygame.image.load('小銘側面_左跨步.png')
    ming_left2 = pygame.image.load('小銘側面_左收步.png')
    ming_front = pygame.transform.scale(ming_front, (Person.width, Person.height))
    ming_right1 = pygame.transform.scale(ming_right1, (Person.width, Person.height))
    ming_right2 = pygame.transform.scale(ming_right2, (Person.width, Person.height))
    ming_left1 = pygame.transform.scale(ming_left1, (Person.width, Person.height))
    ming_left2 = pygame.transform.scale(ming_left2, (Person.width, Person.height))

    global person_list
    person_list = []
    Person.display_width = display_width
    Person.display_height = display_height
    for i in range(Tool.players):
        if i == 0:
            person = Person.Person(300+75+40-i * 40, stair_list[4].y - 60, jie_front, jie_right1, jie_right2, jie_left1, jie_left2, i + 1)
        elif i == 1:
            person = Person.Person(300+75+40-i * 40, stair_list[4].y - 60, ming_front, ming_right1, ming_right2, ming_left1, ming_left2, i + 1)
        person_list.append(person)

    Score.Instance = Score.Score()

    global events

    alt = False
    f4 = False
    while not game_exit:
        try:
            #Update and Display
            
            BackgroundDisplay()
            events = pygame.event.get()
            for i in range(8):
                stair_list[i].Update(display_width * 0.6)

                """
                for person in person_list:
                    stair_list[i].HitPersonUpdate(person)
                """
            
            # 附近的樓梯檢查碰撞就好  
            
            for person in person_list:
                try: 
                    stair_list[(person.y-33)//75].HitPersonUpdate(person)
                except IndexError:
                    pass
                try: 
                    stair_list[(person.y-33)//75 + 1].HitPersonUpdate(person)
                except IndexError:
                    pass
            

            # person update
            for person in person_list:
                person.Update(events)


            if Tool.players == 2:
                Person.PersonInteraction(person_list)

            Score.Instance.Update()

            GraphicDisplay()

            for event in events:
                Tool.CheckAltF4(event)
                #Quit
                if event.type == pygame.QUIT:
                    QuitGame()

                #Press Space to Pause
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Paused()
                    if event.key == pygame.K_F4:
                        f4 = True
                    if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        alt = True

                if alt and f4:
                    QuitGame()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_F4:
                        f4 = False
                    if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        alt = False

            pygame.display.update()
            if Score.Instance.current_score % 50 == 0:
                game_speed += 0.2
            clock.tick(int(game_speed))

        except Exceptions.GameOverError:
            game_exit = True

        
def GameStart():
    """Define Game Intro screen"""
    intro = True
    
    button_width_factor = 0.18
    button_height_factor = 0.1
       
    def StartGame():
        nonlocal intro
        intro = False
        
    def StartButton():
        button_width_factor = 0.18
        button_height_factor = 0.1
        Tool.Button(game_display, "START", display_width / 2 * 0.8, display_height * 0.65, 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Tool.green, Tool.bright_green, StartGame)   

    def TogglePlayer2():
        Tool.players = 2
        P1_text = game_font.render("1P", True, Tool.white)
        game_display.blit(P1_text, P1_rect)
        P2_text = game_font.render("2P", True, Tool.red)
        game_display.blit(P2_text, P2_rect)
        clock.tick(20)

    def TogglePlayer1():
        Tool.players = 1
        P1_text = game_font.render("1P", True, Tool.red)
        game_display.blit(P1_text, P1_rect)
        P2_text = game_font.render("2P", True, Tool.white)
        game_display.blit(P2_text, P2_rect)
        clock.tick(20)


    # Game Intro background display
    intro_background = pygame.image.load('BackgroundIntro.png')
    intro_background = pygame.transform.scale(intro_background, (display_width, display_height + 30))
    game_display.blit(intro_background, [0, -30])
    
    game_font = pygame.font.Font('msjhbd.ttc', 30)
    if Tool.players == 1:
        P1_text = game_font.render("1P", True, Tool.red)
    else:
        P1_text = game_font.render("1P", True, Tool.white)
    P1_rect = P1_text.get_rect()
    P1_rect.center = ((display_width / 2 * 0.78),(display_height * 0.43) - 30)
    game_display.blit(P1_text, P1_rect)

    if Tool.players == 2:
        P2_text = game_font.render("2P", True, Tool.red)
    else:
        P2_text = game_font.render("2P", True, Tool.white)
        
    P2_rect = P2_text.get_rect()
    P2_rect.center = ((display_width / 2 * 1.12),(display_height * 0.43) - 30)
    game_display.blit(P2_text, P2_rect)
    # Load player mode picture and modify
    one_player_pre = pygame.image.load('小傑正面.png')
    one_player_pre = pygame.transform.scale(one_player_pre, (Person.width, Person.height))
    one_player_after = pygame.image.load('小傑正面.png')
    one_player_after = pygame.transform.scale(one_player_pre, (Person.width, Person.height))
    two_player_pre = pygame.image.load('2P_Pre.png')
    two_player_pre = pygame.transform.scale(two_player_pre, (Person.width * 2 + 5, Person.height))
    two_player_after = pygame.image.load('2P_Pre.png')
    two_player_after = pygame.transform.scale(two_player_pre, (Person.width * 2 + 5, Person.height))

    while intro:
        for event in pygame.event.get():  
            Tool.CheckAltF4(event)
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    TogglePlayer1()
                if event.key == pygame.K_RIGHT:
                    TogglePlayer2()
                if event.key == pygame.K_SPACE:
                    StartGame()
        
        StartButton()    

        # display player mode button
        Tool.PictureButton(game_display, one_player_pre, one_player_after, display_width / 2 * 0.75,
                        display_height * 0.48 - 15, display_width * 0.18, display_height * 0.1, TogglePlayer1)
        Tool.PictureButton(game_display, two_player_pre, two_player_after, display_width / 2 * 1.05, 
                        display_height * 0.48 - 15, display_width * 0.85, display_height * 0.1, TogglePlayer2)   
        """
        if Tool.players == 1:
            PlayerOneButton()
        else:
            PlayerTwoButton()
        """
        
        pygame.display.update()
        clock.tick(15)


while not crashed:
    GameStart()
    GameLoop()
