from gc import collect
from os import environ

import pygame

import Colors
import Exceptions
import Helper
import Person
import Stair

# Starting window position
environ['SDL_VIDEO_WINDOW_POS'] = '20,34'
# initiation and display
pygame.init() 

pygame.event.set_allowed(pygame.QUIT)
pygame.event.set_allowed(pygame.KEYDOWN)
pygame.event.set_allowed(pygame.KEYUP)
pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

display_width = 1200
display_height = 640
pygame.display.set_caption('小傑下樓梯')

def Init():
    # Initialize Background
    global background_photo
    background_photo = pygame.image.load('BackgroundIce.png').convert_alpha()
    background_photo = pygame.transform.scale(background_photo, (int(display_width * 0.6), display_height))
    Helper.background_photo = background_photo

    # Initialize Stairs
    global general_stair_photo
    general_stair_photo = pygame.image.load('Generalstairs_2.jpg').convert_alpha()
    general_stair_photo = pygame.transform.scale(general_stair_photo, (150, 20))
    
    global hurt_stair_photo
    hurt_stair_photo = pygame.image.load('Stingstairs.png').convert_alpha()
    hurt_stair_photo = pygame.transform.scale(hurt_stair_photo, (150, 20))
    
    global cloud_stair_photo
    cloud_stair_photo = pygame.image.load('Cloudstairs.png').convert_alpha()
    cloud_stair_photo = pygame.transform.scale(cloud_stair_photo, (150, 40))

    global person_photo 
    person_photo = pygame.transform.scale(pygame.image.load('person.png'), (Person.width, Person.height)).convert_alpha()
    Person.display_width = display_width
    Person.display_height = display_height
    Person.dead_count = Helper.players
    global persons
    persons = []
    
def BackgroundDisplay():
    global background_photo
    for person in persons:
        if person.alive:
            game_display.blit(background_photo, [person.x, person.y], (person.x, person.y, Person.width, Person.height))

    for stair in stair_list:
        game_display.blit(background_photo, [stair.x, stair.y], (stair.x, stair.y, Stair.width, Stair.height + 20)) # + 20 To accomodate for cloud size

def GraphicDisplay():
    """Moving objects display"""
   
    #person
    for person in persons:
        if person.alive:
            game_display.blit(person.photo, [person.x, person.y])

    #stairs
    StairMoving()
    global general_stair_photo
    global hurt_stair_photo
    global cloud_stair_photo

    for stair in stair_list:
        if stair.type == "general":
            stair_photo = general_stair_photo
        elif stair.type == "hurt":
            stair_photo = hurt_stair_photo
        else:
            stair_photo = cloud_stair_photo

        game_display.blit(stair_photo, [stair.x, stair.y])
 
    # points

    # Pause and Restart(Button)
    Helper.Button("Pause!",display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1, Colors.green, Colors.bright_green,action = Helper.Paused)
    Helper.Button("Restart!",display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1,Colors.red, Colors.bright_red,action = Restart)

def Restart():
    raise Exceptions.GameOverException

def StairMoving():
    """ Complicated moving about stairs """
    #Just checking the first one
    if stair_list[0].y < 35:
        del stair_list[0]
        next_stair = Stair.Stair(display_width * 0.6, 8)
        stair_list.append(next_stair)
        collect() # 優化


def GameLoop():
    """ Core Game Loop """
    game_exit = False

    Init()
    Helper.NonMovingBackgroundDisplay()

    #initial stair list
    global stair_list
    stair_list = []
    for i in range(8):
        new_stair = Stair.Stair(display_width * 0.6, i)
        stair_list.append(new_stair)
    stair_list[2].x = 340
    stair_list[2].type = "general"

    global persons
    persons = []
    Person.persons = persons
    global person_photo
    for i in range(Helper.players):
        persons.append(Person.Person(340 + 75 - 20 + i * 30, stair_list[2].y - 40, i))
        persons[-1].photo = person_photo

    Stair.stair_list = stair_list

    Helper.persons = persons
    Helper.UpdateLife()

    # If there are two players, set player_collision to point to collision function
    if Helper.players == 2:
        player_collision = Helper.PlayerCollision
    else:
        player_collision = Helper.EmptyFunction

    while not game_exit:
        BackgroundDisplay()

        # Save events
        events = pygame.event.get()

        # Update Stairs
        for i in range(8):
            stair_list[i].Update()

        # Update person
        for person in persons:
            # Take mod to narrow down to only two possible stairs that can be collided with
            try:
                stair_list[(person.y - 33) // 75].HitStair(person)
                stair_list[(person.y - 33) // 75 + 1].HitStair(person)
            # Possible index error when person below game level
            except IndexError:  
                pass
            person.Update(events)

        # Points to either collision function or empty function depending on player count
        player_collision()               

        # Redraw Background Display -> Foreground Display
        GraphicDisplay()

        for event in events:
            if event.type == pygame.QUIT:
                Helper.QuitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Helper.Paused()

        pygame.display.update()
        clock.tick(60)

        
crashed = False
clock = pygame.time.Clock() 
game_display = pygame.display.set_mode((display_width,display_height),pygame.DOUBLEBUF)
Helper.Init(game_display, display_width, display_height, clock)

while not crashed:

    persons = []
    background_photo = None
    person_photo = None
    stair_list = []
    
    pause = False
    
    
    if not Helper.skip_start:
        Helper.GameStart()
    else:
        # Reset skip_start to False
        Helper.skip_start = False
    
    try:
        GameLoop()
    except Exceptions.GameOverException:
        pass

Helper.QuitGame()
