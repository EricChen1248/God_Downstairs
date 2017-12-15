import pygame
import Helper
import Stair

display_width = None
display_height = None

width = 40
height = 40

dead_count = 2
persons = []

default_fall_time = 4

persons = []
players = 1

def Init(width, height, person_list):
    global display_width 
    display_width = width
    global display_height
    display_height = height
    global persons
    persons = person_list
    global dead_count
    dead_count = players

class Person:

    def SpikeStairs(self, stair):
        """ Spike stair reaction """
        if self.stair is not stair:
            self.UpdateLife(-6)

    def CloudStairs(self, stair):
        """ Cloud stair reaction """
        # If cloud was not the same cloud as last time, reset count
        if self.stair is not stair:
            self.cloud_count = 5
        else:
        # Reduce count and check if below threshold
            self.cloud_count -= 1
            if self.cloud_count <= 0:
                self.fall_through = default_fall_time

    def HitStair(self, stair):
        """ Base hit stair reaction, chains other reactions through """
        # If player is in state of fall through, no interaction with stairs
        if self.fall_through > 0:
            return
        # Set person height to be standing on stair
        self.y = stair.y - height
        # Execute stair reactions
        self.stair_reaction[stair.type](stair)
        # If current stair isn't the same stair as the last collision
        if self.stair is not stair:
            self.UpdateLife(1)
            self.stair = stair

    def UpdateLife(self, reduce = -5):            
        self.life_count += reduce
        if self.life_count > 12:
            self.life_count = 12
        if self.life_count <= 0:
            self.Death()
        
        # Update Life Drawing    
        Helper.UpdateLife()

    def __init__(self, x, y, player_number):
        self.x = int(x)
        self.y = int(y)
        self.player_number = player_number
        
        # Base Initializes
        self.life_count = 12
        self.stair = None
        self.alive = True

        # Used to keep track of cloud standing time
        self.cloud_count = 5
        # Map stair_reaction dictionary
        self.stair_reaction = {'Normal': Helper.EmptyFunction, 'Spike':self.SpikeStairs, 'Cloud':self.CloudStairs }
        # Fall through timer count
        self.fall_through = 0
        # Initialize direction with default 0 (Non moving)
        self.direction = [0]
        # Set respective left and right for players
        if player_number == 1:
            self.left = pygame.K_a
            self.right = pygame.K_d
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
        
    '''
    def Photo(self):
        if i = 1:
            return picture1
        if i = 2: 
            return picture2 
    '''

    def Update(self, events):
        """ Update person's moving and life """
        
        # Stop processing update if already dead
        if self.alive == False:
            return
        
        # Reduce fall through count by 1
        try:
            self.fall_through -= 1
        # Resets to 0 if player somehow manages to survive that long without resets
        except OverflowError:
            self.fall_through = 0

        # Event Handling
        for event in events:
            # Adds direction modifier to direction list
            if event.type == pygame.KEYDOWN:            
                if event.key == self.left:              
                    self.direction.append(-5)
                if event.key == self.right:             
                    self.direction.append(+5)
            if event.type == pygame.KEYUP:              
                if event.key == self.left:
                    self.direction.remove(-5)
                if event.key == self.right:
                    self.direction.remove(+5)

        # Last direction in list means the last, unreleased key press
        self.x += self.direction[-1]

        # Check horizontal bounds
        # Left Bound
        if self.x < 31:                                 
            self.x = 31
        # Right Bound
        elif self.x + width > display_width * 0.6 - 31:       
            self.x = display_width * 0.6 - width - 31

        # Handles vertical Movement
        self.y += 5     
        # If below lower edge -> Dead                                
        if self.y > display_height:
            self.Death()

        # If touching spikes, fall through
        if self.y <= 40:
            self.fall_through = default_fall_time
            self.UpdateLife()


    def Death(self):
        # Mark self as dead
        self.alive = False

        # Update dead count 
        global dead_count
        dead_count -= 1
        
        # Update Life graphics
        self.life_count = 0
        Helper.UpdateLife()

        # If all players are dead, end game
        if dead_count <= 0:
            Helper.GameEnd()