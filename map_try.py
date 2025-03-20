from ursina import *
from PIL import Image

app = Ursina()

ROOM_SIZE = 5  # Oda boyutu (5x5 kare)
WALL_HEIGHT = 3  # Duvar yüksekliği
WALL_THICKNESS = 0.5  # Duvar kalınlığı
TEXTURE_SIZE = 64  # Kullanılacak dokunun kesilecek en küçük kare boyutu (px)
DOOR_WIDTH = 1.5  # Kapı genişliği
MAP_LAYOUT = [  # 1 = oda, 0 = boşluk
    [1, 1, 0, 1],
    [1, 0, 1, 1],
    [1, 1, 1, 0],
]

# **Dokuları 64x64 olarak kırpma fonksiyonu**
def crop_texture(image_path):
    img = Image.open(image_path)
    cropped_img = img.crop((0, 0, TEXTURE_SIZE, TEXTURE_SIZE))
    cropped_img.save("cropped_" + image_path.split("/")[-1])
    return load_texture("cropped_" + image_path.split("/")[-1])

tile_floor = crop_texture("assets/graphics/terrain/stone-path/stone-path-1.png")
tile_wall = crop_texture("assets/graphics/terrain/tutorial-grid/tutorial-grid1.png")

EditorCamera()

# **Tüm zemini oluştur (Odaların içini de dolduracak şekilde)**
for x in range(len(MAP_LAYOUT)):
    for z in range(len(MAP_LAYOUT[0])):
        texture_scale_factor = ROOM_SIZE / (TEXTURE_SIZE / 64)  # **Gerçek ölçekte kaç doku sığacağını hesapla**
        Entity(
            model='cube', texture=tile_floor, 
            scale=(ROOM_SIZE, 0.5, ROOM_SIZE), 
            position=(x*ROOM_SIZE, -0.25, z*ROOM_SIZE), 
            collider=None, texture_scale=(texture_scale_factor, texture_scale_factor)
        )

# **Odaları ve duvarları oluştur**
for x in range(len(MAP_LAYOUT)):
    for z in range(len(MAP_LAYOUT[0])):
        if MAP_LAYOUT[x][z] == 1:
            texture_scale_factor = ROOM_SIZE / (TEXTURE_SIZE / 64)
            
            # **Sol duvar**
            if x == 0 or MAP_LAYOUT[x-1][z] == 0:
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(WALL_THICKNESS, WALL_HEIGHT, ROOM_SIZE - DOOR_WIDTH), 
                    position=(x*ROOM_SIZE - ROOM_SIZE/2, WALL_HEIGHT/2, z*ROOM_SIZE + DOOR_WIDTH/2),
                    texture_scale=(1, texture_scale_factor)
                )
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(WALL_THICKNESS, WALL_HEIGHT, ROOM_SIZE - DOOR_WIDTH), 
                    position=(x*ROOM_SIZE - ROOM_SIZE/2, WALL_HEIGHT/2, z*ROOM_SIZE - DOOR_WIDTH/2),
                    texture_scale=(1, texture_scale_factor)
                )
            
            # **Sağ duvar**
            if x == len(MAP_LAYOUT)-1 or MAP_LAYOUT[x+1][z] == 0:
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(WALL_THICKNESS, WALL_HEIGHT, ROOM_SIZE - DOOR_WIDTH), 
                    position=(x*ROOM_SIZE + ROOM_SIZE/2, WALL_HEIGHT/2, z*ROOM_SIZE + DOOR_WIDTH/2),
                    texture_scale=(1, texture_scale_factor)
                )
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(WALL_THICKNESS, WALL_HEIGHT, ROOM_SIZE - DOOR_WIDTH), 
                    position=(x*ROOM_SIZE + ROOM_SIZE/2, WALL_HEIGHT/2, z*ROOM_SIZE - DOOR_WIDTH/2),
                    texture_scale=(1, texture_scale_factor)
                )
            
            # **Ön duvar**
            if z == 0 or MAP_LAYOUT[x][z-1] == 0:
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(ROOM_SIZE - DOOR_WIDTH, WALL_HEIGHT, WALL_THICKNESS), 
                    position=(x*ROOM_SIZE + DOOR_WIDTH/2, WALL_HEIGHT/2, z*ROOM_SIZE - ROOM_SIZE/2),
                    texture_scale=(texture_scale_factor, 1)
                )
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(ROOM_SIZE - DOOR_WIDTH, WALL_HEIGHT, WALL_THICKNESS), 
                    position=(x*ROOM_SIZE - DOOR_WIDTH/2, WALL_HEIGHT/2, z*ROOM_SIZE - ROOM_SIZE/2),
                    texture_scale=(texture_scale_factor, 1)
                )
            
            # **Arka duvar**
            if z == len(MAP_LAYOUT[0])-1 or MAP_LAYOUT[x][z+1] == 0:
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(ROOM_SIZE - DOOR_WIDTH, WALL_HEIGHT, WALL_THICKNESS), 
                    position=(x*ROOM_SIZE + DOOR_WIDTH/2, WALL_HEIGHT/2, z*ROOM_SIZE + ROOM_SIZE/2),
                    texture_scale=(texture_scale_factor, 1)
                )
                Entity(
                    model='cube', texture=tile_wall, 
                    scale=(ROOM_SIZE - DOOR_WIDTH, WALL_HEIGHT, WALL_THICKNESS), 
                    position=(x*ROOM_SIZE - DOOR_WIDTH/2, WALL_HEIGHT/2, z*ROOM_SIZE + ROOM_SIZE/2),
                    texture_scale=(texture_scale_factor, 1)
                )

app.run()