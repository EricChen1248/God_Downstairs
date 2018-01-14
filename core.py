''' Holds most of our core game logic '''
#pylint: disable-msg=C0103
import pygame

import images
import person
import score
import settings
import stair
import helper
from helper import Color
from filepath import File_Path

def start_game():
    ''' Intializes start screen '''
    settings.window.blit(images.background_intro, [0, -15])
    game_font = pygame.font.Font(File_Path.msjenghei, 30)

    # Sets initial player count text
    if settings.player_count == 1:
        p1 = Color.red
        p2 = Color.white
    elif settings.player_count == 2:
        p1 = Color.white
        p2 = Color.red
    else:
        p1 = Color.white
        p2 = Color.white

    p1_text, p1_rect = helper.text_object("1P", game_font, settings.window_width / 2 * 0.78,
                                          settings.window_height * 0.43 - 30, p1)
    settings.window.blit(p1_text, p1_rect)
    p2_text, p2_rect = helper.text_object("2P", game_font, settings.window_width / 2 * 1.12,
                                          settings.window_height * 0.43 - 30, p2)
    settings.window.blit(p2_text, p2_rect)
    settings.current_status = helper.Game_Status.start
    settings.current_screen = start_screen

def toggle_2player():
    ''' Sets player count to 2 '''
    settings.player_count = 2
    game_font = pygame.font.Font(File_Path.msjenghei, 30)
    p1_text, p1_rect = helper.text_object("1P", game_font, settings.window_width / 2 * 0.78,
                                          settings.window_height * 0.43 - 30, Color.white)
    settings.window.blit(p1_text, p1_rect)
    p2_text, p2_rect = helper.text_object("2P", game_font, settings.window_width / 2 * 1.12,
                                          settings.window_height * 0.43 - 30, Color.red)
    settings.window.blit(p2_text, p2_rect)

def toggle_1player():
    ''' Sets player count to 1 '''
    settings.player_count = 1
    game_font = pygame.font.Font(File_Path.msjenghei, 30)
    p1_text, p1_rect = helper.text_object("1P", game_font, settings.window_width / 2 * 0.78,
                                          settings.window_height * 0.43 - 30, Color.red)
    settings.window.blit(p1_text, p1_rect)
    p2_text, p2_rect = helper.text_object("2P", game_font, settings.window_width / 2 * 1.12,
                                          settings.window_height * 0.43 - 30, Color.white)
    settings.window.blit(p2_text, p2_rect)

def start_button():
    ''' Display start button '''
    button_width_factor = 0.18
    button_height_factor = 0.1
    helper.button("START", settings.window_width / 2 * 0.8, settings.window_height * 0.65,
                  settings.window_width * button_width_factor,
                  settings.window_height * button_height_factor,
                  Color.green, Color.bright_green, start)

def start():
    ''' Starts game '''
    settings.current_status = helper.Game_Status.running
    settings.current_screen = game_core_init

def start_screen():
    ''' Starting Screen, Chooses player count and begins game '''
    settings.events = pygame.event.get()
    for event in settings.events:
        if event.type == pygame.QUIT:
            helper.quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                toggle_1player()
            if event.key == pygame.K_RIGHT:
                toggle_2player()
            if event.key == pygame.K_SPACE:
                start()

    start_button()
    helper.picture_button(images.kungfront, settings.window_width / 2 * 0.75,
                          settings.window_height * 0.48 - 15, settings.window_width * 0.18,
                          settings.window_height * 0.1, toggle_1player)
    helper.picture_button(images.two_pre, settings.window_width / 2 * 1.05,
                          settings.window_height * 0.48 - 15, settings.window_width * 0.85,
                          settings.window_height * 0.1, toggle_2player)

    helper.check_alt_f4()
    pygame.display.update()
    settings.clock.tick(15)

def game_core_init():
    ''' Inits game core '''
    settings.current_screen = game_core
    settings.living_players = settings.player_count

    # background
    settings.window.fill(Color.white.value)
    settings.window.blit(images.background, [0, 0])

    # title
    game_font = pygame.font.Font(File_Path.jetlinkbold1, 60)
    title_name, title_rect = helper.text_object(
        "小傑小銘下樓梯", game_font, settings.window_width * 0.8, settings.window_height * 0.05)
    settings.window.blit(title_name, title_rect)

    initialize_game_stat_display()
    initialize_user_info_display()
    initialize_life_display()

    stair.reset_stair()
    for i in range(8):
        stair.generate_stair(i)
    stair.stair_list[4] = stair.Stair(4)
    stair.stair_list[4].x = 300

    person.reset_person_list()
    for i in range(settings.player_count):
        person.Person(i)

    pygame.display.update()

