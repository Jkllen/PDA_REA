from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from view.qt.ui_parts import CardFrame, StyledLineEdit, PrimaryButton, LinkLabel, BROWN


class SignupScreen(QWidget):
    signup_requested = pyqtSignal(str, str, str)
    login_link_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_margin = 175
        available_w = self.width() - 80
        available_h = self.height() - top_margin - 70

        card_w = max(400, min(532, available_w))
        card_h = max(500, min(678, available_h))

        x = (self.width() - card_w) // 2
        y = max(top_margin, (self.height() - card_h) // 2)
        self.card.setGeometry(x, y, card_w, card_h)

        title_size = max(26, min(36, self.width() // 35))
        label_size = max(16, min(24, self.width() // 55))
        link_size = max(14, min(20, self.width() // 65))

        self.title.setStyleSheet(f"color: {BROWN}; font-size: {title_size}px; font-weight: 700;")
        for lbl in (self.client_label, self.password_label, self.confirm_label):
            lbl.setStyleSheet(f"color: {BROWN}; font-size: {label_size}px; font-weight: 500;")
        self.login_link.setStyleSheet(f"color: #0F3362; font-size: {link_size}px; font-weight: 500;")

    def _build_ui(self):
        self.card = CardFrame(self)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(42, 26, 42, 28)
        layout.setSpacing(10)

        self.title = QLabel("Sign Up")
        layout.addWidget(self.title)

        layout.addSpacing(8)

        self.client_label = QLabel("Client Number")
        layout.addWidget(self.client_label)

        self.client_input = StyledLineEdit("Enter your client number", icon = "fa5s.user")
        layout.addWidget(self.client_input)

        self.password_label = QLabel("Password")
        layout.addWidget(self.password_label)

        self.password_input = StyledLineEdit("Enter your password", icon = "fa5s.lock", password=True)
        layout.addWidget(self.password_input)

        self.confirm_label = QLabel("Confirm Password")
        layout.addWidget(self.confirm_label)

        self.confirm_input = StyledLineEdit("Confirm your password", icon = "fa5s.lock", password=True)
        layout.addWidget(self.confirm_input)

        layout.addSpacing(10)

        self.signup_button = PrimaryButton("Create Account")
        self.signup_button.clicked.connect(self._emit_signup)
        layout.addWidget(self.signup_button)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()

        self.login_link = LinkLabel("Already have an account? Login")
        self.login_link.clicked.connect(self.login_link_clicked.emit)
        bottom_row.addWidget(self.login_link)

        bottom_row.addStretch()
        layout.addLayout(bottom_row)

        layout.addStretch()

    def _emit_signup(self):
        self.signup_requested.emit(
            self.client_input.text().strip(),
            self.password_input.text(),
            self.confirm_input.text(),
        )