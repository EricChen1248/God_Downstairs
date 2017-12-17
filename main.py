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
        pygame.transform.scale(pygame.image.load('Stingstairs.png').convert_alpha(), (150, 20))

    Helper.stair_photos["Cloud"] = \
        pygame.transform.scale(pygame.image.load('Cloudstairs.png').convert_alpha(), (150, 40))

    # Initialize Persons
    global person_photo 
    person_photo = pygame.transform.scale(pygame.image.load('person.png'), (Person.width, Person.height)).convert_alpha()
    
    global persons
    persons = []
    Person.Init(display_width, display_height, persons)
    Person.display_width = display_width
    Person.display_height = display_height

    for i in range(Person.players):
        persons.append(Person.Person(340 + 75 - 20 + i * 30, stair_list[3].y - 40, i))
        persons[-1].photo = person_photo

    
    # Draw life graphics
    Helper.UpdateLife()
    
def BackgroundDisplay():
    """ Blits background over moving parts (players and stairs) of the game """
    for person in persons:
        if person.alive:
            game_display.blit(background_photo, [person.x, person.y], (person.x, person.y, Person.width, Person.height))

    for stair in stair_list:
        game_display.blit(background_photo, [stair.x, stair.y], (stair.x, stair.y, Stair.width, Stair.height + 20)) # + 20 To accomodate for cloud size

def GraphicDisplay():
    """Moving objects display"""
   
    # Display person images if alive
    for person in persons:
        if person.alive:
            game_display.blit(person.photo, [person.x, person.y])

    # Regenerate stairs if top one as reached spikes
    RegenStairs()
    
    # Redraw stairs
    for stair in stair_list:
        game_display.blit(Helper.stair_photos[stair.type], [stair.x, stair.y])
 
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
    
<<<<<<< HEAD
    # If there are two players, set player_collision to point to collision function
    if Person.players == 2:
        player_collision = Helper.PlayerCollision
    else:
        player_collision = Helper.EmptyFunction
=======
    global hurt_stair_photo
    hurt_stair_photo = pygame.image.load('Stingstairs.png')
    hurt_stair_photo = pygame.transform.scale(hurt_stair_photo, (150, 20))
    
    global cloud_stair_photo
    cloud_stair_photo = pygame.image.load('Cloudstairs.png')
    cloud_stair_photo = pygame.transform.scale(cloud_stair_photo, (150, 40))

    global moving_stair_photo #放移動樓梯的圖片
    moving_stair_photo = pygame.image.load('Cloudstairs.png')
    moving_stair_photo = pygame.transform.scale(moving_stair_photo, (150, 20))

    #initial stair list
    global stair_list
    stair_list = []
    for i in range(8):
        new_stair = Stair.Stair(display_width * 0.6, i)
        stair_list.append(new_stair)
    stair_list[2].x = 340

    global person
    person_photo = pygame.image.load('小傑正面.png')
    person = Person.Person(40, 60, 340+75-20, stair_list[2].y - 60, person_photo, display_width, display_height)
    person.photo = pygame.transform.scale(person_photo, (person.width, person.height))

>>>>>>> e1401f8... Add character animation pircture, adjust initial position

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

        pygame.display.update()
        clock.tick(60)

<<<<<<< HEAD
crashed = False
while not crashed:
    if not Helper.skip_start:
        Helper.GameStart()
    else:
        # Reset skip_start to False
        Helper.skip_start = False
=======
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    StartGame()

        # display background and text

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
>>>>>>> e1401f8... Add character animation pircture, adjust initial position
    
    try:
        GameLoop()
    except Exceptions.GameOverException:
        pass

Helper.QuitGame()
