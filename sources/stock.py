from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QGridLayout, QLabel,
    QMainWindow, QMessageBox, QPushButton,
    QWidget,
)

from sources.database import fetch_all, retrieve_info
from sources.utils import open_purchase_history, play_sfx 


class StockWindow(QMainWindow):
    def __init__(self, parent=None, database=None,
    *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Manipular quantidades")
        self.setGeometry(250, 50, 900, 700)

        self.cart_window = None
        self.database = database or []

        play_sfx("stock")

        widget1 = QWidget()
        layout1 = QGridLayout(widget1)

        self.widget2: QWidget = QWidget()
        self.layout2: QGridLayout = QGridLayout(self.widget2)

        purchase_history_button = QPushButton("Ver histórico de compras")
        _ = purchase_history_button.clicked.connect(self.see_sales_report)
        close_button = QPushButton("Fechar")
        _ = close_button.clicked.connect(self.close_window)

        self.update_total_quantities(self.database)

        layout1.addWidget(self.widget2,0,0,1,1,Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(purchase_history_button,1,0,1,1,Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(close_button,2,0,1,1,Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(widget1)


    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()


    def close_window(self):
        play_sfx("close")
        _ = self.close()


    def decrease_quantity(self, item_id):
        dec = self.key_add_sub_amount()
        info = retrieve_info(item_id)

        if info is None:
            play_sfx("warning")
            self._show_message(QMessageBox.Icon.Warning, "Erro", "Não foi possível obter informações do carrinho.")
            return

        current = info["quantity"]

        if current - dec < 0:
            play_sfx("warning")
            self._show_message(QMessageBox.Icon.Warning, "Erro", "Não é possível diminuir abaixo de zero.")
            return

        new_q = current - dec
        self._set_db_quantity(item_id, new_q)
        play_sfx("information")
        self.update_total_quantities(self.database)


    def increase_quantity(self, item_id):
        add = self.key_add_sub_amount()
        info = retrieve_info(item_id)

        if info is None:
            play_sfx("warning")
            self._show_message(QMessageBox.Icon.Warning, "Erro", "Não foi possível obter informações do carrinho.")
            return

        # current stock from DB/info
        current = info["quantity"]
        new_q = current + add
        self._set_db_quantity(item_id, new_q)
        play_sfx("information")
        self.update_total_quantities(self.database)


    def key_add_sub_amount(self):
        mods = QApplication.keyboardModifiers()

        if mods & Qt.KeyboardModifier.ShiftModifier:
            return 10

        if mods & Qt.KeyboardModifier.ControlModifier:
            return 5

        return 1


    def see_sales_report(self):
        open_purchase_history(self)


    def _set_db_quantity(self, item_id: int, new_quantity: int):
        from sources.database import connect

        if new_quantity < 0:
            new_quantity = 0

        with connect() as con:
            cur = con.cursor()
            _ = cur.execute("UPDATE goods SET quantity = ? WHERE id = ?", (new_quantity, item_id))

        # Update in-memory self.database to match DB
        for good in self.database:
            if good['id'] == item_id:
                good['quantity'] = new_quantity
                break


    def _show_message(self, icon, title, text):
        _ = QMessageBox(icon, title, text, QMessageBox.StandardButton.Ok, self).exec_()


    def update_total_quantities(self, _database=None):
        self.clear_layout(self.layout2)
        self.database = fetch_all()
        database = self.database

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