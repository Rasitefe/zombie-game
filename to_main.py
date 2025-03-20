from ursina import *
import numpy as np
from perlin_noise import PerlinNoise

# Oyun başlat
app = Ursina()

# Harita boyutu
GRID_SIZE = 30
TILE_SIZE = 1

# **Perlin Noise ile doğal tepeler oluştur (Merkez tamamen düz olacak şekilde)**
def generate_height_map(size, scale=10):
    noise = PerlinNoise(octaves=4, seed=42)  # Doğal yükseklikler için
    height_map = np.zeros((size, size))
    
    for x in range(size):
        for z in range(size):
            distance_from_center = np.sqrt((x - size/2)**2 + (z - size/2)**2)
            if distance_from_center < size / 4:
                height_map[x, z] = 0  # **Merkez tamamen düz**
            else:
                smooth_factor = np.clip((distance_from_center - size / 4) / (size / 4), 0, 1)  # Kenarlarda eğim
                height_map[x, z] = noise([x / scale, z / scale]) * 2 * smooth_factor  # Kenarlar için tepe
    return height_map

# **Yükseklik haritasını oluştur**
elevation_map = generate_height_map(GRID_SIZE)

# Factorio'dan alınan arazi dokuları
grass_texture = load_texture("assets/graphics/terrain/landfill.png")
sand_texture = load_texture("assets/graphics/terrain/nuclear-ground.png")
grass_texture.wrap = "repeat"
sand_texture.wrap = "repeat"

# Kamera ayarı
EditorCamera()

# **Mesh tabanlı terrain oluşturma**
terrain = Entity(model=Mesh(), scale=(1, 1, 1))

vertices = []
triangles = []
uvs = []
textures = []

# **Doğal eğimli tepeler ekleyerek arazi oluştur (Merkez düz, kenarlar tepeli)**
for x in range(GRID_SIZE):
    for z in range(GRID_SIZE):
        y = elevation_map[x, z]  # **Merkez düz, kenarlarda eğimli tepeler**

        # **Kare yüzeyleri oluştur (iki üçgen ile)**
        v1 = Vec3(x, y, z)
        v2 = Vec3(x+1, elevation_map[min(x+1, GRID_SIZE-1), z], z)
        v3 = Vec3(x, elevation_map[x, min(z+1, GRID_SIZE-1)], z+1)
        v4 = Vec3(x+1, elevation_map[min(x+1, GRID_SIZE-1), min(z+1, GRID_SIZE-1)], z+1)

        i = len(vertices)
        vertices.extend([v1, v2, v3, v4])
        triangles.extend([i, i+1, i+2, i+1, i+3, i+2])

        # **Merkez bölge için sand-3, tepeler için grass-1**
        if y == 0:
            texture = sand_texture  # **Tamamen düz bölgeler**
            uv_y_offset = 0.0  # **UV Y ekseninin alt yarısını kullan**
        else:
            texture = grass_texture  # **Tepeler**
            uv_y_offset = 0.5  # **UV Y ekseninin üst yarısını kullan**
        
        # **Gerçek ölçekli UV koordinatları (Dikey olarak yarısını kullan)**
        uvs.extend([
            Vec2(x / GRID_SIZE, (z / GRID_SIZE) / 2 + uv_y_offset),
            Vec2((x+1) / GRID_SIZE, (z / GRID_SIZE) / 2 + uv_y_offset),
            Vec2(x / GRID_SIZE, ((z+1) / GRID_SIZE) / 2 + uv_y_offset),
            Vec2((x+1) / GRID_SIZE, ((z+1) / GRID_SIZE) / 2 + uv_y_offset)
        ])
        textures.append(texture)

# **Mesh modelini oluştur**
terrain.model.vertices = vertices
terrain.model.triangles = triangles
terrain.model.uvs = uvs
terrain.model.generate()
terrain.texture = textures[0]  # **Başlangıçta bir doku belirle**

# **Oyun döngüsünü başlat**
app.run()