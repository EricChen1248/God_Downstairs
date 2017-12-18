import pygame

display_width = 1200
display_height = 640
game_display = pygame.display.set_mode((display_width,display_height))

# color set
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255) 

def TextObjects(text, font, color = black):
    """ Change word to graphics """
    text_surface = font.render(text, True, color) 
    return text_surface, text_surface.get_rect()

def Button(msg,x,y,w,h,ic,ac,action = None):
    """ Create button"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # change color
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, ic,(x,y,w,h))

    small_font = pygame.font.Font("freesansbold.ttf",32)
    text_surf, text_rect = TextObjects(msg, small_font)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(text_surf, text_rect) 