import pygame
import Colors
import Exceptions
import sys
import Person

game_display = None
display_width = None
display_height = None
background_photo = None
clock = None
stair_photos = {}

skip_start = False

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
    
    button_width_factor = 0.18
    button_height_factor = 0.1

    game_display.fill(Colors.white)
    game_font = pygame.font.Font('JT1-09U.TTF', 115)
    start_name, start_rect = TextObjects("小傑下樓梯~", game_font)
    start_rect.center = ((display_width / 2), (display_height / 4))
    game_display.blit(start_name, start_rect)

    def StartGame():
        nonlocal intro
        intro = False
        
    def StartButton():
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
        Person.players = 2
        clock.tick(20)

    def TogglePlayer1():
        Person.players = 1
        clock.tick(20)

    intro = True
    while intro:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    StartGame()

        StartButton()    

        if Person.players == 1:
            PlayerOneButton()
        else:
            PlayerTwoButton()

        pygame.display.update()
        clock.tick(15)

def GameEnd():
    """ Define Game End Screen """

    button_width_factor = 0.11
    button_height_factor = 0.09
    
    def RestartButton():
        Button("RESTART", display_width / 2 + 180, display_height / 1.15, 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        Colors.green, Colors.bright_green, Restart)
    
    def Restart():
        global skip_start
        skip_start = True
        raise Exceptions.GameOverException

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

    fail = True
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
    """ Captures thread in loop until unpaused """
    def Unpause():
        nonlocal pause
        pause = False

    large_text = pygame.font.Font("freesansbold.ttf",115)
    text_surf, text_rect = TextObjects("Paused", large_text, Colors.red)
    text_rect.center = ((display_width * 0.6 /2),(display_height * 0.4))
    
    pause = True
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

    NonMovingBackgroundDisplay()
    UpdateLife()

def UpdateLife():
    count = 0
    for person in Person.persons:
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
    """ Creates button with click actions """
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
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_surf, text_rect) 

def NonMovingBackgroundDisplay():
    """ Non-moving objects display """
    
    # Fill background white
    game_display.fill(Colors.white)

    # title
    game_font = pygame.font.Font('JT1-09U.TTF', 60)
    title_name, title_rect = TextObjects("小傑下樓梯~", game_font)
    title_rect.center = ((display_width * 0.8), (display_height * 0.05))
    game_display.blit(title_name, title_rect)

    # history highest score
    game_font = pygame.font.Font('JT1-09U.TTF', 36)
    title_name, title_rect = TextObjects("歷史高分：", game_font)
    title_rect.center = ((display_width * 0.68), (display_height * 0.15))
    game_display.blit(title_name, title_rect)

    # User photo
    user_image = pygame.image.load('lckung.png')
    user_image_size = pygame.transform.scale(user_image, (int(display_width * 0.05), int(display_height * 0.1)))
    game_display.blit(user_image_size, [display_width * 0.62, display_height * 0.2])

    # User name
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    user_name, user_rect = TextObjects("小傑", game_font)
    user_rect.center = ((display_width * 0.72), (display_height * 0.25))
    game_display.blit(user_name, user_rect)

    # Current score
    title_name, title_rect = TextObjects("現在分數：", game_font)
    title_rect.center = ((display_width * 0.7), (display_height * 0.35))
    game_display.blit(title_name, title_rect)

    # Life background
    for j in range(Person.players):
        title_name, title_rect = TextObjects("命：", game_font)
        title_rect.center = ((display_width * 0.65), (display_height * 0.45) + j * 60)
        game_display.blit(title_name, title_rect)

        for i in range(12):
            pygame.draw.rect(game_display, Colors.black,[display_width*(0.7+0.0195*i), display_height*0.42 + j * 60, display_width * 0.02 , display_height*0.06],1) 

    game_display.blit(background_photo, [0, 0])

def PlayerCollision():
    """ Handles Player Collision when there's two players """
    a = Person.persons[0]
    b = Person.persons[1]
    width = Person.width
    height = Person.height
    
    x_distance = abs(a.x - b.x)
    y_distance = abs(a.y - b.y)

    # Players need to be intersecting of both x and y axis
    if x_distance < width and y_distance < height:
        # If y distance is larger then it means player fell on top of each other
        if y_distance > x_distance:
            # Set players to stand on each other
            if b.y < a.y:
                b.y = a.y - height
            else:
                a.y = b.y - height
        # Otherwise players walked into each other
        else:
            # Only need to shift players by the amount of collision
            x_distance -= width
            # Determines left right order of players
            if b.x < a.x:
                a.x -= x_distance // 2
                b.x += x_distance  - x_distance // 2
            else:
                a.x += x_distance // 2
                b.x -= x_distance - x_distance // 2

def EmptyFunction(var1 = None, var2 = None, var3 = None, var4 = None, var5 = None):
    """ Empty Function for passing in a function that doesn't do anything when required """
    pass