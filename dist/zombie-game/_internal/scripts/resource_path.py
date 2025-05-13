import sys
import os

def resource_path(relative_path):
    """EXE içinden çağrılan dosya yolunu çözer."""
    try:
        base_path = sys._MEIPASS  # PyInstaller tarafından geçici dizin
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)