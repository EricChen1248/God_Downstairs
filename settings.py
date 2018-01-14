''' Stores shared setting variables '''
#pylint: disable-msg=C0103
window = None
clock = None
events = []

window_width = 1200
window_height = 640
game_width = int(window_width * 0.6)
game_height = int(window_height)

game_speed = 60

player_count = 1
hiscore = 0
living_players = 0

current_screen = None
current_status = None

alt = False
f4 = False
godmode = False
