import pygame
import time
import random
import Person
import Stair
import Tool
import gc
import os


# Starting window position
os.environ['SDL_VIDEO_WINDOW_POS'] = '20,34'

# initiation and display
pygame.init() 
display_width = 1200
display_height = 640
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('小傑下樓梯')
clock = pygame.time.Clock() 

person = None
background_photo = None

def NonMovingBackgroundDisplay():
    """Not-moving objects display"""
    # background
    game_display.fill(Tool.white)

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

    # User name and photo
    user_image = pygame.image.load('lckung.png')
    user_image_size = pygame.transform.scale(user_image, (int(display_width * 0.05), int(display_height * 0.1)))
    game_display.blit(user_image_size, [display_width * 0.62, display_height * 0.2])

    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    user_name, user_rect = Tool.TextObjects("小傑", game_font)
    user_rect.center = ((display_width * 0.72), (display_height * 0.25))
    game_display.blit(user_name, user_rect)

    # Current score
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = Tool.TextObjects("現在分數：", game_font)
    title_rect.center = ((display_width * 0.7), (display_height * 0.35))
    game_display.blit(title_name, title_rect)

    # Life
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = Tool.TextObjects("命：", game_font)
    title_rect.center = ((display_width * 0.65), (display_height * 0.45))
    game_display.blit(title_name, title_rect)

    for i in range(12):
        pygame.draw.rect(game_display, Tool.black,[display_width*(0.7+0.0195*i), display_height*0.42, display_width * 0.02 , display_height*0.06],1) 

def BackgroundDisplay():
    global background_photo
    game_display.blit(background_photo, [0, 0])

def Init():
    global background_photo
    background_photo = pygame.image.load('BackgroundIce.png')
    background_photo = pygame.transform.scale(background_photo, (int(display_width * 0.6), display_height))
    
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
            print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Unpause()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        pygame.display.update()
        clock.tick(15)

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
   
    #person
    global person
    game_display.blit(person.photo, [person.x, person.y])

   
    #stairs
    StairMoving()
    global general_stair_photo
    global hurt_stair_photo
    global cloud_stair_photo

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
 
    #life
    life = person.life_count
    for i in range(life): 
        pygame.draw.rect(game_display, Tool.red,[display_width*(0.7+0.0195*i) + 1, display_height*0.42 + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 
    for i in range(12 - life): 
        pygame.draw.rect(game_display, Tool.white,[display_width*(0.7+0.0195*(life + i)) + 1, display_height*0.42 + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 
    

    #points

    #Pause and Restart(Button)
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
#
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
    stair_list[3].x = 300
    stair_list[3].type = "general"

    global person
    person_photo = pygame.image.load('小傑正面.png')
    person = Person.Person(40, 60, 300+75-20, stair_list[3].y - 60, person_photo, display_width, display_height)
    person.photo = pygame.transform.scale(person_photo, (person.width, person.height))

    global events
    while not game_exit:

        #Update and Display

        events = pygame.event.get()
        person.Update(events)

        for i in range(8):
            stair_list[i].Update(person, display_width * 0.6)

        BackgroundDisplay()
        GraphicDisplay()

        for event in events:
            #Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #Press Space to Pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Paused()

        pygame.display.update()
        clock.tick(60)

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
        nonlocal players
        players = 2
        clock.tick(20)

    def TogglePlayer1():
        nonlocal players
        players = 1
        clock.tick(20)

    players = 1
    while intro:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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

        if players == 1:
            PlayerOneButton()
        else:
            PlayerTwoButton()

        pygame.display.update()
        clock.tick(15)

def GameEnd():
    """Define Game End Screen"""

    def RestartButton():
        button_width_factor = 0.11
        button_height_factor = 0.09
        Tool.Button(game_display, "RESTART", display_width / 2 + 180, display_height / 1.15, 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        green, Tool.bright_green, GameLoop)
    fail = True

    while fail:

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
               
        # Background and text display
        game_display.fill(Tool.white)
        game_font = pygame.font.Font('JT1-09U.TTF', 115)
        end_text = game_font.render("GAME OVER !!", True, Tool.red) 
        end_rect = end_text.get_rect()
        end_rect.center = ((display_width / 2),(display_height / 5))
        game_display.blit(end_text, end_rect)

        score_font = pygame.font.Font('JT1-09U.TTF', 100)
        end_score_text, end_score_rect = Tool.TextObjects("得分：", score_font)
        end_score_rect.center = ((display_width / 2 - 140), (display_height / 2.1))
        game_display.blit(end_score_text, end_score_rect)

        highest_font = pygame.font.Font('JT1-09U.TTF', 80)
        highest_text, highest_rect = Tool.TextObjects("歷史高分：", highest_font)
        highest_rect.center = ((display_width / 2 - 200), (display_height / 1.5))
        game_display.blit(highest_text, highest_rect)

        bottomtext_font = pygame.font.Font('JT1-09U.TTF', 50)
        bottomtext_text, bottomtext_rect = Tool.TextObjects("太可惜了！再來一次吧！", bottomtext_font)
        bottomtext_rect.center = ((display_width / 2 - 120), (display_height / 1.1))
        game_display.blit(bottomtext_text, bottomtext_rect)


        RestartButton()
    # if score > highest_score:            # highest score用global，一開始就抓

        pygame.display.update()
        clock.tick(15)

while not crashed:
    GameStart()
    GameLoop()