def initialize_life_display():
    ''' Draws life graphics in side bar '''
    game_font = pygame.font.Font(File_Path.msjenghei, 36)
    for j in range(settings.player_count):
        title_name, title_rect = helper.text_object(
            "命：", game_font, settings.window_width * 0.65, settings.window_height * 0.45 + 120 * j)
        settings.window.blit(title_name, title_rect)

        for i in range(12):
            pygame.draw.rect(settings.window, Color.black.value,
                             [settings.window_width * (0.7 + 0.0195 * i),
                              settings.window_height * 0.42 + 120 * j,
                              settings.window_width * 0.02,
                              settings.window_height*0.06], 1)

def initialize_user_info_display():
    ''' Setup the basic user info in sidebar '''
    game_font = pygame.font.Font(File_Path.msjenghei, 36)
    for i in range(settings.player_count):
        if i % 2 == 0:
            user_image = pygame.image.load(File_Path.lckung)
            user_image_size = pygame.transform.scale(
                user_image, (int(settings.window_width * 0.05), int(settings.window_height * 0.1)))
            settings.window.blit(
                user_image_size, [settings.window_width * 0.62, settings.window_height * 0.3])

            user_name, user_rect = helper.text_object(
                "小傑", game_font, settings.window_width * 0.72, settings.window_height * 0.35)
            settings.window.blit(user_name, user_rect)
        else:
            user_image_size = pygame.transform.scale(
                pygame.image.load(File_Path.smlu),
                (int(settings.window_width * 0.05), int(settings.window_height * 0.1)))

            settings.window.blit(
                user_image_size, [settings.window_width * 0.62, settings.window_height * 0.5])

            user_name, user_rect = helper.text_object(
                "小銘", game_font, settings.window_width * 0.72, settings.window_height * 0.55)
            settings.window.blit(user_name, user_rect)

def initialize_game_stat_display():
    ''' Setup and draw game stat in sidebar '''
    # history highest score
    game_font = pygame.font.Font(File_Path.msjenghei, 36)
    title_name, title_rect = helper.text_object(
        "歷史高分： " + str(settings.hiscore), game_font, settings.window_width * 0.72,
        settings.window_height * 0.15)
    title_rect.x = settings.window_width * 0.62
    settings.window.blit(title_name, title_rect)

    # Current score
    game_font = pygame.font.Font(File_Path.msjenghei, 48)
    title_name, title_rect = helper.text_object(
        "現在分數：", game_font, settings.window_width * 0.72, settings.window_height * 0.25)
    title_rect.center = ((settings.window_width * 0.72), (settings.window_height * 0.25))
    settings.window.blit(title_name, title_rect)
    return game_font

