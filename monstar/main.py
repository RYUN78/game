import pygame
import math

pygame.init()

# ------------------
# 設定
# ------------------
WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DREADLORD HUNTER")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
GRAY = (60, 60, 60)
YELLOW = (255, 220, 0)

font = pygame.font.SysFont(None, 36)

# ------------------
# プレイヤー
# ------------------
player_x = WIDTH // 2
player_y = HEIGHT - 150

player_speed = 5
player_size = 25
player_hp = 100

attack_range = 100
attack_damage = 10

rolling = False
roll_timer = 0

# ------------------
# ボス
# ------------------
boss_x = WIDTH // 2
boss_y = 180

boss_size = 80
boss_hp = 500
boss_max_hp = 500

boss_speed = 2

attack_cooldown = 0

running = True

while running:

    dt = clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                rolling = True
                roll_timer = 15

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                distance = math.sqrt(
                    (boss_x - player_x) ** 2 +
                    (boss_y - player_y) ** 2
                )

                if distance < attack_range:
                    boss_hp -= attack_damage

    keys = pygame.key.get_pressed()

    speed = player_speed

    if rolling:
        speed = 12
        roll_timer -= 1

        if roll_timer <= 0:
            rolling = False

    if keys[pygame.K_w]:
        player_y -= speed

    if keys[pygame.K_s]:
        player_y += speed

    if keys[pygame.K_a]:
        player_x -= speed

    if keys[pygame.K_d]:
        player_x += speed

    player_x = max(0, min(WIDTH, player_x))
    player_y = max(0, min(HEIGHT, player_y))

    # ------------------
    # ボスAI
    # ------------------

    dx = player_x - boss_x
    dy = player_y - boss_y

    distance = math.sqrt(dx * dx + dy * dy)

    if distance > 5:

        boss_x += dx / distance * boss_speed
        boss_y += dy / distance * boss_speed

    attack_cooldown += 1

    if distance < 100 and attack_cooldown > 60:
        player_hp -= 5
        attack_cooldown = 0

    # ------------------
    # 描画
    # ------------------

    screen.fill((30, 30, 40))

    # 地面
    pygame.draw.rect(screen, (70, 90, 70),
                     (0, HEIGHT - 100, WIDTH, 100))

    # プレイヤー
    pygame.draw.circle(
        screen,
        GREEN,
        (int(player_x), int(player_y)),
        player_size
    )

    # ボス
    pygame.draw.circle(
        screen,
        RED,
        (int(boss_x), int(boss_y)),
        boss_size
    )

    # 攻撃範囲
    pygame.draw.circle(
        screen,
        (100, 100, 100),
        (int(player_x), int(player_y)),
        attack_range,
        1
    )

    # プレイヤーHP
    pygame.draw.rect(screen, GRAY, (20, 20, 300, 30))
    pygame.draw.rect(screen, GREEN,
                     (20, 20, max(0, player_hp * 3), 30))

    # ボスHP
    pygame.draw.rect(screen, GRAY,
                     (340, 20, 600, 30))

    boss_bar = int((boss_hp / boss_max_hp) * 600)

    pygame.draw.rect(
        screen,
        RED,
        (340, 20, max(0, boss_bar), 30)
    )

    title = font.render(
        "DREADLORD",
        True,
        WHITE
    )

    screen.blit(title, (580, 55))

    # 勝利
    if boss_hp <= 0:

        text = font.render(
            "QUEST CLEAR",
            True,
            YELLOW
        )

        screen.blit(text, (520, 300))

    # 敗北
    if player_hp <= 0:

        text = font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(text, (540, 300))

    pygame.display.flip()

pygame.quit()