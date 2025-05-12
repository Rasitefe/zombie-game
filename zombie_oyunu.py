import pygame
import sys
import random
import math
import os
import json

WIDTH, HEIGHT = 1200, 800  # Ekranı büyüttüm
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 100
PLAYER_DAMAGE_COOLDOWN = 1000  # ms
FOV_RADIUS = 500
FOV_ANGLE = 45
ZOMBIE_REVEAL_RADIUS = 300
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
DOOR_OPEN_DISTANCE = 100
GRID_ROWS = 2
GRID_COLS = 2

EMPTY = 0
WALL = 1
DOOR = 2
ZOMBIE = 3
START = 4
END = 5

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
        pygame.draw.rect(screen, BLACK, (
            self.rect.x + WALL_THICKNESS,
            self.rect.y + WALL_THICKNESS,
            self.rect.width - 2 * WALL_THICKNESS,
            self.rect.height - 2 * WALL_THICKNESS
        ))
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
            pygame.image.load("assets/PNG/Zombie/Poses/zombie_walk1.png").convert_alpha(),
            pygame.image.load("assets/PNG/Zombie/Poses/zombie_walk2.png").convert_alpha()
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

def load_map(filename):
    with open(filename, 'r') as f:
        grid = json.load(f)
    return grid

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

FOV_RADIUS = 500
FOV_ANGLE = 45  # Derece
ZOMBIE_REVEAL_RADIUS = 150  # Fener dışında bile bu mesafede zombi görünür

def show_menu(screen, font, title, options):
    selected = 0
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        title_text = font.render(title, True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            option_text = font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 250 + i * 50))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected

