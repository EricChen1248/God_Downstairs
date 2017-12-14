import pygame
import Colors
import Exceptions
import sys

game_display = None
display_width = None
display_height = None
clock = None

skip_start = False
players = 1
persons = []

def Init(display, width, height, oClock):
    global game_display
    game_display = display
    
    global display_width
    display_width = width

    global display_height
    display_height = height

    global clock
    clock = oClock

def GameStart():
    """Define Game Intro screen"""
    intro = True
    
    button_width_factor = 0.18
    button_height_factor = 0.1
    

    # display background and text
    ''' start_background = pygame.image.load('background.png') # 弄圖片
    game_display.fill(start_background) '''
    
    ''' pygame.draw.rect(game_display, (100,100,100), (255,255,main_width,main_height))
    pygame.draw.rect(game_display, (125,125,125), (250,250,main_width,main_height)) '''

    game_display.fill(Colors.white)
    game_font = pygame.font.Font('JT1-09U.TTF', 115)
    start_name, start_rect = TextObjects("小傑下樓梯~", game_font)
    start_rect.center = ((display_width / 2), (display_height / 4))
    game_display.blit(start_name, start_rect)

    def StartGame():
        nonlocal intro
        intro = False
        
    def StartButton():
        button_width_factor = 0.18
        button_height_factor = 0.1
        Button("START", display_width / 2 * (1 - button_width_factor), display_height * 0.7 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Colors.green, Colors.bright_green, StartGame)
        
    def PlayerOneButton():
        Button("1 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Colors.red, Colors.bright_red, TogglePlayer2)

    def PlayerTwoButton():
        Button("2 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Colors.red, Colors.bright_red, TogglePlayer1)
   
    def TogglePlayer2():
        global players
        players = 2
        clock.tick(20)

    def TogglePlayer1():
        global players
        players = 1
        clock.tick(20)

    while intro:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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
        Button("RESTART", display_width / 2 + 180, display_height / 1.15, 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Colors.green, Colors.bright_green, Restart)
    
    def Restart():
        global skip_start
        skip_start = True
        clock.tick(20)
        raise Exceptions.GameOverException

    fail = True

    game_display.fill(Colors.white)
    game_font = pygame.font.Font('JT1-09U.TTF', 115)
    end_text = game_font.render("GAME OVER !!", True, Colors.red) 
    end_rect = end_text.get_rect()
    end_rect.center = ((display_width / 2),(display_height / 5))
    game_display.blit(end_text, end_rect)

    score_font = pygame.font.Font('JT1-09U.TTF', 100)
    end_score_text, end_score_rect = TextObjects("得分：", score_font)
    end_score_rect.center = ((display_width / 2 - 140), (display_height / 2.1))
    game_display.blit(end_score_text, end_score_rect)

    highest_font = pygame.font.Font('JT1-09U.TTF', 80)
    highest_text, highest_rect = TextObjects("歷史高分：", highest_font)
    highest_rect.center = ((display_width / 2 - 200), (display_height / 1.5))
    game_display.blit(highest_text, highest_rect)

    bottomtext_font = pygame.font.Font('JT1-09U.TTF', 50)
    bottomtext_text, bottomtext_rect = TextObjects("太可惜了！再來一次吧！", bottomtext_font)
    bottomtext_rect.center = ((display_width / 2 - 120), (display_height / 1.1))
    game_display.blit(bottomtext_text, bottomtext_rect)

    while fail:

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Restart()
               
        RestartButton()
        # if score > highest_score:            # highest score用global，一開始就抓

        pygame.display.update()
        clock.tick(15)

def QuitGame():
    pygame.quit()
    sys.exit()

def Paused():
    
    def Unpause():
        nonlocal pause
        pause = False

    # Remove original button
    pygame.draw.rect(game_display, Colors.white,(display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1))
    pygame.draw.rect(game_display, Colors.white,(display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1))

    pause = True
    #pygame.draw.rect(game_display  Colors.red,[display_width*(0.7+0.0195*i) + 1, display_height*0.42 + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 
    large_text = pygame.font.Font("freesansbold.ttf",115)
    text_surf, text_rect = TextObjects("Paused", large_text, Colors.red)
    text_rect.center = ((display_width * 0.6 /2),(display_height * 0.4))
    
    while pause:
        game_display.blit(text_surf, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Unpause()
                
        Button("Continue",display_width * 0.05,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2, Colors.green, Colors.bright_green,Unpause)
        Button("Quit",display_width * 0.38,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2, Colors.red, Colors.bright_red,QuitGame)

        pygame.display.update()
        clock.tick(15)

def UpdateLife():
    count = 0
    for person in persons:
        life = person.life_count
        for i in range(life): 
            pygame.draw.rect(game_display,Colors.red,[display_width*(0.7+0.0195*i) + 1, display_height*0.42 + 1 + count * 60, display_width * 0.02 - 2, display_height*0.06 - 2]) 
        for i in range(12 - life): 
            pygame.draw.rect(game_display, Colors.white,[display_width*(0.7+0.0195*(life + i)) + 1, display_height*0.42 + 1 + count * 60, display_width * 0.02 - 2, display_height*0.06 - 2]) 
        count += 1

def TextObjects(text, font, color = Colors.black):
    """ Change word to graph """
    text_surface = font.render(text, True, color) 
    return text_surface, text_surface.get_rect()

def Button(msg,x,y,w,h,ic,ac,action = None):
    """ Create button"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # change color
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, ic,(x,y,w,h))

    small_font = pygame.font.Font("freesansbold.ttf",32)
    text_surf, text_rect = TextObjects(msg, small_font)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(text_surf, text_rect) 

def EmptyFunction(var1 = None, var2 = None, var3 = None, var4 = None, var5 = None):
    pass