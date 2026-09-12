import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from app.config import APP_ICON
from app.customer_form import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("New Customer Registration")
    if APP_ICON.exists():
        window.setWindowIcon(QIcon(str(APP_ICON)))
    window.setFixedSize(805, 500)
    window.setStyleSheet("background:bisque;")
    window.move(900, 520)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
