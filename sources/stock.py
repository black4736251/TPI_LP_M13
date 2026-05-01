from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QMainWindow,
    QPushButton, QWidget, QMessageBox
)
from sources.utils import play_sfx
from sources.database import retrieve_info


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

        self.widget2: QWidget = QWidget()
        self.layout2: QGridLayout = QGridLayout(self.widget2)

        close_button = QPushButton("Fechar")
        _ = close_button.clicked.connect(self.close_window)

        self.update_total_quantities(self.database)

        layout1.addWidget(self.widget2,0,0,1,1,Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(close_button,1,0,1,1,Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(widget1)


    def close_window(self):
        play_sfx(self, "close")
        _ = self.close()


    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


    def update_total_quantities(self, database):
        self.clear_layout(self.layout2)

        for row, item in enumerate(database):
            name_label = QLabel(item['name'])
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            price_label = QLabel(str(item['price']) + "€")
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if item['quantity'] == 0:
                quantity_label = QLabel("Sem quantidade.")
            else:
                quantity_label = QLabel(str(item['quantity']))
                quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            decrease_button = QPushButton("-")
            decrease_button.setFixedWidth(40)
            _ = decrease_button.clicked.connect(lambda _, item_id=item['id']: self.decrease_quantity(item_id))

            increase_button = QPushButton("+")
            increase_button.setFixedWidth(40)
            _ = increase_button.clicked.connect(lambda _, item_id=item['id']: self.increase_quantity(item_id))

            self.layout2.addWidget(name_label, row, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(price_label, row, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(quantity_label, row, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(decrease_button, row, 3, alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout2.addWidget(increase_button, row, 4, alignment=Qt.AlignmentFlag.AlignCenter)


    def increase_quantity(self, item_id):
        info = retrieve_info(item_id)
        if info is None:
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning, "Erro", "Não foi possível obter informações do carrinho.",
                QMessageBox.StandardButton.Ok, self).exec_()
            return
        new_q = info['quantity'] + 1
        self._set_db_quantity(item_id, new_q)
        play_sfx(self, "information")
        _ = QMessageBox(QMessageBox.Icon.Information, "Quantidade aumentada",
        "A quantidade do carrinho foi aumentada com sucesso.",
        QMessageBox.StandardButton.Ok, self).exec_()
        # Refresh UI using current self.database
        self.update_total_quantities(self.database)


    def decrease_quantity(self, item_id):
        info = retrieve_info(item_id)
        if info is None:
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning, "Erro", "Não foi possível obter informações do carrinho.",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        if info['quantity'] <= 0:
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning, "Erro",
            "Não é possível transformar a quantidade em um número negativo.",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        new_q = info['quantity'] - 1
        self._set_db_quantity(item_id, new_q)
        play_sfx(self, "information")
        _ = QMessageBox(QMessageBox.Icon.Information, "Sucesso",
        "Quantidade do carrinho foi diminuída com sucesso.",
        QMessageBox.StandardButton.Ok, self).exec_()
        self.update_total_quantities(self.database)

    
    def _set_db_quantity(self, item_id: int, new_quantity: int):
        from sources.database import connect
        if new_quantity < 0:
            new_quantity = 0
        with connect() as con:
            cur = con.cursor()
            _ = cur.execute("UPDATE goods SET quantity = ? WHERE id = ?", (new_quantity, item_id))
        # Update in-memory self.database to match DB
        for it in self.database:
            if it['id'] == item_id:
                it['quantity'] = new_quantity
                break