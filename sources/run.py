import sys
from database import create, load
from main import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    # Cart related
    cart_list = []
    # Database related
    create() 
    database = load()
    # PySide6 related
    app = QApplication(sys.argv)
    mainwindow = MainWindow(cart_list, database)
    mainwindow.show()
    sys.exit(app.exec())