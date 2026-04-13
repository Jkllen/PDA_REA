from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget
from view.qt.login_screen import LoginScreen
from view.qt.signup_screen import SignupScreen
from view.qt.risk_input_screen import RiskInputScreen
from view.qt.result_screen import ResultScreen
from view.qt.ui_parts import DecorativeBackground


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pre-Driving Accident Risk Evaluation and Advisory")
        self.resize(1100, 760)
        self.setMinimumSize(950, 650)

        background_path = Path("assets/background.png")
        bg_path_str = str(background_path) if background_path.exists() else ""

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.background = DecorativeBackground(bg_path_str)
        layout.addWidget(self.background)

        self.stack = QStackedWidget(self.background)
        self.stack.setGeometry(self.background.rect())

        self.login_screen = LoginScreen(self.background)
        self.signup_screen = SignupScreen(self.background)
        self.risk_input_screen = RiskInputScreen(self.background)
        self.result_screen = ResultScreen(self.background)

        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.signup_screen)
        self.stack.addWidget(self.risk_input_screen)
        self.stack.addWidget(self.result_screen)

        self.show_login()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.stack.setGeometry(self.background.rect())

    def show_login(self):
        self.background.set_header_mode("auth")
        self.stack.setCurrentWidget(self.login_screen)

    def show_signup(self):
        self.background.set_header_mode("auth")
        self.stack.setCurrentWidget(self.signup_screen)

    def show_risk_input(self):
        self.background.set_header_mode("evaluation")
        self.stack.setCurrentWidget(self.risk_input_screen)

    def show_result(self):
        self.background.set_header_mode("auth")
        self.stack.setCurrentWidget(self.result_screen)