import math
import pygame
from utils.constants import BULLET_SPEED, YELLOW


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.radius = 3
        self.active = True

    def move(self, walls):
        new_x = self.x + math.cos(self.angle) * self.speed
        new_y = self.y + math.sin(self.angle) * self.speed

        for wall in walls:
            if wall.collidepoint(new_x, new_y):
                self.active = False
                return

        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
