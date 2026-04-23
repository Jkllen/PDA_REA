import qtawesome as qta

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLineEdit
)
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt

from view.qt.ui_parts import CardFrame


class DriverTripScreen(QWidget):
    next_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(18)

        content_row = QHBoxLayout()
        content_row.setSpacing(28)

        driver_card = self._section_card("DRIVER CONDITION", "fa6s.person-rays")
        driver_layout = driver_card.layout()

        self.driver_age = self._line_field(
            driver_layout,
            "What is your age (in years)?",
            "e.g. 35",
        )

        self.driver_alcohol = self._combo_field(
            driver_layout,
            "Have you consumed any alcohol in the past few hours before planned to drive?",
            [
                "None",
                "1 drink (light)",
                "2-3 drinks (moderate)",
                "More than 3 drinks (high)",
                "Prefer not to say",
            ],
            placeholder="Select",
        )

        self.driver_experience = self._combo_field(
            driver_layout,
            "How many years of driving experience do you have?",
            [
                "Less than 1 year",
                "1-3 years",
                "4-6 years",
                "7-10 years",
                "More than 10 years",
            ],
            placeholder="Select driving experience",
        )

        driver_layout.addStretch()

        trip_card = self._section_card("TRIP & TIME CONDITIONS", "fa5s.clock")
        trip_layout = trip_card.layout()

        self.time_of_day = self._combo_field(
            trip_layout,
            "What time of day are you planning to drive?",
            [
                "Early Morning (12 AM - 5 AM)",
                "Morning (6 AM - 11 AM)",
                "Afternoon (12 PM - 5 PM)",
                "Evening (6 PM - 9 PM)",
                "Late Night (10 PM - 11 PM)",
            ],
            placeholder="Select the time of the day",
        )

        self.trip_duration = self._combo_field(
            trip_layout,
            "How long do you expect your trip to take?",
            [
                "Less than 15 minutes",
                "15-30 minutes",
                "30-60 minutes",
                "1-2 hours",
                "More than 2 hours",
            ],
            placeholder="Select expected trip time",
        )

        trip_layout.addStretch()

        content_row.addWidget(driver_card, 1)
        content_row.addWidget(trip_card, 1)
        page_layout.addLayout(content_row, 1)

        button_row = QHBoxLayout()

        logout_btn = self._dark_button("Logout")
        logout_btn.setMinimumWidth(115)
        logout_btn.clicked.connect(self._confirm_logout)

        next_btn = self._green_button("Next")
        next_btn.setMinimumWidth(115)
        next_btn.clicked.connect(self.next_requested.emit)

        button_row.addWidget(logout_btn)
        button_row.addStretch()
        button_row.addWidget(next_btn)

        page_layout.addLayout(button_row)

    def _section_card(self, title: str, icon_name: str) -> CardFrame:
        card = CardFrame()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 20, 28, 22)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setSpacing(10)
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color="#4E7F2A").pixmap(30, 30))

        header = QLabel(title)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            font-size: 21px;
            font-weight: 800;
            color: #111;
        """)

        header_row.addWidget(icon)
        header_row.addWidget(header)

        layout.addLayout(header_row)

        return card

    def _field_shell(self, label_text: str):
        shell = QWidget()
        layout = QVBoxLayout(shell)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel(label_text)
        label.setWordWrap(True)
        label.setStyleSheet("font-size: 17px; color: #111;")
        layout.addWidget(label)

        return shell, layout

    def _style_combo(self, combo: QComboBox):
        combo.setMinimumHeight(50)
        combo.setStyleSheet("""
            QComboBox {
                background: #F3F3F3;
                border: 1px solid #111;
                border-radius: 24px;
                padding: 0 36px 0 18px;
                font-size: 15px;
                color: #333;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 32px;
                border: none;
            }

            QComboBox::down-arrow {
                image: url(assets/icons/arrow-down.png);
                width: 18px;
                height: 18px;
                padding-right: 10px;
            }

            QComboBox QAbstractItemView {
                background: white;
                color: #222;
                border: 1px solid #BDBDBD;
                selection-background-color: #D8F2D1;
                selection-color: black;
            }
        """)

    def _style_line(self, line: QLineEdit):
        line.setMinimumHeight(50)
        line.setStyleSheet("""
            QLineEdit {
                background: #F3F3F3;
                border: 1px solid #111;
                border-radius: 24px;
                padding: 0 18px;
                font-size: 15px;
                color: #333;
            }
        """)

    def _combo_field(self, parent_layout, label_text: str, items: list[str], placeholder: str = "Select") -> QComboBox:
        shell, layout = self._field_shell(label_text)
        combo = QComboBox()
        combo.addItem(placeholder)
        combo.addItems(items)
        combo.setCurrentIndex(0)
        self._style_combo(combo)
        layout.addWidget(combo)
        parent_layout.addWidget(shell)
        return combo

    def _line_field(self, parent_layout, label_text: str, placeholder: str) -> QLineEdit:
        shell, layout = self._field_shell(label_text)
        line = QLineEdit()
        line.setPlaceholderText(placeholder)
        self._style_line(line)
        layout.addWidget(line)
        parent_layout.addWidget(shell)
        return line

    def _dark_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(54)
        btn.setStyleSheet("""
            QPushButton {
                background: #4A4A4D;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: 700;
                padding: 0 22px;
            }
            QPushButton:hover { background: #5A5A5E; }
        """)
        return btn

    def _green_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(54)
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2CBF3A,
                    stop:1 #1E8F2A
                );
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 15px;
                font-weight: 500;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #35D645,
                    stop:1 #24A833
                );
            }
        """)
        return btn

    def _confirm_logout(self):
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to log out?\n\nAny unsaved progress will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
            
    def reset(self):
        self.driver_age.clear()
        self.driver_alcohol.setCurrentIndex(0)
        self.driver_experience.setCurrentIndex(0)
        self.time_of_day.setCurrentIndex(0)
        self.trip_duration.setCurrentIndex(0)