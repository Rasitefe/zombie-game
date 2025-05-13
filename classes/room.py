import pygame
from utils.constants import ROOM_SIZE, WALL_THICKNESS, BLACK


class Room:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(
            100 + grid_x * ROOM_SIZE,
            100 + grid_y * ROOM_SIZE,
            ROOM_SIZE,
            ROOM_SIZE
        )
        self.doors = []
        self.zombies = []
        self.visited = False

    def add_door(self, door):
        self.doors.append(door)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (
            self.rect.x + WALL_THICKNESS,
            self.rect.y + WALL_THICKNESS,
            self.rect.width - 2 * WALL_THICKNESS,
            self.rect.height - 2 * WALL_THICKNESS
        ))
        for door in self.doors:
            door.draw(screen)
