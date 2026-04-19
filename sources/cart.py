from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QGridLayout,
QLabel, QPushButton)
from utils import play_sfx, finalize_purchase

class CartWindow(QMainWindow):
    def __init__(self, parent=None, cart_list=None, database=None,
    *args, **kwargs, ):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Carrinho")
        self.setGeometry(100, 100, 1280, 720)

        assert cart_list is not None, '"cart_list" tem de ser uma lista.'
        self.cart_list: list = cart_list
        self.database = database

        widget = QWidget()
        layout = QGridLayout(widget)

        self.list_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.list_label.setWordWrap(True)

        self.total_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.total_label.setWordWrap(True)

        buy_button = QPushButton("Concluír compra")
        buy_button.clicked.connect(self.buy_button_click)

        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close_button_click)

        layout.addWidget(self.list_label)
        layout.addWidget(self.total_label)
        layout.addWidget(buy_button)
        layout.addWidget(close_button)

        self.update_cart_display()
        self.update_total_label()

        self.setCentralWidget(widget)

    def buy_button_click(self):
        play_sfx(self, "purchase")
        finalize_purchase(self)
        play_sfx(self, "close")
        self.close()

    def close_button_click(self):
        play_sfx(self, "close")
        self.close()

    def update_cart_display(self):
        if not self.cart_list:
            self.list_label.setText("Carrinho vazio.")
        else:
            text = "\n".join(
                f"{item['name']} — {item['quantity']}x — {item['price']}€/un."
                for item in self.cart_list
            )
            self.list_label.setText(text)

    def update_total_label(self):
        result = 0.0
        for item in self.cart_list:
            result += int(item['quantity']) * float(item['price'])
        text = f"Total: {result:.2f}€"
        self.total_label.setText(text)