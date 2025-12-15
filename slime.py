import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("JR's Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

# IMAGES
try:
    bg_img = pygame.image.load("bg1.png").convert()
    bg_img = pygame.transform.scale(bg_img, (1000, 700))
    player_img = pygame.image.load("pl1.png").convert_alpha()
    bullet_img = pygame.image.load("venom.png").convert_alpha()
    cloud_img = pygame.image.load("c1.png").convert_alpha()

except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

# SCALE IMAGES
SCALE = 0.5
player_img = pygame.transform.scale(
    player_img,
    (int(player_img.get_width() * SCALE), int(player_img.get_height() * SCALE))
)

bullet_img = pygame.transform.scale(
    bullet_img,
    (player_img.get_width(), player_img.get_height())
)

cloud_img = pygame.transform.scale(cloud_img, (300, 150))  # Scale cloud image

# PLAYER VARIABLES
player_x = 1000 // 2 - player_img.get_width() // 2
ground_y = 700 - player_img.get_height() - 100
player_y = ground_y

speed = 5
velocity_y = 0
gravity = 0.8
jump_power = -13
on_ground = True

# BULLET/VENOM VARIABLES
bullets = []
bullet_speed = 10
can_shoot = True
shoot_cooldown = 0
shoot_delay = 15
player_direction = 1  # 1 = right, -1 = left

# CLOUD VARIABLES
clouds = [
    {"x": 1000, "y": 80,  "speed": 1},
    {"x": 1300, "y": 150, "speed": 0.9},
    {"x": 1600, "y": 20,  "speed": 1.2},
]

# LOOP
running = True
while running:
    clock.tick(60)

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # JUMP
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_power
                on_ground = False

            # SHOOT
            if event.key == pygame.K_f and can_shoot:
                if player_direction == 1:
                    bullet_x = player_x + player_img.get_width() - 230
                else:
                    bullet_x = player_x - player_img.get_width() + 230

                bullet_y = player_y + player_img.get_height() // 2 - bullet_img.get_height() // 2

                bullet = {
                    'x': bullet_x,
                    'y': bullet_y,
                    'direction': player_direction
                }
                bullets.append(bullet)
                can_shoot = False
                shoot_cooldown = shoot_delay


    # KEYS FOR MOVEMENTS
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_x -= speed
        player_direction = -1
    if keys[pygame.K_d]:
        player_x += speed
        player_direction = 1
    if keys[pygame.K_w] and not on_ground:
        player_y -= speed
    if keys[pygame.K_s]:
        player_y += speed


    # GRAVITY
    velocity_y += gravity
    player_y += velocity_y

    if player_y >= ground_y:
        player_y = ground_y
        velocity_y = 0
        on_ground = True

    #============= LIMIT MOVEMENT ===============
        bounding = player_img.get_bounding_rect()
        trim_left = bounding.x
        visible_w = bounding.width
        player_x = max(-trim_left, min(player_x, 1000 - visible_w - trim_left))

    #================= SHOOT COOLDOWN ==================
    if not can_shoot:
        shoot_cooldown -= 1
        if shoot_cooldown <= 0:
            can_shoot = True

    # ================= UPDATE BULLETS =================
    for bullet in bullets[:]:
        bullet['x'] += bullet_speed * bullet['direction']
        if bullet['x'] < -bullet_img.get_width() or bullet['x'] > 1000 + bullet_img.get_width():
            bullets.remove(bullet)

        # ================= UPDATE CLOUD =================
    for cloud in clouds:
        cloud["x"] -= cloud["speed"]
        if cloud["x"] < -cloud_img.get_width():
            cloud["x"] = 1000

    screen.fill(WHITE)
    screen.blit(bg_img, (0, 0))
    screen.blit(player_img, (player_x, player_y))

    for cloud in clouds:
        screen.blit(cloud_img, (cloud["x"], cloud["y"]))

    for bullet in bullets:
        screen.blit(bullet_img, (bullet['x'], bullet['y']))

    pygame.display.update()


pygame.quit()
sys.exit()