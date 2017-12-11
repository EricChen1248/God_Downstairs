def GameStart():
    """Define Game Intro screen"""
    intro = True
    
    button_width_factor = 0.18
    button_height_factor = 0.1
       
    def StartGame():
        nonlocal intro
        intro = False
        
    def StartButton():
        button_width_factor = 0.18
        button_height_factor = 0.1
        Button("START", display_width / 2 * (1 - button_width_factor), display_height * 0.7 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        green, bright_green, StartGame)
        
    def PlayerOneButton():
        Button("1 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        red, bright_red, TogglePlayer2)

    def PlayerTwoButton():
        Button("2 Player", display_width / 2 * (1 - button_width_factor), display_height * 0.5 * (1 - button_height_factor), 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        red, bright_red, TogglePlayer1)
   
    def TogglePlayer2():
        nonlocal players
        players = 2
        clock.tick(20)

    def TogglePlayer1():
        nonlocal players
        players = 1
        clock.tick(20)

    players = 1
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
        start_rect.center = ((display_width / 2), (display_height / 4))
        game_display.blit(start_name, start_rect)
        
        ''' pygame.draw.rect(game_display, (100,100,100), (255,255,main_width,main_height))
        pygame.draw.rect(game_display, (125,125,125), (250,250,main_width,main_height)) '''


        StartButton()    

        if players == 1:
            PlayerOneButton()
        else:
            PlayerTwoButton()

        pygame.display.update()
        clock.tick(15)





def GameEnd():
    """Define Game End Screen"""


    def RestartButton():
        button_width_factor = 0.11
        button_height_factor = 0.09
        Button("RESTART", display_width / 2 + 180, display_height / 1.15, 
                        display_width * button_width_factor, display_height * button_height_factor, 
                        green, bright_green, GameLoop)
    
    fail = True

    while fail:

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
               
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


