import math
import pygame
from utils.constants import PLAYER_MAX_HEALTH, BLUE, WHITE, BLACK, WIDTH, HEIGHT
from classes.bullet import Bullet


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.direction = "right"
        self.animation_frame = 0
        self.score = 0
        self.angle = 0
        self.is_auto_firing = False
        self.last_auto_fire_time = 0
        self.current_room = None
        self.health = PLAYER_MAX_HEALTH
        self.last_damage_time = 0

        self.sprite = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.sprite, BLUE, (20, 20), 20)
        pygame.draw.circle(self.sprite, WHITE, (30, 15), 5)
        pygame.draw.circle(self.sprite, WHITE, (30, 25), 5)
        pygame.draw.circle(self.sprite, BLACK, (32, 15), 2)
        pygame.draw.circle(self.sprite, BLACK, (32, 25), 2)

        original_gun = pygame.image.load("assets/PNG/Gun/gun.png").convert()
        original_gun = pygame.transform.scale(original_gun, (60, 20))

        original_gun = original_gun.convert_alpha()
        width, height = original_gun.get_size()
        for x in range(width):
            for y in range(height):
                r, g, b, _ = original_gun.get_at((x, y))
                if r > 240 and g > 240 and b > 240:  # beyaza yakın her tonu sil
                    original_gun.set_at((x, y), (0, 0, 0, 0))  # tam şeffaf

        self.gun_sprite = original_gun

        self.images = [
            pygame.image.load("assets/PNG/Player/Poses/player_walk1.png").convert_alpha(),
            pygame.image.load("assets/PNG/Player/Poses/player_walk2.png").convert_alpha()
        ]
        self.image_index = 0
        self.animation_timer = 0
        self.ANIMATION_SPEED = 200  # ms

    def move(self, dx, dy, walls, doors=None):
        new_x = self.x + dx
        new_y = self.y + dy
        for wall in walls:
            if wall.collidepoint(new_x, new_y):
                return
        self.x = new_x
        self.y = new_y

        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"

        if dx != 0 or dy != 0:
            now = pygame.time.get_ticks()
            if now - self.animation_timer > self.ANIMATION_SPEED:
                self.image_index = (self.image_index + 1) % len(self.images)
                self.animation_timer = now
        else:
            self.image_index = 0

    def update_angle(self, mouse_pos):
        dx = mouse_pos[0] - WIDTH // 2
        dy = mouse_pos[1] - HEIGHT // 2
        self.angle = math.atan2(dy, dx)

    def shoot(self):
        muzzle_x = self.x + math.cos(self.angle) * 30
        muzzle_y = self.y + math.sin(self.angle) * 30
        return Bullet(muzzle_x, muzzle_y, self.angle)

    def draw(self, screen, camera_x, camera_y):
        current_image = self.images[self.image_index]
        if self.direction == "left":
            current_image = pygame.transform.flip(current_image, True, False)
        screen.blit(
            current_image,
            (int(self.x - current_image.get_width() // 2 - camera_x),
             int(self.y - current_image.get_height() // 2 - camera_y))
        )
        gun_offset_y = 30
        gun_rotated = pygame.transform.rotate(self.gun_sprite, -math.degrees(self.angle))
        gun_rect = gun_rotated.get_rect(center=(self.x - camera_x, self.y - camera_y + gun_offset_y))
        screen.blit(gun_rotated, gun_rect)