def game_core():
    ''' Actual game core '''
    game_background()
    settings.events = pygame.event.get()
    stair.regen_stair()

    for s in stair.stair_list:
        s.update()

    for p in person.person_list:
        p.update()

        try:
            s = stair.stair_list[(p.y - 33) // 75]
            if s.collision_check(p):
                s.collide(p)
        except IndexError:
            pass

        try:
            s = stair.stair_list[(p.y - 33) // 75 + 1]
            if s.collision_check(p):
                s.collide(p)
        except IndexError:
            pass

        for p2 in person.person_list:
            if p != p2:
                person.person_interaction(p, p2)

    score.update()
    update_game_graphics()

    helper.check_alt_f4()
    for event in settings.events:
        if event.type == pygame.QUIT:
            helper.quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause()

    pygame.display.update()

    settings.clock.tick(settings.game_speed)

def update_game_graphics():
    ''' Handles game graphics '''
    for s in stair.stair_list:
        settings.window.blit(s.photo, [s.x, s.y])

    # person & life
    for j in range(settings.player_count):
        p = person.person_list[j]
        p.draw()

        life = p.life_count
        for i in range(life):
            pygame.draw.rect(settings.window, Color.red.value,
                             [settings.window_width * (0.7 + 0.0195 * i) + 1,
                              settings.window_height * 0.42 + 120 * j + 1,
                              settings.window_width * 0.02 - 2,
                              settings.window_height * 0.06 - 2])

        for i in range(12 - life):
            pygame.draw.rect(settings.window, Color.white.value,
                             [settings.window_width * (0.7 + 0.0195 * (life + i)) + 1,
                              settings.window_height * 0.42 + 120 * j + 1,
                              settings.window_width * 0.02 - 2,
                              settings.window_height * 0.06 - 2])

    # Current score
    pygame.draw.rect(settings.window, Color.white.value,
                     [settings.window_width* 0.82, settings.window_height * 0.2, 300, 60])

    game_font = pygame.font.Font(File_Path.msjenghei, 48)
    title_name, title_rect = helper.text_object(str(score.score), game_font,
                                                settings.window_width * 0.85,
                                                settings.window_height * 0.25)
    title_rect.x = settings.window_width * 0.82
    settings.window.blit(title_name, title_rect)

    # Pause and Restart(Button)
    helper.button("Pause!",
                  settings.window_width * 0.7, settings.window_height * 0.7,
                  settings.window_width * 0.2, settings.window_height * 0.1,
                  Color.green, Color.bright_green, pause)
    helper.button("Restart!",
                  settings.window_width * 0.7, settings.window_height * 0.85,
                  settings.window_width * 0.2, settings.window_height * 0.1,
                  Color.red, Color.bright_red, restart)

def restart():
    ''' Restart game '''
    score.check_hiscore()
    settings.game_speed = 60
    settings.current_screen = start_game

def pause():
    ''' Pause game '''
    def unpause():
        ''' Unpauses pause screen '''
        nonlocal pause_state
        pause_state = False

    # Remove original button
    pygame.draw.rect(settings.window, Color.white.value,
                     (settings.window_width * 0.7,
                      settings.window_height * 0.7,
                      settings.window_width * 0.2,
                      settings.window_height * 0.1))
    pygame.draw.rect(settings.window, Color.white.value,
                     (settings.window_width * 0.7,
                      settings.window_height * 0.85,
                      settings.window_width * 0.2,
                      settings.window_height * 0.1))

    large_text = pygame.font.Font(File_Path.freesansbold, 115)
    text_surf, text_rect = helper.text_object("Paused", large_text,
                                              settings.game_width / 2, settings.game_height * 0.4,
                                              Color.red)

    pause_state = True
    while pause_state:
        settings.window.blit(text_surf, text_rect)
        settings.events = pygame.event.get()
        helper.button("Continue", settings.window_width * 0.05,
                      settings.window_height * 0.7,
                      settings.window_width * 0.6 * 0.3,
                      settings.window_height * 0.2,
                      Color.green,
                      Color.bright_green, unpause)

        helper.button("Quit", settings.window_width * 0.38,
                      settings.window_height * 0.7,
                      settings.window_width * 0.6 * 0.3,
                      settings.window_height * 0.2,
                      Color.red,
                      Color.bright_red,
                      helper.quit_game)

        for event in settings.events:
            helper.check_alt_f4()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    unpause()

            if event.type == pygame.QUIT:
                helper.quit_game()

        pygame.display.update()
        settings.clock.tick(15)
    settings.window.blit(images.background, [0, 0])

def game_background():
    ''' Undraw entities '''
    for p in person.person_list:
        p.undraw()
    for s in stair.stair_list:
        settings.window.blit(images.background, [s.x, s.y], [s.x, s.y, 150, 40])

def restart_button():
    ''' Restart button on the end game screen '''
    button_width_factor = 0.15
    button_height_factor = 0.09
    helper.button("RESTART", settings.window_width / 2 + 180, settings.window_height / 1.15,
                  settings.window_width * button_width_factor,
                  settings.window_height * button_height_factor,
                  Color.green, Color.bright_green, restart)

def game_over():
    ''' Game over screen '''
    settings.events = pygame.event.get()
    settings.window.fill(Color.white.value)
    game_font = pygame.font.Font(File_Path.jetlinkbold1, 115)
    end_text, end_rect = helper.text_object("GAME OVER !!", game_font,
                                            settings.window_width / 2,
                                            settings.window_height / 5, Color.red)
    settings.window.blit(end_text, end_rect)

    score_font = pygame.font.Font(File_Path.jetlinkbold1, 100)
    end_score_text, end_score_rect = helper.text_object("得分： " + str(score.score), score_font,
                                                        settings.window_width / 2,
                                                        settings.window_height / 2.1)
    settings.window.blit(end_score_text, end_score_rect)

    highest_font = pygame.font.Font(File_Path.jetlinkbold1, 80)
    highest_text, highest_rect = helper.text_object("歷史高分： " + str(settings.hiscore),
                                                    highest_font,
                                                    settings.window_width / 2,
                                                    settings.window_height / 1.5)
    settings.window.blit(highest_text, highest_rect)

    bottomtext_font = pygame.font.Font(File_Path.jetlinkbold1, 50)
    bottomtext_text, bottomtext_rect = helper.text_object("太可惜了！再來一次吧！",
                                                          bottomtext_font,
                                                          settings.window_width / 2 - 120,
                                                          settings.window_height / 1.1)
    settings.window.blit(bottomtext_text, bottomtext_rect)

    restart_button()

    for event in settings.events:
        if event.type == pygame.QUIT:
            helper.quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restart()

    pygame.display.update()
    settings.clock.tick(15)
