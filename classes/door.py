import math
import pygame
from utils.constants import DOOR_OPEN_DISTANCE, DARK_BROWN


class Door:
    def __init__(self, x, y, width, height, is_horizontal):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_horizontal = is_horizontal
        self.connected_rooms = []
        self.is_open = False
        self.open_progress = 0  # 0: kapalı, 1: açık
        self.open_speed = 0.1  # Kapı açılma hızı

    def update(self, player):
        dx = player.x - self.rect.centerx
        dy = player.y - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        target_open = distance < DOOR_OPEN_DISTANCE

        if target_open and self.open_progress < 1:
            self.open_progress = min(1, self.open_progress + self.open_speed)
        elif not target_open and self.open_progress > 0:
            self.open_progress = max(0, self.open_progress - self.open_speed)

        self.is_open = self.open_progress > 0.5

    def draw(self, screen):
        if self.is_horizontal:
            door_width = int(self.rect.width * (1 - self.open_progress))
            if door_width > 0:
                pygame.draw.rect(screen, DARK_BROWN,
                                 (self.rect.x, self.rect.y, door_width, self.rect.height))
        else:
            door_height = int(self.rect.height * (1 - self.open_progress))
            if door_height > 0:
                pygame.draw.rect(screen, DARK_BROWN,
                                 (self.rect.x, self.rect.y, self.rect.width, door_height))

