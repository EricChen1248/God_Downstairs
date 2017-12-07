import pygame

pygame.init()  # remove it when combining files! init() can only be called once

display_width = 1366
display_height = 768
game_display = pygame.display.set_mode((display_width, display_height))

# game clock
clock = pygame.time.Clock()


white = (255, 255, 255)
black = (0, 0, 0)

def TextObjects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def GameStart():
    """Define Game Intro screen"""

    intro = True

    main_width = 500
    main_height = 250
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # display background and text
    
        ''' start_background = pygame.image.load('background.png') # 弄圖片
        game_display.fill(start_background) '''
        game_display.fill(white)
        game_font = pygame.font.Font('JT1-09U.TTF', 115)
        start_name, start_rect = TextObjects("小傑下樓梯~", game_font)
        start_rect.center = ((display_width / 3), (display_height / 4))
        game_display.blit(start_name, start_rect)
        
        ''' pygame.draw.rect(game_display, (100,100,100), (255,255,main_width,main_height))
        pygame.draw.rect(game_display, (125,125,125), (250,250,main_width,main_height)) '''

        mouse = pygame.mouse.get_pos()

        
        
        pygame.display.update()
        clock.tick(60)

GameStart()


