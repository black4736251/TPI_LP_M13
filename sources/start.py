import sys

from PySide6.QtWidgets import QApplication

from sources.database import create, load
from sources.login import LoginWindow


def main():
    # Databases and data
    cart_list = []
    create() # Creates the database
    database = load()

    # Opens the program
    app: QApplication = QApplication(sys.argv)
    loginwindow = LoginWindow(cart_list, database)
    loginwindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()