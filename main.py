import pygame
import random

# Inicializace hry
pygame.init()

# Obrazovka
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Harry Potter a Ohnivý pohár")

# Nastavení hry
player_start_lives = 5  # Měníme
player_speed = 5  # Neměníme
egg_speed = 5  # Měníme
egg_speed_acceleration = 0.5  # Neměníme
egg_behind_border = 100  # Neměníme
score = 0  # Měníme

player_lives = player_start_lives
egg_current_speed = egg_speed

# FPS a hodiny
fps = 60
clock = pygame.time.Clock()

# Barvy
dark_yellow = pygame.Color("#938f0c")
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Fonty
harry_font_big = pygame.font.Font("fonts/Harry.ttf", 50)
harry_font_middle = pygame.font.Font("fonts/Harry.ttf", 30)

# Text
game_name = harry_font_big.render("Harry Potter and Goblet of Fire ", True, dark_yellow)
game_name_rect = game_name.get_rect()
game_name_rect.center = (width//2, 30)

game_over_text = harry_font_big.render("Hra skoncila.", True, dark_yellow)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (width//2, height//2)

continue_text = harry_font_middle.render("Chces hrat znovu? Stiskni libovolnou klavesu.", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width//2, height//2 + 40)

# Zvuky a muzika v pozadí
pygame.mixer.music.load("media/bg-music-hp.wav")
pygame.mixer.music.play(-1, 0.0)
loose_life_sound = pygame.mixer.Sound("media/boom.wav")
loose_life_sound.set_volume(0.1)
take_egg_sound = pygame.mixer.Sound("media/take_egg.wav")
take_egg_sound.set_volume(0.1)

# Obrázky
harry_image = pygame.image.load("img/harryPotter.png")
harry_image_rect = harry_image.get_rect()
harry_image_rect.center = (60, height//2)

egg_image = pygame.image.load("img/egg-icon.png")
egg_image_rect = egg_image.get_rect()
egg_image_rect.x = width + egg_behind_border
egg_image_rect.y = random.randint(60, height-48)

# Hlavní cyklus
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

    # Pohyb klávesami
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and harry_image_rect.top > 60:
        harry_image_rect.y -= player_speed
    elif keys[pygame.K_DOWN] and harry_image_rect.bottom < height:
        harry_image_rect.y += player_speed

    # Pohyb vejce
    if egg_image_rect.x < 0:
        player_lives -= 1
        egg_image_rect.x = width + egg_behind_border
        egg_image_rect.y = random.randint(60, height-48)
        loose_life_sound.play()
    else:
        egg_image_rect.x -= egg_current_speed

    # Kontrola kolize
    if harry_image_rect.colliderect(egg_image_rect):
        score += 1
        egg_current_speed += egg_speed_acceleration
        egg_image_rect.x = width + egg_behind_border
        egg_image_rect.y = random.randint(60, height-48)
        take_egg_sound.play()

    # Znovu vykreslení obrazovky
    screen.fill(black)

    # Tvary
    pygame.draw.line(screen, dark_yellow, (0, 60), (width, 60), 2)

    # Nastavení textů
    lives_text = harry_font_middle.render(f"Zivoty: {player_lives}", True, dark_yellow)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.right = width - 20
    lives_text_rect.top = 15

    score_text = harry_font_middle.render(f"Skore: {score}", True, dark_yellow)
    score_text_rect = score_text.get_rect()
    score_text_rect.left = 20
    score_text_rect.top = 15

    # Texty - vykreslení
    screen.blit(game_name, game_name_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)

    # Obrázky
    screen.blit(harry_image, harry_image_rect)
    screen.blit(egg_image, egg_image_rect)

    # Kontrola konce hry
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_start_lives
                    egg_current_speed = egg_speed
                    harry_image_rect.y = height//2
                    pause = False
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False

    # Update obrazovky
    pygame.display.update()

    # Zpomalení cyklus - tikání hodin
    clock.tick(fps)

# Ukončení hry
pygame.quit()
