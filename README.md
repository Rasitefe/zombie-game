
# Zombi Oyunu - Top-Down Shooter

Bu proje, Pygame kullanılarak geliştirilmiş tam ekran destekli, kuşbakışı görünümlü bir **zombi hayatta kalma oyunudur**. Oyuncu, rastgele hareket eden zombilere karşı hayatta kalmalı ve harita üzerinde belirlenmiş çıkışa ulaşmalıdır.

## Oyun Özellikleri

- Tam ekran mod (ayarlar ile yönetilebilir)
- Animasyonlu yürüyüş sprite'ları
- Fener (ışık konisi) ile görüş alanı
- Otomatik ateş etme 
- Kapılar, duvarlar ve odalar
- Skor sistemi ve sağlık barı
- Çoklu harita desteği 

---

## Kurulum ve Çalıştırma

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/Rasitefe/zombie-game.git
cd zombie-game
```

### 2. Sanal Ortam Oluşturun

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Gereken Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

---

## ⚙️ Ortam Değişkenleri (.env)

Proje kök dizinine `.env` dosyası ekleyerek oyun sabitlerini değiştirebilirsiniz.
Ama sizlere `envsample` dosyasını bıraktık ismini `.env` yaparak devam edebilirsiniz.
```dotenv
WIDTH=1280
HEIGHT=720
PLAYER_SPEED=5
PLAYER_MAX_HEALTH=100
FOV_RADIUS=500
FOV_ANGLE=45
```

Varsayılan ayarlar `utils/constants.py` dosyasında tanımlıdır. `.env` varsa oradan alınır.

---

## Oyunu Başlatmak

```bash
python main.py
```

---

## Harita Yapısı ve Oluşturma

Haritalar `maps/` klasörü içinde JSON formatında yer alır. Her hücre bir int sayı kodu ile temsil edilir:

| Kod | Anlamı    |
|-----|-----------|
| 0   | Boş Alan  |
| 1   | Duvar     |
| 2   | Kapı      |
| 3   | Zombi     |
| 4   | Başlangıç |
| 5   | Çıkış     |

### Örnek Harita (map1.json)

```json
[
  [1, 1, 1, 1, 1],
  [1, 4, 0, 5, 1],
  [1, 3, 0, 0, 1],
  [1, 2, 0, 3, 1],
  [1, 1, 1, 1, 1]
]
```

### Yeni Harita Eklemek İçin

1. Yeni dosya oluşturun: `maps/map3.json`
2. `zombie_oyunu.py` içinde `maps = [...]` listesine ekleyin:

```python
maps = ['maps/map1.json', 'maps/map2.json', 'maps/map3.json']
```

---

## 🧪 Derlenmiş .exe Dosyası ile Çalıştırma (Windows)

### 1. PyInstaller Kurulumu

```bash
pip install pyinstaller
```

### 2. .exe Oluşturma

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "assets;assets" --add-data "maps;maps" zombie_oyunu.py
```

Oluşan dosya: `dist/zombie_oyunu.exe`

---

## Klasör Yapısı

```
zombie-game/
│
├── assets/             # Tüm görseller ve sprite'lar
│   └── PNG/...
├── classes/            # Oyuncu, Zombi gibi sınıflar
├── maps/               # JSON formatındaki haritalar
├── scripts/            # Yardımcı scriptler
├── utils/              # constants.py, yardımcı fonksiyonlar
├── .env                # Ortam değişkenleri
├── zombie_oyunu.py     # Ana oyun dosyası
├── README.md           # Bu dosya
└── requirements.txt
```
---

### Setup

1. Kök dizinde bulunan `setup.bat` dosyasını çalıştırın.
2. Kurulum bittiğinde press (boşluk tuşuna) basın ve bitirin.
3. `dist/zombie-game/zombie-game.exe` exe dosyanız iyi oyunlar...
