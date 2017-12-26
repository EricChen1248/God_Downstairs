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
# Initialization and display
pygame.init() 

pygame.event.set_allowed(pygame.QUIT)
pygame.event.set_allowed(pygame.KEYDOWN)
pygame.event.set_allowed(pygame.KEYUP)
pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

display_width = 1200
display_height = 640
pygame.display.set_caption('小傑下樓梯')
game_display = pygame.display.set_mode((display_width,display_height),pygame.DOUBLEBUF)

clock = pygame.time.Clock()

Helper.Init(game_display, display_width, display_height, clock)

def Init():
    """ Initialization Function for main """
    # Initialize Background
    global background_photo
    background_photo = pygame.image.load('BackgroundIce.png').convert_alpha()
    background_photo = pygame.transform.scale(background_photo, (int(display_width * 0.6), display_height))
    Helper.background_photo = background_photo

    # Initialize Stairs
    global stair_list
    stair_list = []

    Stair.stair_list = stair_list

    for i in range(8):
        new_stair = Stair.Stair(display_width * 0.6, i)
        stair_list.append(new_stair)
        
    # Set stair number 3 to be in the center so players have something to stand on
    stair_list[3].x = 340
    stair_list[3].type = "Normal"

    # Initialize Stair Images
    Helper.stair_photos["Normal"] = \
        pygame.transform.scale(pygame.image.load('Generalstairs_2.jpg').convert_alpha(), (150, 20))
    
    Helper.stair_photos["Spike"] = \
        pygame.transform.scale(pygame.image.load('Stingstairs.png').convert_alpha(), (150, 30))

    Helper.stair_photos["Cloud"] = \
        pygame.transform.scale(pygame.image.load('Cloudstairs.png').convert_alpha(), (150, 40))

    person_photos = [[],[]]
    person_photos[0].append(pygame.transform.scale(pygame.image.load('小傑正面.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[0].append(pygame.transform.scale(pygame.image.load('小傑側面_右跨步.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[0].append(pygame.transform.scale(pygame.image.load('小傑側面_右收步.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[0].append(pygame.transform.scale(pygame.image.load('小傑側面_左跨步.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[0].append(pygame.transform.scale(pygame.image.load('小傑側面_左收步.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[1].append(pygame.transform.scale(pygame.image.load('小銘正面.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[1].append(pygame.transform.scale(pygame.image.load('小銘側面_右跨步.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[1].append(pygame.transform.scale(pygame.image.load('小銘側面_右收步.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[1].append(pygame.transform.scale(pygame.image.load('小銘側面_左跨步.png'), (Person.width, Person.height)).convert_alpha())
    person_photos[1].append(pygame.transform.scale(pygame.image.load('小銘側面_左收步.png'), (Person.width, Person.height)).convert_alpha())

    global persons
    persons = []
    Person.Init(display_width, display_height, persons)
    Person.display_width = display_width
    Person.display_height = display_height

    for i in range(Person.players):
        persons.append(Person.Person(340 + 75 - 20 + i * 30, stair_list[3].y - Person.height,  i, person_photos[i][0], person_photos[i][1], person_photos[i][2],person_photos[i][3],person_photos[i][4]))

    
    # Draw life graphics
    Helper.DrawLife()
    
def BackgroundDisplay():
    """ Blits background over moving parts (players and stairs) of the game """
    for person in persons:
        if person.alive:
            game_display.blit(background_photo, [person.x, person.y], (person.x, person.y, Person.width, Person.height))

    for stair in stair_list:
        height = Helper.stair_photos[stair.type].get_height()
        game_display.blit(background_photo, [stair.x, stair.y - height + 20], (stair.x, stair.y - height + 20, Stair.width, height)) # + 20 To accomodate for cloud size

def GraphicDisplay():
    """Moving objects display"""
   
    # Display person images if alive
    for person in persons:
        if person.alive:
            game_display.blit(person.Photo(), [person.x, person.y])

    # Regenerate stairs if top one as reached spikes
    RegenStairs()
    
    # Redraw stairs
    for stair in stair_list:
        photo = Helper.stair_photos[stair.type]
        game_display.blit(photo, [stair.x, stair.y - photo.get_height() + 20])
 
    # Pause and Restart(Button)
    Helper.Button("Pause!",display_width * 0.7, display_height * 0.7, display_width * 0.2, display_height * 0.1, Colors.green, Colors.bright_green,action = Helper.Paused)
    Helper.Button("Restart!",display_width * 0.7, display_height * 0.85, display_width * 0.2, display_height * 0.1,Colors.red, Colors.bright_red,action = Restart)

def Restart():
    raise Exceptions.GameOverException

def RegenStairs():
    """ Complicated moving about stairs """
    #Just checking the first one
    if stair_list[0].y < 35:
        del stair_list[0]
        next_stair = Stair.Stair(display_width * 0.6, 8)
        stair_list.append(next_stair)
        collect() # 優化

def GameLoop():
    """ Core Game Loop """

    Init()
    Helper.NonMovingBackgroundDisplay()
    
    # If there are two players, set player_collision to point to collision function
    if Person.players == 2:
        player_collision = Helper.PlayerCollision
    else:
        player_collision = Helper.EmptyFunction

    game_exit = False
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

            Helper.CheckAltF4(event)

        pygame.display.update()
        clock.tick(60)

crashed = False
while not crashed:
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
