import pygame
import time
import random
#import Person
#import Stair

#initiation and diaplay
pygame.init() 

display_width = 1200
display_height = 640
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('小傑下樓梯')
clock = pygame.time.Clock() 

#color set
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255)

def TextObjects(text, font):
    """change word to ghaph"""
    text_surface = font.render(text, True, black) 
    return text_surface, text_surface.get_rect()

def Button(msg,x,y,w,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    #change color
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

def BackgroundDisplay():
    """Not-moving objects display"""
    #background
    game_display.fill(white)
    life_photo = pygame.image.load('background_test.png')
    background_image_size = pygame.transform.scale(life_photo, (int(display_width * 0.6), display_height))
    game_display.blit(background_image_size, [0, 0])

    #title
    game_font = pygame.font.Font('JT1-09U.TTF', 60)
    title_name, title_rect = TextObjects("小傑下樓梯~", game_font)
    title_rect.center = ((display_width * 0.8), (display_height * 0.05))
    game_display.blit(title_name, title_rect)

    #history highest score
    game_font = pygame.font.Font('JT1-09U.TTF', 36)
    title_name, title_rect = TextObjects("歷史高分：", game_font)
    title_rect.center = ((display_width * 0.68), (display_height * 0.15))
    game_display.blit(title_name, title_rect)

    #User name and photo
    user_image = pygame.image.load('lckung.png')
    user_image_size = pygame.transform.scale(user_image, (int(display_width * 0.05), int(display_height * 0.1)))
    game_display.blit(user_image_size, [display_width * 0.62, display_height * 0.2])

    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    user_name, user_rect = TextObjects("小傑", game_font)
    user_rect.center = ((display_width * 0.72), (display_height * 0.25))
    game_display.blit(user_name, user_rect)

    #Current score
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = TextObjects("現在分數：", game_font)
    title_rect.center = ((display_width * 0.7), (display_height * 0.35))
    game_display.blit(title_name, title_rect)

    #Life
    game_font = pygame.font.Font('JT1-09U.TTF', 48)
    title_name, title_rect = TextObjects("命：", game_font)
    title_rect.center = ((display_width * 0.65), (display_height * 0.45))
    game_display.blit(title_name, title_rect)

    #Pause and Restart(Button)
    Button("Pause!",display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1, green, bright_green,action = Paused)
    Button("Restart!",display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1, red, bright_red,action = GameStart)


"""
Button Motion
""" 
def Paused():
    global pause   
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
                
        Button("Continue",display_width * 0.1,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2,green,bright_green,Unpause)
        Button("Quit",display_width * 0.4,display_height * 0.7,display_width * 0.6 * 0.3 ,display_height * 0.2,red,bright_red,QuitGame)

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
stair_number = 8 #how many stairs
stair_photo = pygame.image.load('.png')
for i in range(stair_number):
    new_stair = Stair()
    stair_list.append(new_stair)
'''

def GraphicDisplay():
    """Moving objects display"""

    #person
    person_photo = pygame.image.load('.png')
    life_photo = pygame.image.load('.png')
    person = Person(width, height, x, y, person_photo, 12, life_photo)
    person.photo = pygame.transform.scale(person_photo, (person.width, person.height))
    person.life_photo = pygame.transform.scale(life_photo, (int(display_width * 0.6), display_height))
  
    game_display.blit(person.photo, [person.x, person.y])

    #stairs
    StairMoving()
    for i in range(stair_number):
        stair = stair_list[i]
        game_display.blit(stair.photo, [stair.x, stair.y])

    #life
    for i in range(person.life_count):
        game_display.blit(person.life_photo, [int(display_width * 0.8) + i * 20, int(display_height * 0.2)])

    #points


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

def GameStart():
    pass


#LOOP(Logic of the game)
def GameLoop():
    global pause

    gameExit = False
    while not gameExit:
        #Update and Display
        '''
        Person.Update()
        for i in range(stair_number):
            stair_list[i].Update()
        '''
        BackgroundDisplay()
        #GraphicDisplay()


        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #Press Space to Pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True
                    Paused()


        pygame.display.update()
        clock.tick(60)


def GameEnd():
    pass

GameStart()
GameLoop()
pygame.quit()
quit()