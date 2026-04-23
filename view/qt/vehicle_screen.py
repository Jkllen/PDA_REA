import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt

from view.qt.ui_parts import CardFrame


class VehicleScreen(QWidget):
    back_requested = pyqtSignal()
    evaluate_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(18)

        section = self._wide_section_card(
            "VEHICLE CONDITION",
            "Vehicle condition is also important, check your vehicle before you start."
            )
        section_layout = section.layout()
        form_row = QHBoxLayout()
        form_row.setSpacing(25)

        left = QVBoxLayout()
        left.setSpacing(10)
        right = QVBoxLayout()
        right.setSpacing(10)

        self.vehicle_type = self._combo_field(
            left,
            "What type of vehicle will you use?",
            [
                "Motorcycle",
                "Sedan / Car",
                "SUV / Van",
                "Pickup Truck",
            ],
            placeholder="Select vehicle type",
        )
        self.vehicle_age = self._combo_field(
            left,
            "How old is your vehicle (months/years)?",
            [
                "Less than 1 year",
                "1-3 years",
                "4-6 years",
                "7-10 years",
                "More than 10 years",
            ],
            placeholder="Select vehicle age",
        )
        self.maintenance_recency = self._combo_field(
            left,
            "How recently was your vehicle inspected or maintained?",
            [
                "Within last month",
                "1-3 months ago",
                "4-6 months ago",
                "More than 6 months ago",
                "Cannot remember",
            ],
            placeholder="Select last vehicle maintenance",
        )

        self.failure_history = self._combo_field(
            right,
            "Has your vehicle experienced any recent mechanical issues?",
            [
                "None",
                "Minor issues (not affecting driving)",
                "Moderate issues (needs attention)",
                "Major issues (affects safety)",
                "Not sure",
            ],
            placeholder="Select condition",
        )
        self.brake_condition = self._combo_field(
            right,
            "How would you describe your brake condition?",
            [
                "Very responsive",
                "Slight delay",
                "Noticeable delay",
                "Weak / unreliable",
                "Not sure",
            ],
            placeholder="Select condition",
        )

        form_row.addLayout(left, 1)
        form_row.addLayout(right, 1)
        section_layout.addLayout(form_row)
        page_layout.addWidget(section, 0, Qt.AlignmentFlag.AlignTop)

        button_row = QHBoxLayout()

        logout_btn = self._dark_button("Logout")
        logout_btn.setMinimumWidth(115)
        logout_btn.clicked.connect(self._confirm_logout)

        back_btn = self._dark_button("Back")
        back_btn.setMinimumWidth(115)
        back_btn.clicked.connect(self.back_requested.emit)

        run_btn = self._green_button("Next")
        run_btn.setMinimumWidth(115)
        run_btn.clicked.connect(self.evaluate_requested.emit)

        button_row.addWidget(logout_btn)
        button_row.addStretch()
        button_row.addWidget(back_btn)
        button_row.addWidget(run_btn)

        page_layout.addLayout(button_row)

    def _wide_section_card(self, title: str, subtitle: str) -> CardFrame:
        card = CardFrame()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(36, 20, 36, 22)
        layout.setSpacing(14)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_vehicle = QLabel()
        icon_vehicle.setPixmap(qta.icon("fa5s.car-side", color="#4E7F2A").pixmap(34, 34))

        header = QLabel(title)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 21px; font-weight: 800; color: #111;")

        header_row.addWidget(icon_vehicle)
        header_row.addWidget(header)
 
        layout.addSpacing(4)
        layout.addLayout(header_row)
        
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_lbl.setWordWrap(True)
        subtitle_lbl.setStyleSheet("""
            font-size: 14px;
            color: #3F8A2E;
            padding-bottom: 2px;
        """)
        layout.addWidget(subtitle_lbl)

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
                padding: 0 42px 0 18px;
                font-size: 15px;
                color: #333;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 36px;
                border: none;
                padding-right: 12px;
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
                padding: 4px;
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
                background: #3D7600;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: 800;
                padding: 0 24px;
            }
            QPushButton:hover { background: #4A8B07; }
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
        self.vehicle_type.setCurrentIndex(0)
        self.vehicle_age.setCurrentIndex(0)
        self.maintenance_recency.setCurrentIndex(0)
        self.failure_history.setCurrentIndex(0)
        self.brake_condition.setCurrentIndex(0)