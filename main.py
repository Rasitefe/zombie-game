import pygame
import math
import json
import sys
from scripts.resource_path import resource_path
from classes.player import Player
from classes.zombie import Zombie
from utils.constants import (
    WALL,
    DOOR,
    ZOMBIE,
    START,
    END,
    PLAYER_SPEED,
    AUTO_FIRE_DELAY,
    FOV_RADIUS,
    FOV_ANGLE,
    ZOMBIE_REVEAL_RADIUS,
    PLAYER_DAMAGE_COOLDOWN,
    PLAYER_MAX_HEALTH,
    YELLOW,
    WHITE,
    WIDTH,
    HEIGHT
)


def load_map(filename):
    with open(resource_path(filename), 'r') as f:
        return json.load(f)

#Bu fonksiyon, belirtilen dosya yolundan harita verisini (map1.json, map2.json) yükler.
#Harita JSON formatında tanımlanmış olmalı ve her hücrede;
#duvarlar, kapılar, zombiler, başlangıç ve bitiş noktaları gibi öğeler bulunur.


def get_walls_and_doors_from_grid(grid, cell_size):
    walls = []
    doors = []
    # Haritadaki her hücreyi kontrol ederek duvarları ve kapıları ayırır.
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
    #None
    # Haritada zombi, başlangıç ve bitiş noktalarını bulur.
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

def show_menu(screen, font, title, options):
    selected = 0
    clock = pygame.time.Clock()
    # ana menu ve secenekler gösterilir
    while True:
        screen.fill((0, 0, 0))
        title_text = font.render(title, True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))
         # Seçenekler eklenir, seçilen seçenek renklendirilir
        option_rects = []
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            option_text = font.render(option, True, color)
            text_rect = option_text.get_rect(center=(WIDTH // 2, 250 + i * 50))
            option_rects.append(text_rect)
            screen.blit(option_text, text_rect.topleft)

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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        return i


def main():
    pygame.init()
    current_level = 0
    maps = ['maps/map1.json','maps/map2.json']
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    selected_option = show_menu(screen, font, "Zombi Game", ["Başla", "Çıkış"])
    if selected_option == 1:
        pygame.quit()
        return

    while current_level < len(maps):
        #   # Oyun döngüsü içinde harita yüklenir ve oyuncu hareket eder
        map_file = maps[current_level]
        current_level += 1
        win = False
        game_over = False

        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zombi Game')
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)

        grid = load_map(map_file)
        grid_size = len(grid)
        cell_size = 64

        wall_image = pygame.image.load(resource_path('assets/PNG/background/wall.jpg'))
        wall_image = pygame.transform.scale(wall_image, (cell_size, cell_size))

        floor_image = pygame.image.load(resource_path('assets/PNG/background/floor.jpg'))
        floor_image = pygame.transform.scale(floor_image, (cell_size, cell_size))

        door_image = pygame.image.load(resource_path('assets/PNG/background/door.jpg'))
        door_image = pygame.transform.scale(door_image, (cell_size, cell_size))

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
            #Oyun sırasında tuşlar kontrol edilir, oyuncu hareket eder, mermiler atılır
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause = show_menu(screen, font, "Oyun Duraklatıldı", ["Devam Et", "Çıkış"])
                    if pause == 1:
                        pygame.quit()
                        sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    player.is_auto_firing = True
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    player.is_auto_firing = False

            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED
            player.move(dx, dy, walls, doors)
            player.update_angle(pygame.mouse.get_pos())

            if player.is_auto_firing:
                if current_time - player.last_auto_fire_time > AUTO_FIRE_DELAY:
                    bullets.append(player.shoot())
                    player.last_auto_fire_time = current_time

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

            camera_x = player.x - WIDTH // 2
            camera_y = player.y - HEIGHT // 2

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

            health_ratio = player.health / PLAYER_MAX_HEALTH
            health_color = (0, 255, 0) if health_ratio > 0.5 else (255, 255, 0) if health_ratio > 0.2 else (255, 0, 0)
            pygame.draw.rect(screen, (50, 50, 50), (10, 50, 200, 20))
            pygame.draw.rect(screen, health_color, (10, 50, 200 * health_ratio, 20))

            score_text = font.render(f"Skor: {player.score}", True, WHITE)
            screen.blit(score_text, (10, 10))

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

            if current_time - player.last_damage_time < 300:
                red_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 100))
                screen.blit(red_overlay, (0, 0))

            pygame.display.flip()
            clock.tick(60)

        screen.fill((0, 0, 0))
        if win:
            # Süre hesapla
            elapsed_time = pygame.time.get_ticks() // 1000

            screen.fill((0, 0, 0))
            title_text = font.render("🎉 Kazandınız! Tebrikler!", True, (0, 255, 0))
            score_text = font.render(f"Skorunuz: {player.score}", True, WHITE)
            time_text = font.render(f"Geçen Süre: {elapsed_time} saniye", True, WHITE)

            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + 20))

            pygame.display.flip()
            pygame.time.wait(2000)

            if current_level < len(maps):
                selected_option = show_menu(screen, font, "Bölüm Tamamlandı", ["Devam Et", "Çıkış"])
                if selected_option == 1:
                    pygame.quit()
                    sys.exit()
        elif game_over:
            end_text = font.render("Kaybettiniz! Zombiler kazandı.", True, (255, 0, 0))
            screen.blit(end_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

    pygame.quit()




if __name__ == '__main__':
    main()