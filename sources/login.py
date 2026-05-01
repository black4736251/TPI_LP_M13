from PySide6.QtCore import QSize, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel, QGridLayout, QLineEdit,
    QMainWindow, QMessageBox, QPushButton,
    QWidget
)
from sources.database import check_login, get_user
from sources.utils import play_sfx


class LoginWindow(QMainWindow):
    def __init__(self, cart_list, database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Iniciar sessão")
        self.setGeometry(250, 50, 900, 700)

        self.cart_list = cart_list
        self.shop_window = None
        self.stock_window = None
        self.database = database

        play_sfx(self,"login")

        widget = QWidget()
        layout = QGridLayout(widget)

        username_label = QLabel("Nome de utilizador")
        self.username_input: QLineEdit = QLineEdit()
        self.username_input.setPlaceholderText("Introduza aqui...")
        self.username_input.setFixedWidth(150)
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
        password_mode_icon = QIcon("images/eye.png")
        password_mode_button.setIcon(password_mode_icon)
        password_mode_button.setIconSize(QSize(32,32))
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


    def verify_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            self.clear_inputs()
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning, "Campo(s) vazio(s)",
            "O nome de utilizador e/ou a palavra-passe está(ão) vazio(a)(os).",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        if check_login(username, password):
            self.clear_inputs()
            play_sfx(self, "information")
            _ = QMessageBox(QMessageBox.Icon.Information, "Sessão iniciada",
            "Sessão iniciada com sucesso.", QMessageBox.StandardButton.Ok,
            self).exec_()
            user = get_user(username)
            role = user[3]
            if role == "admin":
                if self.stock_window is None:
                    from sources.stock import StockWindow
                    self.stock_window = StockWindow(self,
                    self.cart_list, self.database)
                play_sfx(self, "click")
                self.stock_window.show()
                self.stock_window.raise_()
                self.stock_window.activateWindow()
            else:
                if self.shop_window is None:
                    from sources.shop import ShopWindow
                    self.shop_window = ShopWindow(self,
                    self.cart_list, self.database)
                else:
                    self.shop_window.update_car_labels()
                play_sfx(self, "click")
                self.shop_window.show()
                self.shop_window.raise_()
                self.shop_window.activateWindow()
        else:
            self.clear_inputs()
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning, "Campo(s) inválido(s)",
            ("O nome de utilizador e/ou a palavra-passe é(estão)"
            "inválido(a)(os)."),
            QMessageBox.StandardButton.Ok, self).exec_()
            return


    def exit_program(self):
        play_sfx(self, "close")
        QTimer.singleShot(450, self.close)