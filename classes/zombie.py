import math
import pygame
import random
from scripts.resource_path import resource_path
from utils.constants import (
    RED, WHITE, BLACK, BULLET_DAMAGE, WALL_THICKNESS, ZOMBIE_CHASE_SPEED
)



class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.direction = "right"
        self.speed_variation = random.uniform(0.8, 1.2)
        self.health = 2
        self.alive = True
        self.death_time = 0
        self.can_see_player = False

        self.sprite = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.sprite, RED, (15, 15), 15)
        pygame.draw.circle(self.sprite, WHITE, (20, 10), 4)
        pygame.draw.circle(self.sprite, WHITE, (20, 20), 4)
        pygame.draw.circle(self.sprite, BLACK, (22, 10), 2)
        pygame.draw.circle(self.sprite, BLACK, (22, 20), 2)

        self.images = [
            pygame.image.load(resource_path("assets/PNG/Zombie/Poses/zombie_walk1.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/PNG/Zombie/Poses/zombie_walk2.png")).convert_alpha()
        ]
        self.image_index = 0
        self.animation_timer = 0
        self.ANIMATION_SPEED = 300  # ms

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.ANIMATION_SPEED:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.animation_timer = now

    def take_damage(self):
        self.health -= BULLET_DAMAGE
        if self.health <= 0:
            self.alive = False
            self.death_time = pygame.time.get_ticks()
            return True
        return False

    def respawn(self, room):
        self.x = random.randint(room.rect.x + WALL_THICKNESS + self.radius,
                                room.rect.right - WALL_THICKNESS - self.radius)
        self.y = random.randint(room.rect.y + WALL_THICKNESS + self.radius,
                                room.rect.bottom - WALL_THICKNESS - self.radius)
        self.health = 2
        self.alive = True
        self.current_room = room

    def check_player_visibility(self, player, walls):
        if not self.alive or not self.current_room:
            return False

        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if self.current_room == player.current_room and distance < 300:
            for wall in walls:
                if wall.collidepoint(self.x + dx / 2, self.y + dy / 2):
                    return False
            return True
        return False

    def move_towards_player(self, player, walls, doors):
        if not self.alive:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < self.radius + player.radius:
            return
        if dist != 0:
            dx = dx / dist
            dy = dy / dist
        speed = ZOMBIE_CHASE_SPEED * self.speed_variation
        new_x = self.x + dx * speed
        new_y = self.y + dy * speed
        can_move = True
        for wall in walls:
            if wall.collidepoint(new_x, new_y):
                can_move = False
                break
        for door in doors:
            if door.collidepoint(new_x, new_y):
                can_move = False
                break
        if can_move:
            self.x = new_x
            self.y = new_y
        if dx > 0:
            self.direction = "right"
        else:
            self.direction = "left"

    def draw(self, screen, camera_x, camera_y):
        if not self.alive:
            return
        current_image = self.images[self.image_index]
        if self.direction == "left":
            current_image = pygame.transform.flip(current_image, True, False)
        screen.blit(current_image, (int(self.x - current_image.get_width() // 2 - camera_x),
                                    int(self.y - current_image.get_height() // 2 - camera_y)))
