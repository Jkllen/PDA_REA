from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QCheckBox,
    QMessageBox,
    QPushButton,
)
from PyQt6.QtCore import pyqtSignal, Qt
from view.qt.ui_parts import CardFrame


class OnboardingScreen(QWidget):
    proceed_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.awareness_checks: list[QCheckBox] = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(18)

        intro_text = QLabel(
            "By continuing, you confirm that you are aware of your current driving-related conditions and are\n"
            "prepared to provide accurate and honest inputs for this evaluation.\n\n"
            "Under Republic Act No. 4136, drivers are required to exercise proper care and responsibility.\n"
            "This assessment supports that responsibility and relies on truthful information."
        )
        intro_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro_text.setStyleSheet(
            "font-size: 16px; color: #1B1B1B; font-style: italic; line-height: 1.45;"
        )
        layout.addWidget(intro_text)

        panel = CardFrame()
        panel.setStyleSheet(
            """
            QFrame#cardFrame {
                background: rgba(255, 255, 255, 0.82);
                border: 2px solid #DBD6D6;
                border-radius: 28px;
            }
            """
        )
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 18, 24, 16)
        panel_layout.setSpacing(12)

        header = QLabel("You acknowledge that you are aware of the following")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 20px; font-style: italic; color: #111;")
        panel_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            """
            QScrollArea { border: none; background: transparent; }
            QScrollArea > QWidget > QWidget { background: transparent; }
            QScrollBar:vertical {
                background: #ECECEC; width: 10px; border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0; border-radius: 5px; min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            """
        )
        scroll.setFixedHeight(320)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0,0,0,0)
        body_layout.setSpacing(12)

        acknowledgement_items = [
            (
                "Your Physical and Mental Condition",
                "You are aware of your current state such as alertness, fatigue, or any influence of alcohol or substances.",
            ),
            (
                "Your Driving Behavior and Habits",
                "You understand your typical driving behavior, including speed, focus, and possible distractions.",
            ),
            (
                "Your Vehicle Condition",
                "You are aware of your vehicle's condition, including brakes, lights, tires, and overall roadworthiness.",
            ),
            (
                "Your Route and Environment",
                "You have knowledge of your planned route, traffic situation, weather conditions, and potential road hazards.",
            ),
            (
                "Your Legal Responsibility as a Driver",
                "You understand that reckless or negligent driving is punishable under Republic Act No. 4136 and that you are responsible for ensuring your fitness to drive.",
            ),
        ]

        for title, subtitle in acknowledgement_items:
            item_row = QWidget()
            item_layout = QHBoxLayout(item_row)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(14)
            item_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            checkbox = QCheckBox()
            checkbox.setStyleSheet("""
                QCheckBox {
                    spacing: 0px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
            self.awareness_checks.append(checkbox)

            text_col = QVBoxLayout()
            text_col.setContentsMargins(0, 0, 0, 0)
            text_col.setSpacing(4)

            title_lbl = QLabel(title)
            title_lbl.setWordWrap(True)
            title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #111;")

            subtitle_lbl = QLabel(subtitle)
            subtitle_lbl.setWordWrap(True)
            subtitle_lbl.setStyleSheet("font-size: 14px; color: #6B5A44; font-style: italic;")

            text_col.addWidget(title_lbl)
            text_col.addWidget(subtitle_lbl)

            item_layout.addWidget(checkbox, 0, Qt.AlignmentFlag.AlignTop)
            item_layout.addLayout(text_col, 1)

            body_layout.addWidget(item_row)

        body_layout.addStretch()
        scroll.setWidget(body)
        panel_layout.addWidget(scroll)
        layout.addWidget(panel)
        layout.addStretch()

        button_row = QHBoxLayout()
        logout_btn = self._dark_button("Logout")
        logout_btn.setMinimumWidth(115)
        logout_btn.clicked.connect(self._confirm_logout)
    
        self.start_button = self._green_button("START THE EVALUATION")
        
        self.start_button.setMinimumWidth(360)
        self.start_button.clicked.connect(self._handle_start)
        button_row.addWidget(logout_btn)
        button_row.addStretch()
        button_row.addWidget(self.start_button)
        layout.addLayout(button_row)

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
            QPushButton:hover {
                background: #5A5A5E;
            }
        """)
        return btn

    def _green_button(self, text: str):
        from PyQt6.QtWidgets import QPushButton

        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(54)
        btn.setStyleSheet(
            """
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
            """
        )
        return btn

    def _handle_start(self):
        items = [
            ("your physical and mental condition", self.awareness_checks[0]),
            ("your driving behavior and habits", self.awareness_checks[1]),
            ("your vehicle condition", self.awareness_checks[2]),
            ("your route and environment", self.awareness_checks[3]),
            ("your legal responsibility as a driver", self.awareness_checks[4]),
        ]

        unchecked = [label for label, box in items if not box.isChecked()]

        if unchecked:
            if len(unchecked) == 1:
                missing_text = unchecked[0]
            elif len(unchecked) == 2:
                missing_text = f"{unchecked[0]} and {unchecked[1]}"
            else:
                missing_text = ", ".join(unchecked[:-1]) + f", and {unchecked[-1]}"

            QMessageBox.warning(
                self,
                "Confirmation Required",
                f"Please confirm that you are aware of {missing_text}. "
                "Responsible driving behavior is expected under Republic Act No. 4136.",
            )
            return

        self.proceed_requested.emit()
    
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
        for box in self.awareness_checks:
            box.setChecked(False)
