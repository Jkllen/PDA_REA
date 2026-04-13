import sys
from PyQt6.QtWidgets import QApplication
from controller.app_controller import AppController


def main():
    app = QApplication(sys.argv)
    controller = AppController()
    controller.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()