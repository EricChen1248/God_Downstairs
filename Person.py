''' Person logic handling '''
#pylint: disable-msg=C0103, W0603, W0201
import pygame
import images
import sounds
import settings
import keys
import stair
from core import game_over

width = 40
height = 60

person_list = []

def reset_person_list():
    ''' Resets persons list '''
    global person_list
    person_list = []

def person_interaction(person1, person2):
    ''' 雙人版互動 '''
    dx = person1.x - person2.x
    dy = person1.y - person2.y
    delta_x = abs(dx) - width
    delta_y = abs(dy) - height
    if abs(dx) < width and abs(dy) < height:
        if abs(dx) > abs(dy):
            if person1.x < person2.x:
                person1.x += delta_x // 2
                person2.x -= (delta_x - delta_x // 2)
            else:
                person1.x -= delta_x // 2
                person2.x += (delta_x - delta_x // 2)
        else:
            if person1.y < person2.y:
                person1.y += delta_y
            else:
                person2.y += delta_y
class Person:
    ''' Person entitiy for our game '''
    def __init__(self, id_no):
        self.id = id_no + 1

        self.init_fixed_attributes()
        self.init_photo()
        self.init_controls()
        person_list.append(self)

    def init_fixed_attributes(self):
        ''' Initiazlizes the variables for person '''
        self.x = 455 - self.id * 40
        self.y = stair.stair_list[4].y - 60
        self.cloud_count = 0
        self.blackhole_size = 0
        self.life_count = 12
        self.alive = True
        self.animate_count = 0
        self.last_stair = None
        self.photos = {}
        self.direction = [0]

    def init_controls(self):
        ''' Initializes controls for person '''
        self.left = keys.keys[self.id - 1 % len(keys.keys)].left
        self.right = keys.keys[self.id - 1 % len(keys.keys)].right

    def init_photo(self):
        ''' Initializes the photos for person '''
        if self.id % 2 == 1:
            self.photos['right1'] = images.kungright1
            self.photos['right2'] = images.kungright2
            self.photos['left1'] = images.kungleft1
            self.photos['left2'] = images.kungleft2
            self.photos['front'] = images.kungfront
        else:
            self.photos['right1'] = images.smluright1
            self.photos['right2'] = images.smluright2
            self.photos['left1'] = images.smluleft1
            self.photos['left2'] = images.smluleft2
            self.photos['front'] = images.smlufront

        # default photo is front photo
        self.photo = self.photos['front']

    def update(self):
        ''' Handles all update related functions for person '''

        # Don't run update functions if dead
        if not self.alive:
            return

        # Handles vertical Movement
        self.y += 5

        self.capture_controls()
        self.boundary_check()
        self.photo_handling()

    def undraw(self):
        ''' Clears person graphic from screen '''
        settings.window.blit(images.background, [self.x, self.y - 5],
                             [self.x, self.y - 5, width, height + 5])

    def draw(self):
        ''' Draws person to screen '''
        if self.blackhole_size != 0:
            settings.window.blit(
                pygame.transform.scale(self.photo,
                                       (width - self.blackhole_size,
                                        height - self.blackhole_size * 2)),
                [self.x + self.blackhole_size // 2, self.y - 5 + self.blackhole_size * 2])
        else:
            settings.window.blit(self.photo, [self.x, self.y - 5])

    def boundary_check(self):
        ''' Checks and clamps the horizontal and vertical boundaries '''
        # Check horizontal bounds
        if self.x <= 31:
            self.x = 31
        if self.x + width >= settings.game_width - 31:
            self.x = settings.game_width - width - 31

        if self.y - height > settings.game_height:
            self.death()

        if self.y <= 40:
            sounds.sounds["Hurt"].play()
            stair.stair_list[0].pass_through = True
            self.life_count += -5
            if self.life_count <= 0:
                self.death()

    def capture_controls(self):
        ''' Handles pygame events '''
        for event in settings.events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.left:
                    self.direction.append(-5)
                elif event.key == self.right:
                    self.direction.append(5)
            elif event.type == pygame.KEYUP:
                if event.key == self.left:
                    self.direction.remove(-5)
                elif event.key == self.right:
                    self.direction.remove(5)

    def death(self):
        ''' Handles person death '''
        if settings.godmode:
            self.life_count = 12
            self.y = 40
            return

        sounds.sounds["Death"].play()
        self.alive = False
        self.life_count = 0
        self.y = 1000
        settings.living_players -= 1
        if settings.living_players <= 0:
            settings.current_screen = game_over

    def photo_handling(self):
        ''' Sets photo to the correct one based on direction and animation '''
        self.animate_count += 1
        # Handles horizontal movements
        self.x += self.direction[-1]
        if self.direction[-1] == 5:
            if self.animate_count > 10:
                self.photo = self.photos['right1']
                if self.animate_count > 20:
                    self.animate_count = 0
            else:
                self.photo = self.photos['right2']
        elif self.direction[-1] == -5:
            if self.animate_count > 10:
                self.photo = self.photos['left1']
                if self.animate_count > 20:
                    self.animate_count = 0
            else:
                self.photo = self.photos['left2']
        else:
            self.photo = self.photos['front']
        