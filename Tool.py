import pygame
import Exceptions


# color set
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255) 

game_display = None
display_width =  0
display_height = 0
clock = None
death_count = 0
players = 0
sounds = {}


def Init(display, width, height, clock_):
    global game_display
    global display_width
    global display_height
    global clock
    global death_count
    game_display = display
    display_width = width
    display_height = height
    clock = clock_
    death_count = 0

def AddSound(name, sound):
    sounds[name] = sound

def TextObjects(text, font, color = black):
    """ Change word to graphics """
    text_surface = font.render(text, True, color) 
    return text_surface, text_surface.get_rect()

def Button(where,msg,x,y,w,h,ic,ac,action = None):
    """ Create button"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # change color
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(where, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(where, ic,(x,y,w,h))

    small_font = pygame.font.Font("freesansbold.ttf",32)
    text_surf, text_rect = TextObjects(msg, small_font)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    where.blit(text_surf, text_rect) 

def PictureButton(where,picture_pre,picture_after,x,y,w,h,action = None):
     """ Create Picture Button"""
     mouse = pygame.mouse.get_pos()
     click = pygame.mouse.get_pressed()
     
     # change color
     if x+w > mouse[0] > x and y+h > mouse[1] > y:
         #pygame.draw.rect(where, ac,(x,y,w,h))
         where.blit(picture_after, (x, y))
         if click[0] == 1 and action != None:
             action()
     else:
         #pygame.draw.rect(where, ic,(x,y,w,h))
         where.blit(picture_pre, (x, y))

     #small_font = pygame.font.Font("freesansbold.ttf",32)
     #text_surf, text_rect = TextObjects(msg, small_font)
     #text_rect.center = ( (x+(w/2)), (y+(h/2)) )
     #where.blit(text_surf, text_rect) 

def GameEndCount():
    global death_count
    death_count += 1
    
    if death_count == players:
        GameEnd()



def GameEnd():
    """Define Game End Screen"""

    def GameEndRestart():
            raise Exceptions.GameOverError

    def RestartButton():
        
        button_width_factor = 0.11
        button_height_factor = 0.09
        Button(game_display, "RESTART", display_width / 2 + 180, display_height / 1.15, 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        green, bright_green, GameEndRestart)             
        
    fail = True

    while fail:

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GameEndRestart()
               
        # Background and text display
        game_display.fill(white)
        game_font = pygame.font.Font('JT1-09U.TTF', 115)
        end_text = game_font.render("GAME OVER !!", True, red) 
        end_rect = end_text.get_rect()
        end_rect.center = ((display_width / 2),(display_height / 5))
        game_display.blit(end_text, end_rect)

        score_font = pygame.font.Font('JT1-09U.TTF', 100)
        end_score_text, end_score_rect = TextObjects("得分：", score_font)
        end_score_rect.center = ((display_width / 2 - 140), (display_height / 2.1))
        game_display.blit(end_score_text, end_score_rect)

        highest_font = pygame.font.Font('JT1-09U.TTF', 80)
        highest_text, highest_rect = TextObjects("歷史高分：", highest_font)
        highest_rect.center = ((display_width / 2 - 200), (display_height / 1.5))
        game_display.blit(highest_text, highest_rect)

        bottomtext_font = pygame.font.Font('JT1-09U.TTF', 50)
        bottomtext_text, bottomtext_rect = TextObjects("太可惜了！再來一次吧！", bottomtext_font)
        bottomtext_rect.center = ((display_width / 2 - 120), (display_height / 1.1))
        game_display.blit(bottomtext_text, bottomtext_rect)


        RestartButton()
    # if score > highest_score:            # highest score用global，一開始就抓

        pygame.display.update()
        clock.tick(15)

