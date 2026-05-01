from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QMainWindow,
    QMessageBox, QPushButton, QWidget
)
from sources.utils import add_to_cart, set_image, play_sfx
from sources.database import retrieve_info


class ShopWindow(QMainWindow):
    def __init__(self, parent=None, cart_list=None, database=None,
    *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Loja de carrinhos")
        self.setGeometry(250, 50, 900, 700)

        self.cart_list = cart_list or []
        self.cart_window = None
        self.database = database

        play_sfx(self,"shop")

        widget = QWidget()
        layout = QGridLayout(widget)

        greeting_label = QLabel('Carrinhos "Hot-Wheels" (Rodas-Quentes):')

        cart_button = QPushButton()
        cart_button.setFixedWidth(100)
        set_image(cart_button, "cart", 100, 100)
        _ = cart_button.clicked.connect(self.open_cart_window)

        bolide_button = QPushButton()
        set_image(bolide_button,"bugatti_bolide", 300, 300)
        _ = bolide_button.clicked.connect(lambda: add_to_cart(self, 1))

        miata_button = QPushButton()
        set_image(miata_button, "mazda_mx-5", 300, 300)
        _ = miata_button.clicked.connect(lambda: add_to_cart(self, 2))

        nissan_gt_r_button = QPushButton()
        set_image(nissan_gt_r_button, "nissan_gt-r",
        300, 300)
        _ = nissan_gt_r_button.clicked.connect(lambda: add_to_cart(self, 3))

        self.bolide_label: QLabel = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.bolide_label.setWordWrap(True)

        self.miata_label: QLabel = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.miata_label.setWordWrap(True)

        self.nissan_gt_r_label: QLabel = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.nissan_gt_r_label.setWordWrap(True)

        close_button = QPushButton("Fechar")
        _ = close_button.clicked.connect(self.close_button_click)

        layout.addWidget(greeting_label, 0, 0, 1, 3,
        Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(cart_button, 0, 2, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(bolide_button, 1, 0)
        layout.addWidget(self.bolide_label, 2, 0)
        layout.addWidget(miata_button, 1, 1)
        layout.addWidget(self.miata_label, 2, 1)
        layout.addWidget(nissan_gt_r_button, 1, 2)
        layout.addWidget(self.nissan_gt_r_label, 2, 2)
        layout.addWidget(close_button, 3, 0, 1, 3)

        self.update_car_labels()
        self.setCentralWidget(widget)


    def close_button_click(self):
        play_sfx(self, "close")
        QTimer.singleShot(450, self.close)


    def open_cart_window(self):
        if not self.cart_list:
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning,
            "Carrinho vazio",
            ("O carrinho está vazio. Por favor, selecione pelo menos"
            " um carrinho."),
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        if self.cart_window is None:
            from sources.cart import CartWindow
            self.cart_window = CartWindow(self, self.cart_list,
            self.database)
            self.cart_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.cart_window.destroyed.connect(self._on_cart_closed)
        else:
            self.cart_window.update_cart_display()
        self.cart_window.update_cart_display()
        play_sfx(self, "click")
        self.cart_window.show()
        self.cart_window.raise_()
        self.cart_window.activateWindow()


    def increase_quantity(self, index):
        if not self.cart_list:
            return
        car_id = self.cart_list[index]['id']
        info = retrieve_info(car_id)
        if info is None:
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning,
            "Erro", "Não foi possível obter informações do produto.",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        quantity = info["quantity"]
        if self.cart_list[index]["quantity"] + 1 > quantity:
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning,
            "Limite atingido", "Atingiu o limite do carrinho.",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        self.cart_list[index]["quantity"] += 1
        if self.cart_window is not None:
            self.cart_window.update_cart_display()
            self.cart_window.update_total_label()


    def update_car_labels(self):
        car_ids = {
            1: self.bolide_label,
            2: self.miata_label,
            3: self.nissan_gt_r_label
        }

        for car_id, label in car_ids.items():
            info = retrieve_info(car_id)
            if info is None:
                label.setText("Erro ao carregar informações.")
                continue

            name = info["name"]
            price = info["price"]
            quantity = info["quantity"]

            label.setText(
                f"{name}\nPreço: {price:.2f}€\nStock: {quantity}"
            )


    def _on_cart_closed(self):
        self.cart_window = None
        self.show()