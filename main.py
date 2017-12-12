import pygame
import time
import random
import Person
# import Stair

# initiation and display
pygame.init() 

display_width = 1200
display_height = 640
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('小傑下樓梯')
clock = pygame.time.Clock() 

# color set
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255)

person = None
background_photo = None

def TextObjects(text, font):
    """ Change word to graph """
    text_surface = font.render(text, True, black) 
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

    small_font = pygame.font.Font("freesansbold.ttf",20)
    text_surf, text_rect = TextObjects(msg, small_font)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(text_surf, text_rect) 

def NonMovingBackgroundDisplay():
    """Not-moving objects display"""
    # background
    game_display.fill(white)

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

    # User name and photo
    user_image = pygame.image.load('lckung.png')
    user_image_size = pygame.transform.scale(user_image, (int(display_width * 0.05), int(display_height * 0.1)))
    game_display.blit(user_image_size, [display_width * 0.62, display_height * 0.2])

    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    user_name, user_rect = TextObjects("小傑", game_font)
    user_rect.center = ((display_width * 0.72), (display_height * 0.25))
    game_display.blit(user_name, user_rect)

    # Current score
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = TextObjects("現在分數：", game_font)
    title_rect.center = ((display_width * 0.7), (display_height * 0.35))
    game_display.blit(title_name, title_rect)

    # Life
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = TextObjects("命：", game_font)
    title_rect.center = ((display_width * 0.65), (display_height * 0.45))
    game_display.blit(title_name, title_rect)

    for i in range(12):
        pygame.draw.rect(game_display, black,[display_width*(0.7+0.0195*i), display_height*0.42, display_width * 0.02 , display_height*0.06],1) 

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
    pygame.draw.rect(game_display, white,(display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1))
    pygame.draw.rect(game_display, white,(display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1))

    pause = True
    large_text = pygame.font.Font("freesansbold.ttf",115)
    text_surf, text_rect = TextObjects("Paused", large_text)
    text_rect.center = ((display_width * 0.6 /2),(display_height * 0.4))
    
    while pause:
        game_display.blit(text_surf, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        Button("Continue",display_width * 0.05,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2,green,bright_green,Unpause)
        Button("Quit",display_width * 0.38,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2,red,bright_red,QuitGame)

        pygame.display.update()
        clock.tick(15)

def Unpause():
    global pause
    pause = False

def QuitGame():
    pygame.quit()
    quit()


'''
#initial stair list
stair_list = []
stair_number = 8 # how many stairs
stair_photo = pygame.image.load('.png')
for i in range(stair_number):
    new_stair = Stair()
    stair_list.append(new_stair)
'''

def GraphicDisplay():
    """Moving objects display"""
   
    #person
    global person
    game_display.blit(person.photo, [person.x, person.y])

    '''
    #stairs
    StairMoving()
    for i in range(stair_number):
        stair = stair_list[i]
        game_display.blit(stair.photo, [stair.x, stair.y])
    '''
    #life
    #for i in range(person.life_count):
    for i in range(5):   
        pygame.draw.rect(game_display, red,[display_width*(0.7+0.0195*i) + 1, display_height*0.42 + 1, display_width * 0.02 - 2, display_height*0.06 - 2]) 
     
    #points

    #Pause and Restart(Button)
    Button("Pause!",display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1, green, bright_green,action = Paused)
    Button("Restart!",display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1, red, bright_red,action = GameStart)

def StairMoving():
    """Complicated moving about stairs"""
    #Just checking the first one
    if stair_list[0].y < 0:
        stair_list.pop(0)
        next_stair = Stair()
        stair_list.append(next_stair)

#
crashed = False 
pause = False

#LOOP(Logic of the game)
def GameLoop():

    gameExit = False

    Init()
    NonMovingBackgroundDisplay()

    global person
    person_photo = pygame.image.load('person.png')
    person = Person.Person(40, 60, 350, 150, person_photo, display_width, display_height)
    person.photo = pygame.transform.scale(person_photo, (person.width, person.height))
    
    while not gameExit:

        #Update and Display

        events = pygame.event.get()
        person.Update(events)

        '''
        for i in range(stair_number):
            stair_list[i].Update()
        '''
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
        Button("START", display_width / 2 * (1 - button_width_factor), display_height * 0.7 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        green, bright_green, StartGame)
        
    def PlayerOneButton():
        Button("1 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        red, bright_red, TogglePlayer2)

    def PlayerTwoButton():
        Button("2 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        red, bright_red, TogglePlayer1)
   
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

        # display background and text
        ''' start_background = pygame.image.load('background.png') # 弄圖片
        game_display.fill(start_background) '''
        game_display.fill(white)
        game_font = pygame.font.Font('JT1-09U.TTF', 115)
        start_name, start_rect = TextObjects("小傑下樓梯~", game_font)
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
        Button("RESTART", display_width / 2 + 180, display_height / 1.15, 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        green, bright_green, GameLoop)
    
    fail = True

    while fail:

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
               
        # Background and text display
        game_display.fill(white)
        game_font = pygame.font.Font('JT1-09U.TTF', 115)
        end_text = game_font.render("GAME OVER !!", True, red) 
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


        RestartButton()
    # if score > highest_score:            # highest score用global，一開始就抓

        pygame.display.update()
        clock.tick(15)



GameStart()
GameLoop()
pygame.quit()
quit()