import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("player-cam")

clock = pygame.time.Clock()
FPS = 60

player_images = [
    pygame.image.load("../assets/PNG/Player/Poses/player_walk1.png").convert_alpha(),
    pygame.image.load("../assets/PNG/Player/Poses/player_walk2.png").convert_alpha()
]
player_idle = player_images[0]

player_pos = pygame.Vector2(WIDTH//2, HEIGHT//2)
player_speed = 3
animation_index = 0
animation_timer = 0
animation_speed = 150

running = True
while running:
    dt = clock.tick(FPS)
    screen.fill((30, 30, 30))

    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_w]:
        player_pos.y -= player_speed
        moving = True
    if keys[pygame.K_s]:
        player_pos.y += player_speed
        moving = True
    if keys[pygame.K_a]:
        player_pos.x -= player_speed
        moving = True
    if keys[pygame.K_d]:
        player_pos.x += player_speed
        moving = True

    if moving:
        animation_timer += dt
        if animation_timer >= animation_speed:
            animation_timer = 0
            animation_index = (animation_index + 1) % len(player_images)
        player_image = player_images[animation_index]
    else:
        player_image = player_idle
        animation_index = 0
        animation_timer = 0

    screen.blit(player_image, player_pos)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
