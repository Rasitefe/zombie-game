import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def get_int(name, default):
    return int(os.getenv(name, default))

# Ayarları al
WIDTH = get_int("WIDTH", 1200)
HEIGHT = get_int("HEIGHT", 800)

PLAYER_SPEED = get_int("PLAYER_SPEED", 5)
PLAYER_MAX_HEALTH = get_int("PLAYER_MAX_HEALTH", 100)
PLAYER_DAMAGE_COOLDOWN = get_int("PLAYER_DAMAGE_COOLDOWN", 1000)

FOV_RADIUS = get_int("FOV_RADIUS", 500)
FOV_ANGLE = get_int("FOV_ANGLE", 45)
ZOMBIE_REVEAL_RADIUS = get_int("ZOMBIE_REVEAL_RADIUS", 150)

ZOMBIE_SPEED = get_int("ZOMBIE_SPEED", 2)
ZOMBIE_CHASE_SPEED = get_int("ZOMBIE_CHASE_SPEED", 4)
ZOMBIE_COUNT = get_int("ZOMBIE_COUNT", 3)
ZOMBIE_SPACING = get_int("ZOMBIE_SPACING", 50)

BULLET_SPEED = get_int("BULLET_SPEED", 10)
BULLET_DAMAGE = get_int("BULLET_DAMAGE", 1)
RESPAWN_DELAY = get_int("RESPAWN_DELAY", 2000)
AUTO_FIRE_DELAY = get_int("AUTO_FIRE_DELAY", 100)

ROOM_SIZE = get_int("ROOM_SIZE", 400)
WALL_THICKNESS = get_int("WALL_THICKNESS", 20)
DOOR_SIZE = get_int("DOOR_SIZE", 100)
DOOR_OPEN_DISTANCE = get_int("DOOR_OPEN_DISTANCE", 100)
GRID_ROWS = get_int("GRID_ROWS", 2)
GRID_COLS = get_int("GRID_COLS", 2)

# Sabit ID'ler
EMPTY, WALL, DOOR, ZOMBIE, START, END = range(6)

# Renkler
BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
RED        = (255, 0, 0)
GREEN      = (0, 255, 0)
BLUE       = (0, 0, 255)
YELLOW     = (255, 255, 0)
GRAY       = (100, 100, 100)
BROWN      = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
# Bu kod, bir oyun için çeşitli ayarları ve sabitleri .env dosyasından yükler. 
# dotenv kütüphanesi kullanılarak ortam değişkenleri (.env dosyasındaki değerler) Python programına aktarılır.
#  Bu sayede oyun ayarları dışarıdan yapılandırılabilir. 