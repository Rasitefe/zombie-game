import pygame
import sys
import random
import math
import os
import json

# Oyun için sabitler
WIDTH, HEIGHT = 1200, 800  # Ekranı büyüttüm
PLAYER_SPEED = 5
ZOMBIE_SPEED = 2
ZOMBIE_CHASE_SPEED = 4
ZOMBIE_COUNT = 3
ZOMBIE_SPACING = 50
BULLET_SPEED = 10
BULLET_DAMAGE = 1
RESPAWN_DELAY = 2000
AUTO_FIRE_DELAY = 100
ROOM_SIZE = 400  # Oda boyutunu büyüttüm
WALL_THICKNESS = 20
DOOR_SIZE = 100  # Kapı boyutunu büyüttüm
DOOR_OPEN_DISTANCE = 100  # Kapıyı açmak için gereken mesafe
GRID_ROWS = 2
GRID_COLS = 2

EMPTY = 0
WALL = 1
DOOR = 2
ZOMBIE = 3
START = 4
END = 5

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)

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
        # Oda içi
        pygame.draw.rect(screen, BLACK, (
            self.rect.x + WALL_THICKNESS,
            self.rect.y + WALL_THICKNESS,
            self.rect.width - 2 * WALL_THICKNESS,
            self.rect.height - 2 * WALL_THICKNESS
        ))
        # Kapılar
        for door in self.doors:
            door.draw(screen)

class Door:
    def __init__(self, x, y, width, height, is_horizontal):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_horizontal = is_horizontal
        self.connected_rooms = []
        self.is_open = False
        self.open_progress = 0  # 0: kapalı, 1: açık
        self.open_speed = 0.1  # Kapı açılma hızı

    def update(self, player):
        # Oyuncu kapıya yakınsa aç
        dx = player.x - self.rect.centerx
        dy = player.y - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        target_open = distance < DOOR_OPEN_DISTANCE
        
        # Kapıyı yavaşça aç/kapat
        if target_open and self.open_progress < 1:
            self.open_progress = min(1, self.open_progress + self.open_speed)
        elif not target_open and self.open_progress > 0:
            self.open_progress = max(0, self.open_progress - self.open_speed)
        
        self.is_open = self.open_progress > 0.5

    def draw(self, screen):
        if self.is_horizontal:
            # Yatay kapı
            door_width = int(self.rect.width * (1 - self.open_progress))
            if door_width > 0:
                pygame.draw.rect(screen, DARK_BROWN, 
                               (self.rect.x, self.rect.y, door_width, self.rect.height))
        else:
            # Dikey kapı
            door_height = int(self.rect.height * (1 - self.open_progress))
            if door_height > 0:
                pygame.draw.rect(screen, DARK_BROWN,
                               (self.rect.x, self.rect.y, self.rect.width, door_height))

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
        
        # Duvarlarla çarpışma kontrolü
        for wall in walls:
            if wall.collidepoint(new_x, new_y):
                self.active = False
                return
        
        self.x = new_x
        self.y = new_y
        
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

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
        
        # Oyuncu sprite'ı
        self.sprite = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.sprite, BLUE, (20, 20), 20)
        pygame.draw.circle(self.sprite, WHITE, (30, 15), 5)
        pygame.draw.circle(self.sprite, WHITE, (30, 25), 5)
        pygame.draw.circle(self.sprite, BLACK, (32, 15), 2)
        pygame.draw.circle(self.sprite, BLACK, (32, 25), 2)

        # Tüfek sprite'ı
        self.gun_sprite = pygame.Surface((40, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.gun_sprite, (100, 100, 100), (0, 0, 35, 10))
        pygame.draw.rect(self.gun_sprite, (80, 80, 80), (35, 2, 5, 6))
        pygame.draw.rect(self.gun_sprite, (120, 80, 40), (0, 0, 10, 10))

    def move(self, dx, dy, walls, doors=None):
        new_x = self.x + dx
        new_y = self.y + dy
        # Sadece duvarlarda çarpışma kontrolü
        for wall in walls:
            if wall.collidepoint(new_x, new_y):
                return
        self.x = new_x
        self.y = new_y
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"

    def update_angle(self, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.atan2(dy, dx)

    def shoot(self):
        muzzle_x = self.x + math.cos(self.angle) * 30
        muzzle_y = self.y + math.sin(self.angle) * 30
        return Bullet(muzzle_x, muzzle_y, self.angle)

    def draw(self, screen):
        if self.direction == "left":
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)
            screen.blit(flipped_sprite, (int(self.x - 20), int(self.y - 20)))
        else:
            screen.blit(self.sprite, (int(self.x - 20), int(self.y - 20)))
        
        gun_rotated = pygame.transform.rotate(self.gun_sprite, -math.degrees(self.angle))
        gun_rect = gun_rotated.get_rect(center=(self.x, self.y))
        screen.blit(gun_rotated, gun_rect)

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
        self.current_room = None
        
        # Zombi sprite'ı
        self.sprite = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.sprite, RED, (15, 15), 15)
        pygame.draw.circle(self.sprite, WHITE, (20, 10), 4)
        pygame.draw.circle(self.sprite, WHITE, (20, 20), 4)
        pygame.draw.circle(self.sprite, BLACK, (22, 10), 2)
        pygame.draw.circle(self.sprite, BLACK, (22, 20), 2)

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
            
        # Oyuncu ile zombi arasındaki mesafe
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Eğer oyuncu aynı odadaysa ve duvarlar arasında engel yoksa
        if self.current_room == player.current_room and distance < 300:
            # Duvarlarla çarpışma kontrolü
            for wall in walls:
                if wall.collidepoint(self.x + dx/2, self.y + dy/2):
                    return False
            return True
        return False

    def move_towards_player(self, player, walls, doors):
        if not self.alive:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        # Oyuncunun içine girmesin
        if dist < self.radius + player.radius:
            return
        if dist != 0:
            dx = dx / dist
            dy = dy / dist
        speed = ZOMBIE_CHASE_SPEED * self.speed_variation
        new_x = self.x + dx * speed
        new_y = self.y + dy * speed
        # Duvar ve kapı çarpışması (kapıdan geçemez)
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

    def draw(self, screen):
        if not self.alive:
            return
            
        if self.direction == "left":
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)
            screen.blit(flipped_sprite, (int(self.x - 15), int(self.y - 15)))
        else:
            screen.blit(self.sprite, (int(self.x - 15), int(self.y - 15)))

