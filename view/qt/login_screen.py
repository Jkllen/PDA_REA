from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from view.qt.ui_parts import CardFrame, StyledLineEdit, PrimaryButton, LinkLabel, BROWN


class LoginScreen(QWidget):
    login_requested = pyqtSignal(str, str)
    signup_link_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_margin = 175
        available_w = self.width() - 80
        available_h = self.height() - top_margin - 70

        card_w = max(380, min(532, available_w))
        card_h = max(420, min(549, available_h))

        x = (self.width() - card_w) // 2
        y = max(top_margin, (self.height() - card_h) // 2)
        self.card.setGeometry(x, y, card_w, card_h)

        title_size = max(26, min(36, self.width() // 35))
        label_size = max(16, min(24, self.width() // 55))
        link_size = max(14, min(20, self.width() // 65))

        self.title.setStyleSheet(f"color: {BROWN}; font-size: {title_size}px; font-weight: 700;")
        self.client_label.setStyleSheet(f"color: {BROWN}; font-size: {label_size}px; font-weight: 500;")
        self.password_label.setStyleSheet(f"color: {BROWN}; font-size: {label_size}px; font-weight: 500;")
        self.signup_link.setStyleSheet(f"color: #0F3362; font-size: {link_size}px; font-weight: 500;")

    def _build_ui(self):
        self.card = CardFrame(self)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(42, 26, 42, 30)
        layout.setSpacing(12)

        self.title = QLabel("Login")
        layout.addWidget(self.title)

        layout.addSpacing(10)

        self.client_label = QLabel("Client Number")
        layout.addWidget(self.client_label)

        self.client_input = StyledLineEdit("Enter your client number", icon = "fa5s.user")
        layout.addWidget(self.client_input)

        layout.addSpacing(4)

        self.password_label = QLabel("Password")
        layout.addWidget(self.password_label)

        self.password_input = StyledLineEdit("Enter your password", icon = "fa5s.lock", password=True)
        layout.addWidget(self.password_input)

        row = QHBoxLayout()
        row.addStretch()
        self.signup_link = LinkLabel("Sign up?")
        self.signup_link.clicked.connect(self.signup_link_clicked.emit)
        row.addWidget(self.signup_link)
        layout.addLayout(row)

        layout.addSpacing(10)

        self.login_button = PrimaryButton("Login")
        self.login_button.clicked.connect(self._emit_login)
        layout.addWidget(self.login_button)

        layout.addStretch()

    def _emit_login(self):
        self.login_requested.emit(
            self.client_input.text().strip(),
            self.password_input.text()
        )

    def set_client_number(self, client_number: str):
        self.client_input.setText(client_number)
        self.password_input.clear()