import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

current_volume = 0.3

pygame.mixer.music.load('assets/sounds/otherworldly_oceanside.wav')
pygame.mixer.music.set_volume(0.3)

pygame.mixer.music.play(-1)

pause_img_raw = pygame.image.load('assets/images/pause_bg.png')
pause_img = pygame.transform.scale(pause_img_raw, (390,300))

minus_img_raw = pygame.image.load('assets/images/minus.png')
minus_img = pygame.transform.scale(minus_img_raw, (40, 40))

plus_img_raw = pygame.image.load('assets/images/plus.png')
plus_img = pygame.transform.scale(plus_img_raw, (40, 40))

go_img_raw = pygame.image.load('assets/images/game_over_bg.png')
go_img = pygame.transform.scale(go_img_raw, (390, 300))

fish_sound = pygame.mixer.Sound('assets/sounds/whoosh-clean.mp3')
fish_sound.set_volume(0.3)
score_sound = pygame.mixer.Sound('assets/sounds/bubble-pop.mp3')
score_sound.set_volume(0.3)
game_over_sound = pygame.mixer.Sound('assets/sounds/game-over-button.mp3')
game_over_sound.set_volume(0.3)

WIDTH = 500
HEIGHT = 680

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flabby Fish")
icon_surface = pygame.image.load('assets/images/icon.png')

pygame.display.set_icon(icon_surface)

ng_font = pygame.font.Font('assets/fonts/PixeloidSans-Bold.otf', 60)
fonts = pygame.font.Font('assets/fonts/PixeloidSans-Bold.otf', 70)
vol_font = pygame.font.Font('assets/fonts/PixeloidSans-Bold.otf', 30)

clock = pygame.time.Clock()

ocean_img_raw = pygame.image.load('assets/images/ocean.png')
ocean_img = pygame.transform.scale(ocean_img_raw, (WIDTH, HEIGHT))

flabby_img_raw = pygame.image.load('assets/images/flappy_fish.png')
flabby_img = pygame.transform.scale(flabby_img_raw, (80,80))

bubble_img_raw = pygame.image.load('assets/images/bubble.png')
bubble_img = pygame.transform.scale(bubble_img_raw, (20,20))

#T1
bottle_img_raw = pygame.image.load('assets/images/bottle.png')
bottle_img = pygame.transform.scale(bottle_img_raw, (60,60))

glass_img_raw = pygame.image.load('assets/images/glass.png')
glass_img = pygame.transform.scale(glass_img_raw, (60,60))

pb_img_raw = pygame.image.load('assets/images/plastic_bag.png')
pb_img = pygame.transform.scale(pb_img_raw, (60, 60))

#T2
tb_img_raw = pygame.image.load('assets/images/trash_bag.png')
tb_img = pygame.transform.scale(tb_img_raw, (60,60))

straw_img_raw = pygame.image.load('assets/images/straw.png')
straw_img = pygame.transform.scale(straw_img_raw, (60,60))

mc_img_raw = pygame.image.load('assets/images/metal_cans.png')
mc_img = pygame.transform.scale(mc_img_raw, (60,60))

#T3
apple_img_raw = pygame.image.load('assets/images/apple.png')
apple_img = pygame.transform.scale(apple_img_raw, (60,60))

mc2_img_raw = pygame.image.load('assets/images/metal_cans2.png')
mc2_img = pygame.transform.scale(mc2_img_raw, (60,60))

fb_img_raw = pygame.image.load('assets/images/fish_bone.png')
fb_img = pygame.transform.scale(fb_img_raw, (60,60))

bg_x1 = 0
bg_x2 = WIDTH
scroll_speed = 2

menu_width = 390
menu_height = 300

#Menu
menu_x = (WIDTH - menu_width) // 2
menu_y = (HEIGHT - menu_height) // 2

minus_btn_rect = pygame.Rect(menu_x + 60, menu_y + 140, 50, 40)
plus_btn_rect = pygame.Rect(menu_x + 290, menu_y + 140, 50, 40)

#Fish
fish_x = 50
fish_y = 300

fish_velocity = 0

GRAVITY = 0.3
JUMP_STRENGTH = -6

#trash
trash_radius = 20
trash_speed = 3

t1_x = WIDTH
t1_y = random.randint(100,500)
t1_type = random.randint(1,3)

t2_x = WIDTH + 200
t2_y = random.randint(100,500)
t2_type = random.randint(1,3)

t3_x = WIDTH + 400
t3_y = random.randint(100,500)
t3_type = random.randint(1,3)


#bullet
bullet_x = fish_x
bullet_y = fish_y
bullet_speed = 15

game_over = False
game_pause = False
game_started = False
score = 0

