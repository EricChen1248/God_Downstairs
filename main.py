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
    title_name, title_rect = Tool.TextObjects("小傑下樓梯~", game_font)
    title_rect.center = ((display_width * 0.8), (display_height * 0.05))
    game_display.blit(title_name, title_rect)

    # history highest score
    game_font = pygame.font.Font('JT1-09U.TTF', 36)
    title_name, title_rect = Tool.TextObjects("歷史高分：", game_font)
    title_rect.center = ((display_width * 0.68), (display_height * 0.15))
    game_display.blit(title_name, title_rect)

    # Current score
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = Tool.TextObjects("現在分數：", game_font)
    title_rect.center = ((display_width * 0.7), (display_height * 0.25))
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
        game_display.blit(background_photo, [person.x, person.y], [person.x, person.y, Person.width, Person.height])
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
        game_display.blit(stair_photo, [stair.x, stair.y])

    # person & life
    global person
    for j in range(Tool.players):
        person = person_list[j]
        game_display.blit(person.photo, [person.x, person.y])
 
        life = person.life_count
        for i in range(life): 
            pygame.draw.rect(game_display, Tool.red,[display_width*(0.7+0.0195*i) + 1, display_height*0.42 + 120 * j + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 
        for i in range(12 - life): 
            pygame.draw.rect(game_display, Tool.white,[display_width*(0.7+0.0195*(life + i)) + 1, display_height*0.42 + 120 * j + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 

    # Current score
    pygame.draw.rect(game_display, Tool.white,[display_width* 0.8, display_height * 0.2, 300, 50]) 
    
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = Tool.TextObjects(str(score.current_score), game_font)
    title_rect.center = ((display_width * 0.84), (display_height * 0.25))
    title_rect.x = display_width * 0.81
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
    global game_exit
    game_exit = False

    Init()
    NonMovingBackgroundDisplay()

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

    #initial stair list
    global stair_list
    stair_list = []
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
    
    global score
    score = Score.Score()

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
                
            for person in person_list:
                # 附近的樓梯檢查碰撞就好
                stair_list[(person.y-33)//75].HitPersonUpdate(person)
                stair_list[(person.y-33)//75+1].HitPersonUpdate(person)

                person.Update(events)

            if Tool.players == 2:
                Person.PersonInteraction(person_list)

            score.Update()

            GraphicDisplay()

            for event in events:
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
            clock.tick(60)

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
        Tool.Button(game_display, "START", display_width / 2 * (1 - button_width_factor), display_height * 0.7 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Tool.green, Tool.bright_green, StartGame)
        
    def PlayerOneButton():
        Tool.Button(game_display, "1 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Tool.red, Tool.bright_red, TogglePlayer2)

    def PlayerTwoButton():
        Tool.Button(game_display, "2 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Tool.red, Tool.bright_red, TogglePlayer1)
    
    def TogglePlayer2():
        Tool.players = 2
        clock.tick(20)

    def TogglePlayer1():
        Tool.players = 1
        clock.tick(20)


    Tool.players = 1
    while intro:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    StartGame()

        # display background and text

        game_display.fill(Tool.white)
        game_font = pygame.font.Font('JT1-09U.TTF', 115)
        start_name, start_rect = Tool.TextObjects("小傑下樓梯~", game_font)
        start_rect.center = ((display_width / 2), (display_height / 4))
        game_display.blit(start_name, start_rect)
        
        ''' pygame.draw.rect(game_display, (100,100,100), (255,255,main_width,main_height))
        pygame.draw.rect(game_display, (125,125,125), (250,250,main_width,main_height)) '''
        
        StartButton()    

        if Tool.players == 1:
            PlayerOneButton()
        else:
            PlayerTwoButton()

        pygame.display.update()
        clock.tick(15)


while not crashed:
    GameStart()
    GameLoop()
