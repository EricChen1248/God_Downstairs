''' helper module storing commonly used shared functions '''
#pylint: disable-msg=C0103
from enum import Enum
import pygame
import settings
from filepath import File_Path

class Color(Enum):
    ''' Holds used color values of the game '''
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (200, 0, 0)
    green = (0, 200, 0)
    bright_red = (255, 0, 0)
    bright_green = (0, 255, 0)
    block_color = (53, 115, 255)

class Game_Status(Enum):
    ''' Current game status '''
    start = 0
    running = 1
    ending = 2

def check_alt_f4():
    ''' Checks for alt f4 key press '''
    for event in settings.events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                settings.alt = True

            elif event.key == pygame.K_F4:
                settings.f4 = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                settings.alt = False

            elif event.key == pygame.K_F4:
                settings.f4 = False

        if settings.alt and settings.f4:
            quit_game()

def quit_game():
    ''' Handles quit game logic '''
    pygame.quit()
    quit()

def button(msg, x, y, width, height, original_color, hover_color, action,
           font=None, font_size=32):
    ''' Used for drawing text buttons '''

    if font == None:
        font = File_Path.freesansbold
    mouse = pygame.mouse.get_pos()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(settings.window, hover_color.value, (x, y, width, height))
        for event in settings.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                action()
    else:
        pygame.draw.rect(settings.window, original_color.value, (x, y, width, height))
    font = pygame.font.Font(font, font_size)
    text_surf, text_rect = text_object(msg, font, x + width / 2, y + height / 2)
    settings.window.blit(text_surf, text_rect)

def picture_button(picture, x, y, width, height, action):
    ''' Used for drawing picture buttons '''
    mouse = pygame.mouse.get_pos()
    settings.window.blit(picture, (x, y))

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        for event in settings.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                action()

def text_object(text, font, center_x, center_y, color=Color.black):
    ''' Returns texts as objects '''
    text_surface = font.render(text, True, color.value)
    center = text_surface.get_rect()
    center.center = (center_x, center_y)
    return text_surface, center
