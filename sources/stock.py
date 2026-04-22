from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QMainWindow,
    QPushButton, QWidget, QLineEdit,
    QMessageBox
)
from utils import play_sfx


class StockWindow(QMainWindow):
    def __init__(self, parent=None, cart_list=None, database=None,
    *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Manipular quantidades")
        self.setGeometry(100, 100, 1280, 720)

        self.cart_list = cart_list
        self.cart_window = None
        self.database = database

        play_sfx(self, "stock")

        widget1 = QWidget()
        layout1 = QGridLayout(widget1)

        self.widget2 = QWidget()
        self.layout2 = QGridLayout(self.widget2)

        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close_window)

        layout1.addWidget(self.widget2,0,0,1,1,Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(close_button,1,0,1,1,Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(widget1)


    def close_window(self):
        play_sfx(self, "close")
        self.close()