# --- Haritayı yükle ---
def load_map(filename):
    with open(filename, 'r') as f:
        grid = json.load(f)
    return grid

# --- Grid tabanlı duvar ve kapı çizimi ---
def get_walls_and_doors_from_grid(grid, cell_size):
    walls = []
    doors = []
    grid_size = len(grid)
    for y in range(grid_size):
        for x in range(grid_size):
            cell = grid[y][x]
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if cell == WALL:
                walls.append(rect)
            elif cell == DOOR:
                doors.append(rect)
    return walls, doors

# --- Zombi, başlangıç ve bitiş noktalarını bul ---
def get_entities_from_grid(grid, cell_size):
    zombies = []
    start = None
    end = None
    grid_size = len(grid)
    for y in range(grid_size):
        for x in range(grid_size):
            cell = grid[y][x]
            cx = x * cell_size + cell_size // 2
            cy = y * cell_size + cell_size // 2
            if cell == ZOMBIE:
                zombies.append((cx, cy))
            elif cell == START:
                start = (cx, cy)
            elif cell == END:
                end = (cx, cy)
    return zombies, start, end

def is_in_open_door(x, y, doors):
    for door in doors:
        if door.is_open and door.rect.collidepoint(x, y):
            return True
    return False

# --- Fener/ışık konisi için parametreler ---
FOV_RADIUS = 100
FOV_ANGLE = 60  # Derece
ZOMBIE_REVEAL_RADIUS = 40  # Fener dışında bile bu mesafede zombi görünür

