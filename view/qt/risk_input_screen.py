from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QSizePolicy,
    QScrollArea,
)
from PyQt6.QtCore import pyqtSignal, Qt
from view.qt.ui_parts import CardFrame


class RiskInputScreen(QWidget):
    evaluate_requested = pyqtSignal(dict)
    back_to_login_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_y = 210
        card_w = min(1183, self.width() - 60)
        card_h = min(678, self.height() - top_y - 40)

        card_w = max(820, card_w)
        card_h = max(430, card_h)

        x = (self.width() - card_w) // 2
        self.card.setGeometry(x, top_y, card_w, card_h)

    def _build_ui(self):
        self.card = CardFrame(self)

        outer_layout = QVBoxLayout(self.card)
        outer_layout.setContentsMargins(34, 28, 34, 28)
        outer_layout.setSpacing(18)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(0)
        
        content_row = QHBoxLayout()
        content_row.setSpacing(32)

        left_col = QVBoxLayout()
        right_col = QVBoxLayout()
        left_col.setSpacing(12)
        right_col.setSpacing(12)
        
        left_col.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_col.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.driver_age = self._spin_row(left_col, "👤", "Driver Age", 18, 70, 30, "What is the age of the person driving in Years?")
        self.driver_experience = self._spin_row(left_col, "🪪", "Driver Experience", 0, 50, 5, "How long has the person been driving in Years?")
        self.driver_alcohol = self._double_row(left_col, "🍺", "Alcohol Level", 0.0, 1.0, 0.0, 1, "Alcohol level of the person before driving. Meaning of (0-1) values not yet known")
        self.lighting = self._combo_row(
            left_col,
            "💡",
            "Lighting Condition",
            ["daylight", "dusk", "darkness-light lit", "darkness"],
            "How bright is the road you are driving in?"
        )
        self.road_condition = self._combo_row(
            left_col,
            "🚧",
            "Road Condition",
            ["dry", "damp", "wet", "flood"],
            "What is the state of the road you will be driving on"        
        )
        self.road_type = self._combo_row(
            left_col,
            "🛣️",
            "Road Infrastructure",
            ["city road", "rural road", "highway", "mountain road"],
            "What type of road will you be driving on?"
        )
        self.weather = self._combo_row(
            right_col,
            "☁️",
            "Weather Condition",
            ["clear", "windy", "fog", "rain"],
            "What is the current weather before you drive?"
        )
        self.traffic_density = self._combo_row(
            right_col,
            "🚗",
            "Traffic Density",
            ["0", "1", "2"],
            "How dense is the traffic on your travel?"
        )
        self.time_of_day = self._combo_row(
            right_col,
            "🕒",
            "Time Based Data",
            ["morning", "afternoon", "evening"],
            "What part of the day will you be driving?"
        )
        self.vehicle_age = self._spin_row(right_col, "🔧", "Vehicle Age", 0, 21, 5, "How old is the vehicle you are driving in Years")
        self.failure_history = self._combo_row(
            right_col,
            "⚠️",
            "Failure History",
            ["no", "yes", "unknown"],
            "Has the vehicle you will be driving had any recent or common failures"
        )
        self.brake_condition = self._combo_row(
            right_col,
            "🔩",
            "Brake Condition",
            ["good", "fair", "poor"],
            "Is your vehicle's breaks functional"
        )
        self.vehicle_type = self._combo_row(
            right_col,
            "🚙",
            "Vehicle Type",
            ["car", "van", "bus", "truck", "motorcycle"],
            "What kind of vehicle will you be driving?"
        ) 
        self.road_defect = self._combo_row(
            right_col,
            "🕳️",
            "Road Defect",
            ["no defects", "worn surface", "ruts/holes"],
            "Does the road you will be driving on have any defects?"
        )
        self.intersection_related = self._combo_row(
            left_col,
            "➕",
            "Intersection",
            ["no intersection", "at intersection"],
            "Will you be driving in an intersection during your trip?"
        )
        self.speed_limit = self._spin_row(
            left_col,
            "🚦",
            "Speed Limit(KMph)",
            30, 213, 60,
            "What is the road's speed limit in KM/h"
        )
        left_col.addStretch()
        right_col.addStretch()
        
        content_row.addLayout(left_col, 1)
        content_row.addLayout(right_col, 1)
        
        scroll_layout.addLayout(content_row)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_container)
        outer_layout.addWidget(scroll, 1)

        button_row = QHBoxLayout()
        button_row.addStretch()

        self.evaluate_btn = QPushButton("Evaluate Driving Risk")
        self.evaluate_btn.setFixedHeight(64)
        self.evaluate_btn.setMinimumWidth(320)
        self.evaluate_btn.setMaximumWidth(420)
        self.evaluate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.evaluate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FCCC74,
                    stop:1 #F3BC23
                );
                color: white;
                font-size: 20px;
                font-weight: 500;
                letter-spacing: 3px;
                border: none;
                border-radius: 20px;
                padding: 0 24px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FFD283,
                    stop:1 #F5C53B
                );
            }
        """)
        self.evaluate_btn.clicked.connect(self._emit_data)

        button_row.addWidget(self.evaluate_btn)
        button_row.addStretch()
        outer_layout.addLayout(button_row)

    def _make_row_container(self, icon_text: str, label_text: str, labelToolTip: str):
        row = QWidget()
        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(5)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(8)

        icon = QLabel(icon_text)
        icon.setStyleSheet("""
            QLabel {
                font-size: 22px;
                color: #0A7D8C;
            }
        """)

        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 18px;
                font-weight: 700;
            }
        """)
        label.setToolTip(labelToolTip)

        header.addWidget(icon)
        header.addWidget(label)
        header.addStretch()

        row_layout.addLayout(header)
        return row, row_layout

    def _style_combo(self, combo: QComboBox):
        combo.setMinimumHeight(50)
        combo.setMaximumHeight(50)
        combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        combo.setStyleSheet("""
            QComboBox {
                background: white;
                border: 1px solid #AFAFAF;
                border-radius: 18px;
                padding: 0 16px;
                font-size: 16px;
                color: #434343;
            }
            QComboBox::drop-down {
                border: none;
                width: 34px;
            }
            QComboBox QAbstractItemView {
                background: white;
                color: #222222;
                border: 1px solid #AFAFAF;
                selection-background-color: #F3BC23;
                selection-color: black;
                padding: 4px;
                outline: 0;
        }
        """)

    def _style_spin(self, widget):
        widget.setMinimumHeight(50)
        widget.setMaximumHeight(50)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        widget.setStyleSheet("""
            QSpinBox, QDoubleSpinBox {
                background: white;
                border: 1px solid #AFAFAF;
                border-radius: 18px;
                padding: 0 16px;
                font-size: 16px;
                color: #434343;
            }
        """)

    def _combo_row(self, parent_layout, icon_text, label_text, items, toolTipLabel):
        row, row_layout = self._make_row_container(icon_text, label_text, toolTipLabel)
        combo = QComboBox()
        combo.addItems(items)
        combo.setToolTip(toolTipLabel)
        self._style_combo(combo)
        row_layout.addWidget(combo)
        parent_layout.addWidget(row)
        return combo

    def _spin_row(self, parent_layout, icon_text, label_text, min_val, max_val, default, labelToolTip):
        row, row_layout = self._make_row_container(icon_text, label_text, labelToolTip)
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        self._style_spin(spin)
        row_layout.addWidget(spin)
        parent_layout.addWidget(row)
        return spin

    def _double_row(self, parent_layout, icon_text, label_text, min_val, max_val, default, decimals, toolTipLabel):
        row, row_layout = self._make_row_container(icon_text, label_text, toolTipLabel)
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setDecimals(decimals)
        spin.setSingleStep(0.1)
        spin.setToolTip(toolTipLabel)
        self._style_spin(spin)
        row_layout.addWidget(spin)
        parent_layout.addWidget(row)
        return spin

    def _emit_data(self):
        failure_map = {
            "no": 0.0,
            "yes": 1.0,
            "unknown": 0.5,
        }

        inputs = {
            "driver_age": int(self.driver_age.value()),
            "driver_experience": int(self.driver_experience.value()),
            "driver_alcohol": float(self.driver_alcohol.value()),
            "traffic_density": int(self.traffic_density.currentText()),
            "vehicle_age": int(self.vehicle_age.value()),
            "failure_history": failure_map[self.failure_history.currentText()],
            "brake_condition": self.brake_condition.currentText(),
            "weather": self.weather.currentText(),
            "lighting": self.lighting.currentText(),
            "road_condition": self.road_condition.currentText(),
            "time_of_day": self.time_of_day.currentText(),
            "road_type": self.road_type.currentText(),
            "vehicle_type": self.vehicle_type.currentText(),
            "road_defect": self.road_defect.currentText(),
            "intersection": self.intersection_related.currentText(),
            "speed_limit": int(self.speed_limit.value()),
        }
            
        self.evaluate_requested.emit(inputs)

    def clear_form(self):
        self.driver_age.setValue(30)
        self.driver_experience.setValue(5)
        self.driver_alcohol.setValue(0.0)
        self.lighting.setCurrentIndex(0)
        self.road_condition.setCurrentIndex(0)
        self.road_type.setCurrentIndex(0)
        self.weather.setCurrentIndex(0)
        self.traffic_density.setCurrentIndex(0)
        self.time_of_day.setCurrentIndex(0)
        self.vehicle_age.setValue(5)
        self.failure_history.setCurrentIndex(0)
        self.brake_condition.setCurrentIndex(0)