def main():
    pygame.init()
    current_level = 0
    maps = ['map1.json','map2.json']
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    selected_option = show_menu(screen, font, "Zombi Oyunu", ["Başla", "Çıkış"])
    if selected_option == 1:
            pygame.quit()
            return
    while current_level < len(maps):
        map_file = maps[current_level]
        current_level += 1
        win = False
        game_over = False
        

        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zombi Oyunu')
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)

        

        # Haritayı yükle
        
        grid = load_map(map_file)
        grid_size = len(grid)
        cell_size = 64

        # Grafik yüklemeleri
        wall_image = pygame.image.load(r'assets\PNG\background\wall.jpg')
        wall_image = pygame.transform.scale(wall_image, (cell_size, cell_size))
        floor_image = pygame.image.load(r'assets\PNG\background\floor.jpg')
        floor_image = pygame.transform.scale(floor_image, (cell_size, cell_size))
        door_image = pygame.image.load(r'assets\PNG\background\door.jpg')
        door_image = pygame.transform.scale(door_image, (cell_size, cell_size))

        # Haritadan öğeleri al
        walls, doors = get_walls_and_doors_from_grid(grid, cell_size)
        zombie_positions, start_pos, end_pos = get_entities_from_grid(grid, cell_size)

        if not start_pos or not end_pos:
            print('HATA: Haritada başlangıç veya bitiş noktası yok!')
            pygame.quit()
            return

        player = Player(*start_pos)
        zombies = [Zombie(x, y) for (x, y) in zombie_positions]
        end_rect = pygame.Rect(end_pos[0] - cell_size // 2, end_pos[1] - cell_size // 2, cell_size, cell_size)

        bullets = []
        running = True

        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause = show_menu(screen, font, "Oyun Duraklatıldı", ["Devam Et", "Çıkış"])
                    if pause == 1:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    player.is_auto_firing = True
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    player.is_auto_firing = False

            # Oyuncu hareket
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED
            player.move(dx, dy, walls, doors)
            player.update_angle(pygame.mouse.get_pos())

            # Otomatik ateşleme
            if player.is_auto_firing:
                if current_time - player.last_auto_fire_time > AUTO_FIRE_DELAY:
                    bullets.append(player.shoot())
                    player.last_auto_fire_time = current_time

            # Mermileri güncelle
            for bullet in bullets[:]:
                bullet.move(walls)
                if not bullet.active:
                    bullets.remove(bullet)
                    continue
                for zombie in zombies:
                    if zombie.alive and math.hypot(bullet.x - zombie.x, bullet.y - zombie.y) < zombie.radius:
                        if zombie.take_damage():
                            player.score += 100
                        bullet.active = False
                        break

            # Zombileri güncelle
            for zombie in zombies:
                if not zombie.alive:
                    continue
                dist = math.hypot(zombie.x - player.x, zombie.y - player.y)
                if dist <= FOV_RADIUS:
                    zombie.update()
                    zombie.move_towards_player(player, walls, doors)
                    if dist < zombie.radius + 20:
                        if current_time - player.last_damage_time > PLAYER_DAMAGE_COOLDOWN:
                            player.health -= 0.0002
                            player.last_damage_time = current_time

            if player.health <= 0:
                player.health = 0
                game_over = True
                running = False

            if end_rect.collidepoint(player.x, player.y):
                win = True
                running = False

            # Kamera pozisyonu
            camera_x = player.x - WIDTH // 2
            camera_y = player.y - HEIGHT // 2

            # Çizim
            screen.fill((0, 0, 0))
            for y in range(grid_size):
                for x in range(grid_size):
                    cell = grid[y][x]
                    draw_rect = pygame.Rect(x * cell_size - camera_x, y * cell_size - camera_y, cell_size, cell_size)
                    if cell == WALL:
                        screen.blit(wall_image, draw_rect.topleft)
                    elif cell == DOOR:
                        screen.blit(door_image, draw_rect.topleft)
                    else:
                        if cell != 5:
                            screen.blit(floor_image, draw_rect.topleft)
                        else:
                            pygame.draw.rect(screen, (0, 255, 0), draw_rect) 

            for bullet in bullets:
                pygame.draw.circle(screen, YELLOW, (int(bullet.x - camera_x), int(bullet.y - camera_y)), bullet.radius)

            for zombie in zombies:
                dist = math.hypot(zombie.x - player.x, zombie.y - player.y)
                angle_to_player = math.degrees(math.atan2(zombie.y - player.y, zombie.x - player.x))
                player_angle = math.degrees(player.angle)
                diff = abs((angle_to_player - player_angle + 180) % 360 - 180)
                if (dist <= FOV_RADIUS and diff < FOV_ANGLE / 2) or dist < ZOMBIE_REVEAL_RADIUS:
                    if zombie.alive:
                        zombie.draw(screen, camera_x, camera_y)

            player.draw(screen, camera_x, camera_y)

            # Sağlık barı
            health_ratio = player.health / PLAYER_MAX_HEALTH
            health_color = (0, 255, 0) if health_ratio > 0.5 else (255, 255, 0) if health_ratio > 0.2 else (255, 0, 0)
            pygame.draw.rect(screen, (50, 50, 50), (10, 50, 200, 20))
            pygame.draw.rect(screen, health_color, (10, 50, 200 * health_ratio, 20))

            # Skor
            score_text = font.render(f"Skor: {player.score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # Fener görüş efekti
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(
                s, (255, 255, 180, 60),
                [
                    (WIDTH // 2, HEIGHT // 2),
                    (
                        WIDTH // 2 + FOV_RADIUS * math.cos(player.angle - math.radians(FOV_ANGLE / 2)),
                        HEIGHT // 2 + FOV_RADIUS * math.sin(player.angle - math.radians(FOV_ANGLE / 2))
                    ),
                    (
                        WIDTH // 2 + FOV_RADIUS * math.cos(player.angle + math.radians(FOV_ANGLE / 2)),
                        HEIGHT // 2 + FOV_RADIUS * math.sin(player.angle + math.radians(FOV_ANGLE / 2))
                    )
                ]
            )
            screen.blit(s, (0, 0))

            # Zombi saldırısı efekti
            if current_time - player.last_damage_time < 300:
                red_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 100))
                screen.blit(red_overlay, (0, 0))

            pygame.display.flip()
            clock.tick(60)

        # Son ekran
        screen.fill((0, 0, 0))
        if win:
            end_text = font.render("Kazandınız! Tebrikler!", True, (0, 255, 0))
            if current_level == 0:
                
                selected_option = show_menu(screen, font, "Zombi Oyunu", ["Devam Et", "Çıkış"])
                if selected_option == 1:
                    continue
        elif game_over:
            end_text = font.render("Kaybettiniz! Zombiler kazandı.", True, (255, 0, 0))
        screen.blit(end_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()





if __name__ == '__main__':
    main()