def main():
    pygame.init()
    grid = load_map('map.json')
    grid_size = len(grid)
    # Ekran boyutunu al
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    cell_size = min(screen_w, screen_h) // grid_size
    screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size))
    pygame.display.set_caption('Harita Tabanlı Zombi Oyunu')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    walls, doors = get_walls_and_doors_from_grid(grid, cell_size)
    zombie_positions, start_pos, end_pos = get_entities_from_grid(grid, cell_size)

    if not start_pos or not end_pos:
        print('HATA: Haritada başlangıç veya bitiş noktası yok!')
        pygame.quit()
        return

    player = Player(*start_pos)
    zombies = [Zombie(x, y) for (x, y) in zombie_positions]
    end_rect = pygame.Rect(end_pos[0] - cell_size//2, end_pos[1] - cell_size//2, cell_size, cell_size)

    bullets = []
    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.is_auto_firing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    player.is_auto_firing = False

        mouse_pos = pygame.mouse.get_pos()
        player.update_angle(mouse_pos)

        # WASD kontrolleri
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED
        player.move(dx, dy, walls, doors)

        # Taramalı ateş
        current_time = pygame.time.get_ticks()
        if player.is_auto_firing and hasattr(player, 'last_auto_fire_time'):
            if current_time - getattr(player, 'last_auto_fire_time', 0) > AUTO_FIRE_DELAY:
                bullets.append(player.shoot())
                player.last_auto_fire_time = current_time
        elif not hasattr(player, 'last_auto_fire_time'):
            player.last_auto_fire_time = 0

        # Mermileri hareket ettir
        for bullet in bullets[:]:
            bullet.move(walls)
            if not bullet.active:
                bullets.remove(bullet)
                continue
            for zombie in zombies:
                if zombie.alive:
                    dx = bullet.x - zombie.x
                    dy = bullet.y - zombie.y
                    if math.sqrt(dx*dx + dy*dy) < zombie.radius:
                        if zombie.take_damage():
                            player.score += 100
                        bullet.active = False
                        break

        # Zombileri hareket ettir
        for zombie in zombies:
            zombie.move_towards_player(player, walls, doors)

        # Kazanma kontrolü
        if end_rect.collidepoint(player.x, player.y):
            win = True
            running = False

        # Ekranı çiz
        screen.fill((0,0,0))
        # Harita her zaman açık
        for y in range(grid_size):
            for x in range(grid_size):
                cell = grid[y][x]
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if cell == WALL:
                    pygame.draw.rect(screen, (80,80,80), rect)
                elif cell == DOOR:
                    pygame.draw.rect(screen, (160,82,45), rect)
                elif cell == END:
                    pygame.draw.rect(screen, (0, 200, 0), rect)
        # Sadece görüş konisinde olan mermiler çizilsin
        for bullet in bullets:
            dx = bullet.x - player.x
            dy = bullet.y - player.y
            dist = math.sqrt(dx*dx + dy*dy)
            angle = math.degrees(math.atan2(dy, dx))
            player_angle = math.degrees(player.angle)
            diff = (angle - player_angle + 360) % 360
            if diff > 180:
                diff = 360 - diff
            if dist <= FOV_RADIUS and diff < FOV_ANGLE/2:
                bullet.draw(screen)
        # Zombiler: fener konisinde veya çok yakınsa görünür
        for zombie in zombies:
            dx = zombie.x - player.x
            dy = zombie.y - player.y
            dist = math.sqrt(dx*dx + dy*dy)
            angle = math.degrees(math.atan2(dy, dx))
            player_angle = math.degrees(player.angle)
            diff = (angle - player_angle + 360) % 360
            if diff > 180:
                diff = 360 - diff
            if (dist <= FOV_RADIUS and diff < FOV_ANGLE/2) or dist < ZOMBIE_REVEAL_RADIUS:
                zombie.draw(screen)
        player.draw(screen)
        # Fener konisini belirgin göstermek için yarı saydam aydınlık alan çiz
        s = pygame.Surface((grid_size*cell_size, grid_size*cell_size), pygame.SRCALPHA)
        pygame.draw.polygon(
            s, (255,255,180,60),
            [
                (player.x, player.y),
                (
                    player.x + FOV_RADIUS * math.cos(player.angle - math.radians(FOV_ANGLE/2)),
                    player.y + FOV_RADIUS * math.sin(player.angle - math.radians(FOV_ANGLE/2))
                ),
                (
                    player.x + FOV_RADIUS * math.cos(player.angle + math.radians(FOV_ANGLE/2)),
                    player.y + FOV_RADIUS * math.sin(player.angle + math.radians(FOV_ANGLE/2))
                )
            ]
        )
        screen.blit(s, (0,0))
        score_text = font.render(f'Skor: {player.score}', True, (255,255,255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    if win:
        screen.fill((0,0,0))
        win_text = font.render('Kazandınız! Tebrikler!', True, (0, 255, 0))
        screen.blit(win_text, (grid_size * cell_size // 2 - 150, grid_size * cell_size // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(3000)
    pygame.quit()

if __name__ == '__main__':
    main() 