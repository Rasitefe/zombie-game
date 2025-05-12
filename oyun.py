import pygame
import sys
import random
import os

# Oyun için sabitler
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Grafik dosyalarını yükle
def load_image(name):
    return pygame.image.load(os.path.join('Graphics', name)).convert_alpha()

# Yılanın başlangıç ayarları
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Yılan Oyunu')
    clock = pygame.time.Clock()

    # Grafikleri yükle
    head_up = load_image('head_up.png')
    head_down = load_image('head_down.png')
    head_left = load_image('head_left.png')
    head_right = load_image('head_right.png')
    body_horizontal = load_image('body_horizontal.png')
    body_vertical = load_image('body_vertical.png')
    tail_up = load_image('tail_up.png')
    tail_down = load_image('tail_down.png')
    tail_left = load_image('tail_left.png')
    tail_right = load_image('tail_right.png')
    apple = load_image('apple.png')

    while True:
        snake = [(100, 100), (80, 100), (60, 100)]
        direction = (CELL_SIZE, 0)
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        score = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)

            # Yılanı hareket ettir
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, new_head)

            # Yılan yemeği yedi mi?
            if snake[0] == food:
                score += 1
                food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            else:
                snake.pop()

            # Çarpışma kontrolü
            if (
                snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT or
                snake[0] in snake[1:]
            ):
                break  # Oyun biter

            # Ekranı çiz
            screen.fill(BLACK)
            for i, segment in enumerate(snake):
                if i == 0:  # Baş
                    if direction == (0, -CELL_SIZE):
                        screen.blit(head_up, segment)
                    elif direction == (0, CELL_SIZE):
                        screen.blit(head_down, segment)
                    elif direction == (-CELL_SIZE, 0):
                        screen.blit(head_left, segment)
                    else:
                        screen.blit(head_right, segment)
                elif i == len(snake) - 1:  # Kuyruk
                    prev_segment = snake[i - 1]
                    if prev_segment[0] > segment[0]:
                        screen.blit(tail_left, segment)
                    elif prev_segment[0] < segment[0]:
                        screen.blit(tail_right, segment)
                    elif prev_segment[1] > segment[1]:
                        screen.blit(tail_up, segment)
                    else:
                        screen.blit(tail_down, segment)
                else:  # Gövde
                    prev_segment = snake[i - 1]
                    next_segment = snake[i + 1]
                    if prev_segment[0] == next_segment[0]:
                        screen.blit(body_vertical, segment)
                    else:
                        screen.blit(body_horizontal, segment)

            screen.blit(apple, food)
            pygame.display.flip()
            clock.tick(10)

        print(f'Oyun bitti! Skorunuz: {score}')
        print('Tekrar oynamak için bir tuşa basın...')
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

if __name__ == '__main__':
    main() 