high_score_file = "highscore.txt"
high_score = 0
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        try:
            high_score = int(f.read().strip())
        except:
            high_score = 0

running = True

play_btn_rect = pygame.Rect(150, 280, 200, 60)
quit_btn_rect = pygame.Rect(150, 380, 200, 60)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            mouse_pos = pygame.mouse.get_pos()

            if play_btn_rect.collidepoint(mouse_pos):
                game_started = True

            if quit_btn_rect.collidepoint(mouse_pos):
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_pause:
            mouse_pos = pygame.mouse.get_pos()
            if minus_btn_rect.collidepoint(mouse_pos):
                current_volume = max(0.0, current_volume - 0.1)
                pygame.mixer.music.set_volume(current_volume)
            if plus_btn_rect.collidepoint(mouse_pos):
                current_volume = min(1.0, current_volume + 0.1)
                pygame.mixer.music.set_volume(current_volume)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not game_over:
                game_pause = not game_pause
                fish_sound.set_volume(0.3)
            if event.key == pygame.K_ESCAPE and game_pause:
                fish_sound.set_volume(0)
            if event.key == pygame.K_SPACE and not game_over:
                fish_velocity = JUMP_STRENGTH
                fish_sound.play()
            if event.key == pygame.K_SPACE and game_over:
                fish_y = 300
                bullet_x = fish_x

                t1_x = WIDTH
                t1_y = random.randint(100,500)
                t1_type = random.randint(1,3)

                t2_x = WIDTH +200
                t2_y = random.randint(100,500)
                t2_type = random.randint(1,3)

                t3_x = WIDTH + 400
                t3_y = random.randint(100,500)
                t3_type = random.randint(1,3)

                fish_velocity = 0
                score = 0
                pygame.mixer.music.play()
                game_over_sound.stop()
                game_over = False

    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as f:
            f.write(str(high_score))

    bg_x1 -= scroll_speed
    bg_x2 -= scroll_speed

    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= - WIDTH:
        bg_x2 = WIDTH

    fish_rect = pygame.Rect(fish_x, fish_y, 30, 30)

    bullet_rect = pygame.Rect(bullet_x, bullet_y, 10, 10)

    t1_rect = pygame.Rect(t1_x - 25, t1_y - 25, 50, 50)
    t2_rect = pygame.Rect(t2_x - 25, t2_y - 25, 50 ,50)
    t3_rect = pygame.Rect(t3_x - 25, t3_y - 25, 50 ,50)

    if game_started and not game_over and not game_pause:
        bullet_x += bullet_speed
        if bullet_x > WIDTH:
            bullet_x = fish_x
            bullet_y = fish_y

        fish_velocity += GRAVITY
        fish_y += fish_velocity

        t1_x -= trash_speed
        t2_x -= trash_speed
        t3_x -= trash_speed

        if t1_x < -trash_radius:
            t1_x = WIDTH
            t1_y = random.randint(100, 500)
            t1_type = random.randint(1, 3)
        if t2_x < -trash_radius:
            t2_x = WIDTH
            t2_y = random.randint(100, 500)
            t2_type = random.randint(1, 3)
        if t3_x < -trash_radius:
            t3_x = WIDTH
            t3_y = random.randint(100, 500)
            t3_type = random.randint(1, 3)

        if bullet_rect.colliderect(t1_rect):
            score += 1
            score_sound.play()
            t1_x = WIDTH
            t1_y = random.randint(100, 500)
            t1_type = random.randint(1,3)
            bullet_x = fish_x

        if bullet_rect.colliderect(t2_rect):
            score += 1
            score_sound.play()
            t2_x = WIDTH
            t2_y = random.randint(100, 500)
            t2_type = random.randint(1,3)
            bullet_x = fish_x

        if bullet_rect.colliderect(t3_rect):
            score += 1
            score_sound.play()
            t3_x = WIDTH
            t3_y = random.randint(100, 500)
            t3_type = random.randint(1,3)
            bullet_x = fish_x

        if fish_rect.colliderect(t1_rect) or fish_rect.colliderect(t2_rect) or fish_rect.colliderect(t3_rect) or fish_y >= HEIGHT or fish_y <= 0:
            game_over = True
            game_over_sound.play()
            pygame.mixer.music.stop()

    screen.fill(BLACK)

    screen.blit(ocean_img, (bg_x1, 0))
    screen.blit(ocean_img, (bg_x2, 0))

    screen.blit(flabby_img, (fish_x, fish_y ))

    if t1_type == 1:
        screen.blit(bottle_img, (t1_x -25, t1_y -25))
    elif t1_type == 2:
        screen.blit(glass_img, (t1_x -25, t1_y -25))
    else:
        screen.blit(pb_img, (t1_x - 25, t1_y - 25))

    if t2_type == 1:
        screen.blit(tb_img, (t2_x -25, t2_y -25))
    elif t2_type == 2:
        screen.blit(straw_img, (t2_x -25, t2_y -25))
    else:
        screen.blit(mc_img, (t2_x - 25, t2_y -25))

    if t3_type == 1:
        screen.blit(mc2_img, (t3_x -25, t3_y -25))
    elif t3_type == 2:
        screen.blit(fb_img, (t3_x - 25, t3_y -25))
    else:
        screen.blit(apple_img, (t3_x - 25, t3_y -25))

    screen.blit(bubble_img, (bullet_x, bullet_y))

    if not game_started:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        title = ng_font.render("FLABBY FISH", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 180))
        screen.blit(title, title_rect)

        pygame.draw.rect(screen, WHITE, play_btn_rect)
        play_text = vol_font.render("PLAY", True, BLACK)
        play_text_rect = play_text.get_rect(center=play_btn_rect.center)
        screen.blit(play_text, play_text_rect)

        pygame.draw.rect(screen, WHITE, quit_btn_rect)
        quit_text = vol_font.render("QUIT", True, BLACK)
        quit_text_rect = quit_text.get_rect(center=quit_btn_rect.center)
        screen.blit(quit_text, quit_text_rect)

    if game_pause:
        screen.blit(pause_img, (menu_x, menu_y))

        screen.blit(minus_img, (minus_btn_rect.x, minus_btn_rect.y))

        volume_percent = int(current_volume * 100)

        vol_text = vol_font.render(f"VOL  {volume_percent}", True, WHITE)
        stroke_vol_text = vol_font.render(f"VOL  {volume_percent}", True, BLACK)

        vol_text_rect = vol_text.get_rect(center=(WIDTH // 2, menu_y + 160))
        stroke_vol_text_rect = stroke_vol_text.get_rect(center=(WIDTH // 2 + 2, menu_y + 160 + 2))

        screen.blit(stroke_vol_text, stroke_vol_text_rect)
        screen.blit(vol_text, vol_text_rect)

        screen.blit(plus_img, (plus_btn_rect.x, plus_btn_rect.y))

    if game_over:
        center_x, center_y = screen.get_rect().center

        screen.blit(go_img, (menu_x, menu_y))

        sg_over_surface = fonts.render("Game Over", True, BLACK)
        sg_over_rect = sg_over_surface.get_rect(center=(center_x + 2, center_y - 178))
        screen.blit(sg_over_surface, sg_over_rect)

        over_surface = fonts.render("Game Over", True, WHITE)
        over_rect = over_surface.get_rect(center=(center_x, center_y - 180))
        screen.blit(over_surface, over_rect)

        lbl_score = fonts.render(f"Score:  {score}", True, WHITE)
        lbl_score_stroke = fonts.render(f"Score:  {score}", True, BLACK)

        new_w_score = int(lbl_score.get_width() * 0.5)
        new_h_score = int(lbl_score.get_height() * 0.5)

        lbl_score_resized = pygame.transform.scale(lbl_score, (new_w_score, new_h_score))
        lbl_score_stroke_resized = pygame.transform.scale(lbl_score_stroke, (new_w_score, new_h_score))

        score_center_y = menu_y + 100
        screen.blit(lbl_score_stroke_resized,
                    lbl_score_stroke_resized.get_rect(center=(center_x + 2, score_center_y + 2)))
        screen.blit(lbl_score_resized, lbl_score_resized.get_rect(center=(center_x, score_center_y)))

        lbl_best = fonts.render(f"High score:  {high_score}", True, WHITE)
        lbl_best_stroke = fonts.render(f"High score:  {high_score}", True, BLACK)

        new_w_best = int(lbl_best.get_width() * 0.5)
        new_h_best = int(lbl_best.get_height() * 0.5)

        lbl_best_resized = pygame.transform.scale(lbl_best, (new_w_best, new_h_best))
        lbl_best_stroke_resized = pygame.transform.scale(lbl_best_stroke, (new_w_best, new_h_best))

        best_center_y = menu_y + 160
        screen.blit(lbl_best_stroke_resized, lbl_best_stroke_resized.get_rect(center=(center_x + 2, best_center_y + 2)))
        screen.blit(lbl_best_resized, lbl_best_resized.get_rect(center=(center_x, best_center_y)))

    if game_started and not game_over and not game_pause:
        pos_x, pos_y = WIDTH / 2, HEIGHT / 4
        stroke_surface = fonts.render(str(score), True, BLACK)
        stroke_rect = stroke_surface.get_rect(center=(pos_x + 2, pos_y + 2))
        screen.blit(stroke_surface, stroke_rect)

        score_surface = fonts.render(str(score), True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(score_surface, score_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()