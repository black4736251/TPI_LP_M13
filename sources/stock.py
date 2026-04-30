from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QMainWindow,
    QPushButton, QWidget, QLineEdit,
    QMessageBox
)
from utils import play_sfx
from database import retrieve_info


class StockWindow(QMainWindow):
    def __init__(self, parent=None, cart_list=None, database=None,
    *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Manipular quantidades")
        self.setGeometry(250, 50, 900, 700)

        self.cart_list = cart_list
        self.cart_window = None
        self.database = database or []

        play_sfx(self, "stock")

        widget1 = QWidget()
        layout1 = QGridLayout(widget1)

        self.widget2 = QWidget()
        self.layout2 = QGridLayout(self.widget2)

        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close_window)

        self.update_total_quantities(database)

        layout1.addWidget(self.widget2,0,0,1,1,Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(close_button,1,0,1,1,Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(widget1)


    def close_window(self):
        play_sfx(self, "close")
        self.close()


    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


    def update_total_quantities(self, database):
        self.clear_layout(self.layout2)

        for index, item in enumerate(database):
            name_label = QLabel(item['name'])
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            price_label = QLabel(str(item['price'])+"€")
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if item['quantity'] == 0:
                quantity_label = QLabel("Sem quantidade.")
            else:
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


    def increase_quantity(self, i):
        car_id = self.database[i]['id']
        info = retrieve_info(car_id)
        if info is None:
            play_sfx(self, "warning")
            QMessageBox(QMessageBox.Icon.Warning,
            "Erro", "Não foi possível obter informações do carrinho.",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        self.database[i]["quantity"] += 1
        play_sfx(self, "information")
        QMessageBox(QMessageBox.Icon.Information,
            "Quantidade aumentada", ("A quantidade do carrinho foi"
            "aumentada com sucesso."),
            QMessageBox.StandardButton.Ok, self).exec_()
        self.update_total_quantities(self.database)


    def decrease_quantity(self, i):
        if self.database[i]["quantity"] > 1:
            self.database[i]["quantity"] -= 1
            play_sfx(self, "information")
            QMessageBox(QMessageBox.Icon.Information,
            "Sucesso", "Quantidade do carrinho aumentada com sucesso.",
            QMessageBox.StandardButton.Ok, self).exec_()
        else:
            play_sfx(self, "warning")
            QMessageBox(QMessageBox.Icon.Warning,
            "Erro", ("Não é possível transformar a quantidade"
            "em um número negativo."),
            QMessageBox.StandardButton.Ok, self).exec_()


        self.update_total_quantities(self.database)