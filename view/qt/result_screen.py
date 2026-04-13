from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import pyqtSignal, Qt
from view.qt.ui_parts import CardFrame, PrimaryButton, BROWN


class ResultScreen(QWidget):
    back_requested = pyqtSignal()
    encrypt_requested = pyqtSignal()
    decrypt_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_margin = 190
        available_w = self.width() - 70
        available_h = self.height() - top_margin - 35

        card_w = max(760, min(1000, available_w))
        card_h = max(420, min(680, available_h))

        x = (self.width() - card_w) // 2
        y = max(top_margin, (self.height() - card_h) // 2)
        self.card.setGeometry(x, y, card_w, card_h)

        title_size = max(24, min(32, self.width() // 40))
        risk_size = max(16, min(20, self.width() // 65))
        score_size = max(15, min(18, self.width() // 72))

        self.title.setStyleSheet(f"color: {BROWN}; font-size: {title_size}px; font-weight: 700;")
        self.risk_label.setStyleSheet(f"font-size: {risk_size}px; font-weight: 600; color: #222;")
        self.score_label.setStyleSheet(f"font-size: {score_size}px; font-weight: 500; color: #333;")

    def _build_ui(self):
        self.card = CardFrame(self)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)

        self.title = QLabel("Evaluation Result")
        layout.addWidget(self.title)

        self.risk_label = QLabel("Risk Level: -")
        layout.addWidget(self.risk_label)

        self.score_label = QLabel("Risk Score: -")
        layout.addWidget(self.score_label)

        self.report_box = QTextEdit()
        self.report_box.setReadOnly(True)
        self.report_box.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 1px solid #D5D5D5;
                border-radius: 16px;
                padding: 12px;
                font-size: 14px;
                color: #222;
            }
        """)
        layout.addWidget(self.report_box, 1)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_requested.emit)

        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_requested.emit)

        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_requested.emit)

        self.new_eval_button = PrimaryButton("New Evaluation")
        self.new_eval_button.clicked.connect(self.back_requested.emit)

        for btn in (self.back_button, self.encrypt_button, self.decrypt_button):
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background: #353434;
                    color: white;
                    border: none;
                    border-radius: 14px;
                    font-size: 16px;
                    font-weight: 600;
                    padding: 0 18px;
                }
            """)
            button_row.addWidget(btn)

        button_row.addStretch()
        button_row.addWidget(self.new_eval_button)

        layout.addLayout(button_row)

    def set_result(self, report: str, risk_level: str, score: float):
        self.risk_label.setText(f"Risk Level: {risk_level}")
        self.score_label.setText(f"Risk Score: {score:.2f}")
        self.report_box.setPlainText(report)

    def set_decrypted_report(self, report: str):
        self.report_box.setPlainText(report)

    def clear_result(self):
        self.risk_label.setText("Risk Level: -")
        self.score_label.setText("Risk Score: -")
        self.report_box.clear()