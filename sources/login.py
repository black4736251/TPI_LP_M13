from PySide6.QtCore import Qt, QTimer 
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QLineEdit, 
    QMainWindow, QMessageBox, QPushButton,
    QWidget
)

from sources.cart_manager import CartManager
from sources.login_manager import LoginManager
from sources.utils import play_sfx, set_image


class LoginWindow(QMainWindow):
    def __init__(self, database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Iniciar sessão")
        self.setGeometry(250, 50, 900, 700)

        self.shop_window = None
        self.stock_window = None
        self.database = database

        play_sfx("login")

        widget = QWidget()
        layout = QGridLayout(widget)

        username_label = QLabel("Utilizador(a)")
        self.username_input: QLineEdit = QLineEdit()
        self.username_input.setPlaceholderText("Introduza aqui...")
        self.username_input.setFixedWidth(150)
        self.username_input.setFocus()
        _ = self.username_input.returnPressed.connect(self.verify_login)
        password_label = QLabel("Palavra-passe")
        self.password_input: QLineEdit = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Introduza aqui...")
        self.password_input.setFixedWidth(150)
        _ = self.password_input.returnPressed.connect(self.verify_login)
        self.password_visible: bool = False
        password_mode_button = QPushButton()
        _ = password_mode_button.clicked.connect(self.change_password_mode)
        set_image(password_mode_button, "eye", 50, 50)
        signin_button = QPushButton("Iniciar sessão")
        _ = signin_button.clicked.connect(self.verify_login)
        exit_button = QPushButton("Sair")
        _ = exit_button.clicked.connect(self.exit_program)

        layout.addWidget(username_label,0,0,1,2,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.username_input,1,0,1,2,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(password_label,2,0,1,2,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.password_input,3,0,1,2,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(password_mode_button,3,2,
        alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(signin_button,4,0,1,2,
        alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exit_button,5,0,1,2,
        alignment=Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(widget)


    def change_password_mode(self):
        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_visible = False

        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_visible = True


    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()

        if self.password_visible:
            self.change_password_mode()


    def exit_program(self):
        play_sfx("close")
        QTimer.singleShot(450, self.close)


    def _on_stock_closed(self):
        self.stock_window = None
        self.show()


    def _on_shop_closed(self):
        CartManager().clear()
        self.shop_window = None
        self.show()


    def verify_login(self):
        manager = LoginManager()
        result = manager.login(
        self.username_input.text(),
        self.password_input.text()
        )

        # Empty fields
        if result.error == "empty_fields":
            self.clear_inputs()
            play_sfx("warning")
            _ = QMessageBox(
                QMessageBox.Icon.Warning,
                "Campo(s) vazio(s)",
                "O utilizador(a) e/ou a palavra-passe está(ão) vazio(a)(os).",
                QMessageBox.StandardButton.Ok,
                self
            ).exec_()
            return

        # Invalid credentials
        if result.error == "invalid_credentials":
            self.clear_inputs()
            play_sfx("warning")
            _ = QMessageBox(
                QMessageBox.Icon.Warning,
                "Campo(s) inválido(s)",
                "O(a) utilizador(a) e/ou a palavra-passe é(estão) inválido(a)(os)(as).",
                QMessageBox.StandardButton.Ok,
                self
            ).exec_()
            return

        # Successful login
        self.clear_inputs()
        play_sfx("information")
        _ = QMessageBox(
            QMessageBox.Icon.Information,
            "Sessão iniciada",
            "Sessão iniciada com sucesso.",
            QMessageBox.StandardButton.Ok,
            self
        ).exec_()

        role = result.role

        if role == "admin":
            if self.stock_window is None:
                from sources.stock import StockWindow
                self.stock_window = StockWindow(self, self.database)
                self.stock_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
                _ = self.stock_window.destroyed.connect(self._on_stock_closed)

            self.stock_window.update_total_quantities(result.stock_data)
            self.hide()
            play_sfx("click")
            self.stock_window.show()
            self.stock_window.raise_()
            self.stock_window.activateWindow()

        else:
            if self.shop_window is None:
                from sources.shop import ShopWindow
                self.shop_window = ShopWindow(self, self.database)
                self.shop_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
                _ = self.shop_window.destroyed.connect(self._on_shop_closed)

            else:
                self.shop_window.update_car_labels()

            self.hide()
            play_sfx("click")
            self.shop_window.show()
            self.shop_window.raise_()
            self.shop_window.activateWindow()