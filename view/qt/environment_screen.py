import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from view.qt.ui_parts import CardFrame


class EnvironmentScreen(QWidget):
    back_requested = pyqtSignal()
    next_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(14)

        section = self._wide_section_card(
            "WEATHER, ROAD, & ENVIRONMENT CONDITION",
            "Weather, road, and environment condition are also important, check updates using weather applications and navigation apps before driving."
            )
        section_layout = section.layout()

        form_row = QHBoxLayout()
        form_row.setSpacing(24)

        left = QVBoxLayout()
        left.setSpacing(10)
        left.setAlignment(Qt.AlignmentFlag.AlignTop)

        right = QVBoxLayout()
        right.setSpacing(10)
        right.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.weather = self._combo_field(
            left,
            "What is the expected weather condition based on forecast?",
            [
                "Clear / Sunny",
                "Cloudy / Overcast",
                "Light Rain",
                "Heavy Rain",
                "Storm / Typhoon",
                "Fog / Low Visibility",
            ],
            placeholder="Select current weather condition",
        )
        self.weather.currentIndexChanged.connect(self._update_road_condition_options)
        
        self.road_type = self._combo_field(
            left,
            "What type of road will you mostly be driving on?",
            [
                "Highway / Expressway",
                "Main Road / City Road",
                "Residential Area",
                "Rural / Provincial Road",
                "Mountain / Curved Road",
            ],
            placeholder="Select road type",
        )
        self.road_condition = self._combo_field(
            left,
            "What is the current road condition?",
            [
                "Dry and clear",
                "Wet / Slippery",
                "Muddy",
                "Flooded",
                "Damaged / Uneven",
            ],
            placeholder="Select road condition",
        )

        self.road_defect = self._combo_field(
            right,
            "Are there any visible road issues along your planned route?",
            [
                "None",
                "Potholes / Uneven road",
                "Flooding",
                "Road construction",
                "Accidents / Obstructions",
                "Poor lighting",
                "Not sure",
            ],
            placeholder="Select possible visible road issues",
        )
        self.traffic_density = self._combo_field(
            right,
            "What is the expected traffic level?",
            [
                "Light (free-flowing)",
                "Moderate",
                "Heavy (slow-moving)",
                "Severe congestion / Standstill",
            ],
            placeholder="Select expected traffic level",
        )
        self.intersection_related = self._combo_field(
            right,
            "Will your route include intersections or busy crossings?",
            [
                "No",
                "Yes - Few",
                "Yes - Many",
                "Not sure",
            ],
            placeholder="Select",
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

        next_btn = self._green_button("RUN SAFETY ASSESSMENT")
        next_btn.setMinimumWidth(320)
        next_btn.clicked.connect(self.next_requested.emit)

        button_row.addWidget(logout_btn)
        button_row.addStretch()
        button_row.addWidget(back_btn)
        button_row.addWidget(next_btn)

        page_layout.addLayout(button_row)
        
        self._update_road_condition_options()

    def _wide_section_card(self, title: str, subtitle: str) -> CardFrame:
        card = CardFrame()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(36, 20, 36, 22)
        layout.setSpacing(14)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_weather = QLabel()
        icon_weather.setPixmap(qta.icon("fa5s.cloud-sun", color="#4E7F2A").pixmap(34, 34))

        icon_road = QLabel()
        icon_road.setPixmap(qta.icon("fa5s.road", color="#4E7F2A").pixmap(34, 34))

        header = QLabel(title)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 21px; font-weight: 800; color: #111;")

        header_row.addWidget(icon_weather)
        header_row.addWidget(icon_road)
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

    def _update_road_condition_options(self):
        weather = self.weather.currentText().strip().lower()
        dry_text = "Dry and clear"

        model = self.road_condition.model()

        rainy_or_low_visibility = {
            "light rain",
            "heavy rain",
            "storm / typhoon",
            "fog / low visibility",
        }

        for i in range(self.road_condition.count()):
            text = self.road_condition.itemText(i)

            if text.lower() == dry_text.lower():
                item = model.item(i)
                if item is not None:
                    should_disable = weather in rainy_or_low_visibility
                    item.setEnabled(not should_disable)

                    # if user already selected dry and clear, force reset
                    if should_disable and self.road_condition.currentText().lower() == dry_text.lower():
                        self.road_condition.setCurrentIndex(0)

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
        self.weather.setCurrentIndex(0)
        self.road_type.setCurrentIndex(0)
        self.road_condition.setCurrentIndex(0)
        self.road_defect.setCurrentIndex(0)
        self.traffic_density.setCurrentIndex(0)
        self.intersection_related.setCurrentIndex(0)