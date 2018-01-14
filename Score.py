''' Handles score related logic '''
#pylint: disable-msg=C0103, W0603
import settings
from config import update_config
score = 0
count = 0

def update():
    ''' Update score '''
    global count
    count += 1
    if count >= 20:
        global score
        score += 1
        count -= 20
    if score % 50 == 0:
        settings.game_speed += 0.2

def check_hiscore():
    '''' Checks if hiscore is beat and resets score '''
    global score
    global count
    if score >= settings.hiscore:
        update_config(score)
        settings.hiscore = score

    score = 0
    count = 0
