''' Stores and handles all sound files in our game '''
from pygame import mixer
from filepath import File_Path

sounds = {}

def load_sounds():
    ''' Loads sound file into library '''
    sounds['Hurt'] = mixer.Sound(File_Path.hurtsound)
    sounds['Death'] = mixer.Sound(File_Path.deathsound)

def play_sound(sound):
    ''' Plays sound from library '''
    sounds[sound].play()
