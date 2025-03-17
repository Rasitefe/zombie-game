import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Zombie Attack")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()
FPS = 60

camera_x, camera_y = 0, 0

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 5
        self.size = 40

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x - camera_x, self.y - camera_y, self.size, self.size))

class Zombie:
    def __init__(self):
        self.x = random.choice([0, WIDTH])
        self.y = random.choice([0, HEIGHT])
        self.speed = 2
        self.size = 30

    def move_towards_player(self, player):
        dx, dy = player.x - self.x, player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x - camera_x, self.y - camera_y, self.size, self.size))

player = Player()
zombies = [Zombie() for _ in range(5)]

running = True
while running:
    screen.fill((0, 0, 0)) 
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2
    
    player.move(keys)
    player.draw()
    
    for zombie in zombies:
        zombie.move_towards_player(player)
        zombie.draw()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()