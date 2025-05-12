import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect

EMPTY = 0
WALL = 1
DOOR = 2
ZOMBIE = 3
START = 4
END = 5

COLORS = {
    EMPTY: QColor(255, 255, 255),
    WALL: QColor(80, 80, 80),
    DOOR: QColor(160, 82, 45),
    ZOMBIE: QColor(200, 0, 0),
    START: QColor(0, 120, 255),
    END: QColor(0, 200, 0)
}

class MapEditor(QWidget):
    def __init__(self, grid_size, cell_size):
        super().__init__()
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = cell_size
        self.grid = [[EMPTY for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.selected_tool = WALL
        self.start_set = False
        self.end_set = False
        self.setFixedSize(self.GRID_SIZE * self.CELL_SIZE, self.GRID_SIZE * self.CELL_SIZE)

    def paintEvent(self, event):
        qp = QPainter(self)
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                rect = QRect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                qp.setBrush(COLORS[self.grid[y][x]])
                qp.setPen(QPen(Qt.black, 1))
                qp.drawRect(rect)
        # Izgara çizgileri
        qp.setPen(QPen(Qt.gray, 1, Qt.DotLine))
        for i in range(self.GRID_SIZE + 1):
            qp.drawLine(i * self.CELL_SIZE, 0, i * self.CELL_SIZE, self.GRID_SIZE * self.CELL_SIZE)
            qp.drawLine(0, i * self.CELL_SIZE, self.GRID_SIZE * self.CELL_SIZE, i * self.CELL_SIZE)

    def mousePressEvent(self, event):
        x = event.x() // self.CELL_SIZE
        y = event.y() // self.CELL_SIZE
        if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
            if self.selected_tool == START:
                # Sadece bir başlangıç noktası olsun
                if self.start_set:
                    for row in self.grid:
                        for i in range(len(row)):
                            if row[i] == START:
                                row[i] = EMPTY
                self.start_set = True
            if self.selected_tool == END:
                # Sadece bir bitiş noktası olsun
                if self.end_set:
                    for row in self.grid:
                        for i in range(len(row)):
                            if row[i] == END:
                                row[i] = EMPTY
                self.end_set = True
            self.grid[y][x] = self.selected_tool
            self.update()

    def set_tool(self, tool):
        self.selected_tool = tool

    def save_map(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.grid, f)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Harita Editörü')
        # Tam ekran ve grid ayarı
        screen = QApplication.primaryScreen().geometry()
        grid_size = 40
        cell_size = min(screen.width(), screen.height()) // grid_size
        self.editor = MapEditor(grid_size, cell_size)
        self.init_ui()
        self.showFullScreen()

    def init_ui(self):
        main_layout = QVBoxLayout()
        tool_layout = QHBoxLayout()
        btn_wall = QPushButton('Duvar')
        btn_door = QPushButton('Kapı')
        btn_zombie = QPushButton('Zombi')
        btn_start = QPushButton('Başlangıç')
        btn_end = QPushButton('Bitiş')
        btn_empty = QPushButton('Sil')
        btn_save = QPushButton('Kaydet')
        info = QLabel('Araç seçin ve hücreye tıklayın. Sadece bir başlangıç/bitiş noktası olabilir.')

        btn_wall.clicked.connect(lambda: self.editor.set_tool(WALL))
        btn_door.clicked.connect(lambda: self.editor.set_tool(DOOR))
        btn_zombie.clicked.connect(lambda: self.editor.set_tool(ZOMBIE))
        btn_start.clicked.connect(lambda: self.editor.set_tool(START))
        btn_end.clicked.connect(lambda: self.editor.set_tool(END))
        btn_empty.clicked.connect(lambda: self.editor.set_tool(EMPTY))
        btn_save.clicked.connect(self.save_map)

        tool_layout.addWidget(btn_wall)
        tool_layout.addWidget(btn_door)
        tool_layout.addWidget(btn_zombie)
        tool_layout.addWidget(btn_start)
        tool_layout.addWidget(btn_end)
        tool_layout.addWidget(btn_empty)
        tool_layout.addWidget(btn_save)

        main_layout.addWidget(info)
        main_layout.addLayout(tool_layout)
        main_layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.setFixedSize(container.sizeHint())

    def save_map(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Haritayı Kaydet', '', 'JSON Files (*.json)')
        if filename:
            self.editor.save_map(filename)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_()) 