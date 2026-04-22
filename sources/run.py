import sys
from database import create, load
from login import LoginWindow
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    # Cart related
    cart_list = []


    # Database related
    create() 
    database = load()


    # PySide6 related
    app = QApplication(sys.argv)
    loginwindow = LoginWindow(cart_list, database)
    loginwindow.show()
    sys.exit(app.exec())