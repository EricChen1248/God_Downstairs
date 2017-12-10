import pygame
import time
import random

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

def TextObjects(text, font):
    """change word to ghaph"""
    text_surface = font.render(text, True, black) 
    return text_surface, text_surface.get_rect()


def BackgroundDisplay():
    """Not-moving objects display"""
    
    #background
    game_display.fill(white)
    background_image = pygame.image.load('background test.png')
    background_image_size = pygame.transform.scale(background_image, (int(display_width * 0.6), display_height))
    game_display.blit(background_image_size, [0, 0])

    #
    game_font = pygame.font.Font('JT1-09U.TTF', 60)
    title_name, title_rect = TextObjects("小傑下樓梯~", game_font)
    title_rect.center = ((display_width * 0.8), (display_height * 0.2))
    game_display.blit(title_name, title_rect)


"""
Button Motion
"""


#initial stair list
stair_list = []
stair_number = 8 #how many stairs
for i in range(stair_number):
    stair_list.append(Stair())

def GraphicDisplay():
    """Moving objects display"""
    #person
    person = Person()
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
        stair_list.append(Stair())





#
crashed = False 
pause = False

def GameStart():
    pass

"""

#LOOP(Logic of the game)
def GameLoop():

    #Update and Display
    Person.Update()
    for i in range(stair_number):
        stair_list[i].Update()
    BackgroundDisplay()
    GraphicDisplay()

    """
    global pause
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    thingCount = 1
    dodged = 0    
    
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)


"""

def GameEnd():
    pass

GameStart()
GameLoop()
pygame.quit()
quit()