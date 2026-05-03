import sys

from PySide6.QtWidgets import QApplication
from typing import Any

from sources.database import create, fetch_all
from sources.login import LoginWindow


def main():
    # Database
    create() # Creates the database
    database: list[dict[str, Any]] = fetch_all() # Loads the database

    # Opens the program
    app: QApplication = QApplication(sys.argv)
    loginwindow = LoginWindow(database)
    loginwindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()