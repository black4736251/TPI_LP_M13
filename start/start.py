import sys
import os


# Ensure project root (parent of start/) is on sys.path so 'sources' is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


from sources.database import create, load
from sources.login import LoginWindow
from PySide6.QtWidgets import QApplication


def main():
    cart_list = []

    # Database
    create()
    database = load()

    # PySide6
    app: QApplication = QApplication(sys.argv)
    loginwindow = LoginWindow(cart_list, database)
    loginwindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()