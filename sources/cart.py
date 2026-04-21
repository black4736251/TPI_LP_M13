from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout,
    QLabel, QPushButton, QMessageBox
)
from database import retrieve_info
from utils import finalize_purchase, play_sfx 

class CartWindow(QMainWindow):
    def __init__(self, parent=None, cart_list=None, database=None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Carrinho")
        self.setGeometry(100, 100, 1280, 720)

        assert cart_list is not None, '"cart_list" tem de ser uma lista.'
        self.cart_list: list = cart_list
        self.database = database

        widget1 = QWidget()
        layout1 = QGridLayout(widget1)

        self.widget2 = QWidget()
        self.layout2 = QGridLayout(self.widget2)

        self.total_label = QLabel(
        alignment=Qt.AlignmentFlag.AlignCenter)
        self.total_label.setWordWrap(True)

        buy_button = QPushButton("Concluír compra")
        buy_button.clicked.connect(self.buy_button_click)

        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close_button_click)

        layout1.addWidget(self.widget2, 1, 0, 1, 5,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(self.total_label, 2, 0, 1, 5,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(buy_button, 3, 0, 1, 5,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(close_button, 4, 0, 1, 5,
        alignment=Qt.AlignmentFlag.AlignCenter)

        self.update_cart_display()
        self.update_total_label()

        self.setCentralWidget(widget1)

    def buy_button_click(self):
        if not self.cart_list:
            play_sfx(self, "warning")
            QMessageBox(QMessageBox.Icon.Warning,"Carrinho vazio",
            "O carrinho está vazio. Por favor, adicione algum carrinho.",
            QMessageBox.StandardButton.Ok, self).exec_()
            self.close()
            return
        play_sfx(self, "purchase")
        finalize_purchase(self)
        play_sfx(self, "close")
        self.close()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def close_button_click(self):
        play_sfx(self, "close")
        self.close()

    def decrease_quantity(self, index):
        if self.cart_list[index]["quantity"] > 1:
            self.cart_list[index]["quantity"] -= 1
        else:
            self.cart_list.pop(index)

        self.update_cart_display()
        self.update_total_label()

    def increase_quantity(self, index):
        car_id = self.cart_list[index]['id']
        info = retrieve_info(car_id)
        if info is None:
            play_sfx(self, "warning")
            QMessageBox(QMessageBox.Icon.Warning,
            "Erro", "Não foi possível obter informações do produto.",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        quantity = info[2]
        if self.cart_list[index]["quantity"] + 1 > quantity:
            play_sfx(self, "warning")
            QMessageBox(QMessageBox.Icon.Warning,
            "Limite atingido", "Atingiu o limite do carrinho.",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        self.cart_list[index]["quantity"] += 1
        self.update_cart_display()
        self.update_total_label()

    def update_cart_display(self):
        self.clear_layout(self.layout2)

        if not self.cart_list:
            empty_label = QLabel("Carrinho vazio.")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(empty_label, 0, 0)
            return

        for index, item in enumerate(self.cart_list):
            name_label = QLabel(item['name'])
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            price_label = QLabel(str(item['price'])+"€")
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            quantity_label = QLabel(str(item['quantity']))
            quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            decrease_button = QPushButton("-")
            decrease_button.setFixedWidth(40)
            decrease_button.clicked.connect(lambda _,
            i=index: self.decrease_quantity(i))

            increase_button = QPushButton("+")
            increase_button.setFixedWidth(40)
            increase_button.clicked.connect(lambda _,
            i=index: self.increase_quantity(i))

            self.layout2.addWidget(name_label, index, 0,
            alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(price_label, index, 1,
            alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(quantity_label, index, 2,
            alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(decrease_button, index, 3,
            alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(increase_button, index, 4,
            alignment=Qt.AlignmentFlag.AlignCenter)

    def update_total_label(self):
        result = sum(int(item['quantity']) *
        float(item['price'])
        for item in self.cart_list)
        self.total_label.setText(f"Total: {result:.2f}€")