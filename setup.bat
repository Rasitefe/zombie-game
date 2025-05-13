@echo off
echo [1/4] Sanal ortam etkinleştiriliyor..
call venv\Scripts\activate

echo [2/4] PyInstaller kontrol ediliyor..
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller yüklü değil. Yükleniyor..
    pip install pyinstaller
)

echo [3/4] Eski derlemeler temizleniyor..
rmdir /s /q build
rmdir /s /q dist
del /q zombie-game.spec

echo [4/4] EXE oluşturuluyor...
pyinstaller --noconfirm --clean ^
--add-data "scripts;scripts" ^
--add-data "assets;assets" ^
--add-data "maps;maps" ^
--add-data ".env;." ^
--name zombie-game ^
--windowed main.py

echo.
echo --------------------------------------
echo ✔ Build tamamlandı!
echo EXE dosyası: dist\zombie-game\zombie-game.exe
echo --------------------------------------
pause
