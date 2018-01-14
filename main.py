''' Entry point of our game '''
from os import environ

import pygame
import sounds
import filepath
import settings
import images
import config
from core import start_game


# Sets starting window position
environ['SDL_VIDEO_WINDOW_POS'] = '20,34'

# initialization and display
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.display.set_caption('小傑下樓梯')

settings.window = pygame.display.set_mode((settings.window_width, settings.window_height - 15))
settings.clock = pygame.time.Clock()

filepath.init()
images.init()
config.load_config()
sounds.load_sounds()

settings.current_screen = start_game
while True:
    settings.current_screen()
