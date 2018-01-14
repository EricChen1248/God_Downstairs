''' stores and loads resources used by game '''
#pylint: disable-msg=C0103, W0603
import pygame
import settings
import person
import stair
from filepath import File_Path

background = None
two_pre = None
background_intro = None
blackhole = None
cloud = None
normal = None
lckung = None
smlu = None
sting = None
kungright1 = None
kungright2 = None
kungleft1 = None
kungleft2 = None
kungfront = None
smluright1 = None
smluright2 = None
smluleft1 = None
smluleft2 = None
smlufront = None

hurt_sound = None
death_sound = None


def init():
    ''' Loads in all resources '''
    global background
    background = pygame.transform.scale(
        pygame.image.load(File_Path.background).convert_alpha(),
        (settings.game_width, settings.game_height))
    global two_pre
    two_pre = pygame.transform.scale(
        pygame.image.load(File_Path.two_pre).convert_alpha(),
        (person.width * 2 + 5, person.height))
    global background_intro
    background_intro = pygame.transform.scale(
        pygame.image.load(File_Path.backgroundintro).convert_alpha(),
        (settings.window_width, settings.window_height))
    global blackhole
    blackhole = pygame.transform.scale(
        pygame.image.load(File_Path.blackhole).convert_alpha(),
        (stair.width, stair.height + 20))
    global cloud
    cloud = pygame.transform.scale(
        pygame.image.load(File_Path.cloud).convert_alpha(),
        (stair.width, stair.height + 20))
    global normal
    normal = pygame.transform.scale(
        pygame.image.load(File_Path.normal).convert_alpha(),
        (stair.width, stair.height))
    global lckung
    lckung = pygame.transform.scale(
        pygame.image.load(File_Path.lckung).convert_alpha(),
        (int(settings.window_width * 0.05), int(settings.window_height * 0.1)))
    global smlu
    smlu = pygame.transform.scale(
        pygame.image.load(File_Path.smlu).convert_alpha(),
        (int(settings.window_width * 0.05), int(settings.window_height * 0.1)))
    global sting
    sting = pygame.transform.scale(
        pygame.image.load(File_Path.sting).convert_alpha(),
        (stair.width, stair.height))
    global kungright1
    kungright1 = pygame.transform.scale(
        pygame.image.load(File_Path.kungright1).convert_alpha(),
        (person.width, person.height))
    global kungright2
    kungright2 = pygame.transform.scale(
        pygame.image.load(File_Path.kungright2).convert_alpha(),
        (person.width, person.height))
    global kungleft1
    kungleft1 = pygame.transform.scale(
        pygame.image.load(File_Path.kungleft1).convert_alpha(),
        (person.width, person.height))
    global kungleft2
    kungleft2 = pygame.transform.scale(
        pygame.image.load(File_Path.kungleft2).convert_alpha(),
        (person.width, person.height))
    global kungfront
    kungfront = pygame.transform.scale(
        pygame.image.load(File_Path.kungfront).convert_alpha(),
        (person.width, person.height))
    global smluright1
    smluright1 = pygame.transform.scale(
        pygame.image.load(File_Path.smluright1).convert_alpha(),
        (person.width, person.height))
    global smluright2
    smluright2 = pygame.transform.scale(
        pygame.image.load(File_Path.smluright2).convert_alpha(),
        (person.width, person.height))
    global smluleft1
    smluleft1 = pygame.transform.scale(
        pygame.image.load(File_Path.smluleft1).convert_alpha(),
        (person.width, person.height))
    global smluleft2
    smluleft2 = pygame.transform.scale(
        pygame.image.load(File_Path.smluleft2).convert_alpha(),
        (person.width, person.height))
    global smlufront
    smlufront = pygame.transform.scale(
        pygame.image.load(File_Path.smlufront).convert_alpha(),
        (person.width, person.height))
