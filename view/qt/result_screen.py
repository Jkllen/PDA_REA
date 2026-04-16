from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QSizePolicy,
    QScrollArea,
)
from PyQt6.QtCore import pyqtSignal, Qt, QRectF
from PyQt6.QtGui import QPainter, QColor
import qtawesome as qta

from view.qt.ui_parts import CardFrame, BROWN


LOW_COLOR = "#059A1C"
MEDIUM_COLOR = "#8D8D01"
HIGH_COLOR = "#FF0000"

DIM_GREEN = "#1F7A2A"
DIM_YELLOW = "#8A8115"
DIM_RED = "#972414"

ORANGE = "#F28C13"
DARK_BUTTON = "#343438"
GREEN_BUTTON = "#22952E"
YELLOW_BUTTON = "#F0BF2C"


class TrafficLightWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_level = "-"
        self.setMinimumSize(360, 120)
        self.setMaximumHeight(130)

    def set_level(self, risk_level: str):
        self.current_level = risk_level
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        body_w = min(360, rect.width() - 8)
        body_h = min(108, rect.height() - 8)
        x = (rect.width() - body_w) / 2
        y = (rect.height() - body_h) / 2

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#1E1E22"))
        painter.drawRoundedRect(QRectF(x, y, body_w, body_h), 42, 42)

        circle_d = 74
        gap = 26
        total_w = circle_d * 3 + gap * 2
        start_x = x + (body_w - total_w) / 2
        cy = y + (body_h - circle_d) / 2

        green = DIM_GREEN
        yellow = DIM_YELLOW
        red = DIM_RED

        if self.current_level == "Low Risk":
            green = "#27E62F"
        elif self.current_level == "Medium Risk":
            yellow = "#F7E600"
        elif self.current_level == "High Risk":
            red = HIGH_COLOR

        colors = [green, yellow, red]
        for i, color in enumerate(colors):
            cx = start_x + i * (circle_d + gap)
            painter.setBrush(QColor(color))
            painter.drawEllipse(QRectF(cx, cy, circle_d, circle_d))


class ResultScreen(QWidget):
    back_requested = pyqtSignal()
    encrypt_requested = pyqtSignal()
    decrypt_requested = pyqtSignal()
    advisory_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_risk_level = "-"
        self.current_client_id = "-"
        self.current_inputs = {}
        self.current_reasons = []
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_margin = 205
        available_w = self.width() - 70
        available_h = self.height() - top_margin - 35

        card_w = max(1020, min(1180, available_w))
        card_h = max(460, min(500, available_h))

        x = (self.width() - card_w) // 2
        y = max(top_margin, (self.height() - card_h) // 2)
        self.card.setGeometry(x, y, card_w, card_h)
        
        light_w = 360
        light_h = 120
        light_x = (self.width() - light_w) // 2
        light_y = y + card_h + 1
        self.traffic_light.setGeometry(light_x, light_y, light_w, light_h)
        self.traffic_light.raise_()

    def _build_ui(self):
        self.card = CardFrame(self)
        
        self.traffic_light = TrafficLightWidget(self)
        self.traffic_light.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.traffic_light.raise_()

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(36, 20, 36, 16)
        layout.setSpacing(14)

        # ---------------- TOP HEADER ----------------
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        left_top = QVBoxLayout()
        left_top.setSpacing(8)

        title_row = QHBoxLayout()
        title_row.setSpacing(14)

        title_icon = QLabel()
        title_icon.setPixmap(qta.icon("fa5s.clipboard-check", color=ORANGE).pixmap(42, 42))
        self.title = QLabel("EVALUATION RESULT")
        self.title.setStyleSheet(f"color: {BROWN}; font-size: 28px; font-weight: 800;")

        title_row.addWidget(title_icon)
        title_row.addWidget(self.title)
        title_row.addStretch()
        left_top.addLayout(title_row)

        risk_row = QHBoxLayout()
        risk_row.setSpacing(8)

        self.risk_prefix = QLabel("Accident Risk Level:")
        self.risk_prefix.setStyleSheet("font-size: 24px; font-weight: 600; color: #111;")

        self.risk_value = QLabel("-")
        self.risk_value.setStyleSheet("font-size: 24px; font-weight: 500; color: #111;")

        risk_row.addWidget(self.risk_prefix)
        risk_row.addWidget(self.risk_value)
        risk_row.addStretch()
        left_top.addLayout(risk_row)

        top_row.addLayout(left_top, 1)

        right_top = QVBoxLayout()
        right_top.setSpacing(10)
        right_top.setAlignment(Qt.AlignmentFlag.AlignRight)

        client_row = QHBoxLayout()
        client_row.setAlignment(Qt.AlignmentFlag.AlignRight)
        client_icon = QLabel()
        client_icon.setPixmap(qta.icon("fa5s.user", color="#808080").pixmap(26, 26))
        self.client_label = QLabel("Client ID: -")
        self.client_label.setStyleSheet("font-size: 18px; color: #0A2AD5; font-weight: 500;")
        client_row.addWidget(client_icon)
        client_row.addWidget(self.client_label)

        self.score_label = QLabel("Evaluation Score: -")
        self.score_label.setStyleSheet("font-size: 18px; color: #111; font-weight: 600;")

        right_top.addLayout(client_row)
        right_top.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignRight)

        top_row.addLayout(right_top)
        layout.addLayout(top_row)

        hline = QFrame()
        hline.setFrameShape(QFrame.Shape.HLine)
        hline.setStyleSheet("background: #5F5F5F; min-height: 2px; max-height: 2px; border: none;")
        layout.addWidget(hline)

        # ---------------- MAIN CONTENT ----------------
        content_row = QHBoxLayout()
        content_row.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_row.setSpacing(18)

        # LEFT PANEL
        left_col = QVBoxLayout()
        left_col.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_col.setSpacing(14)

        input_title_row = QHBoxLayout()
        input_title_row.setSpacing(10)

        input_icon = QLabel()
        input_icon.setPixmap(qta.icon("fa5s.list", color=ORANGE).pixmap(28, 28))
        input_title = QLabel("INPUT SUMMARY")
        input_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #111;")

        input_title_row.addWidget(input_icon)
        input_title_row.addWidget(input_title)
        input_title_row.addStretch()
        left_col.addLayout(input_title_row)

        input_grid = QHBoxLayout()
        input_grid.setSpacing(34)

        self.left_inputs_box = QVBoxLayout()
        self.left_inputs_box.setSpacing(4)
        self.right_inputs_box = QVBoxLayout()
        self.right_inputs_box.setSpacing(4)

        self.input_labels = {}

        left_fields = [
            ("driver_age", "fa5s.user", "Driver Age"),
            ("driver_experience", "fa5s.star", "Driver Experience"),
            ("driver_alcohol", "fa5s.wine-bottle", "Alcohol Level"),
            ("traffic_density", "fa5s.car", "Traffic Density"),
            ("vehicle_age", "fa5s.calendar-alt", "Vehicle Age"),
            ("vehicle_type", "fa5s.car-side", "Vehicle Type"),
            ("failure_history", "fa5s.file-alt", "Failure History"),
            ("brake_condition", "fa5s.bullseye", "Brake Condition"),
        ]

        right_fields = [
            ("weather", "fa5s.cloud-rain", "Weather"),
            ("lighting", "fa5s.moon", "Lighting"),
            ("road_condition", "fa5s.road", "Road Condition"),
            ("time_of_day", "fa5s.sun", "Time of Day"),
            ("road_type", "fa5s.road", "Road Type"),
            ("road_defect", "fa5s.exclamation-triangle", "Road Defect"),
            ("intersection", "fa5s.hashtag", "Intersection"),
            ("speed_limit", "fa5s.tachometer-alt", "Speed Limit"),
        ]

        for key, icon_name, title in left_fields:
            row, value_lbl = self._make_field_row(icon_name, title)
            self.left_inputs_box.addWidget(row)
            self.input_labels[key] = value_lbl
            self.left_inputs_box.addStretch()

        for key, icon_name, title in right_fields:
            row, value_lbl = self._make_field_row(icon_name, title)
            self.right_inputs_box.addWidget(row)
            self.input_labels[key] = value_lbl
            self.right_inputs_box.addStretch()

        input_grid.addLayout(self.left_inputs_box)
        input_grid.addLayout(self.right_inputs_box)
        left_col.addLayout(input_grid)
        left_col.addStretch()

        content_row.addLayout(left_col, 1)

        vline = QFrame()
        vline.setFrameShape(QFrame.Shape.VLine)
        vline.setStyleSheet("background: #B8B8B8; min-width: 1px; max-width: 1px; border: none;")
        content_row.addWidget(vline)

        # RIGHT PANEL
        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_col.setSpacing(14)

        results_title_row = QHBoxLayout()
        results_title_row.setSpacing(10)

        results_icon = QLabel()
        results_icon.setPixmap(qta.icon("fa5s.signal", color=ORANGE).pixmap(28, 28))
        results_title = QLabel("RESULTS")
        results_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #111;")

        results_title_row.addWidget(results_icon)
        results_title_row.addWidget(results_title)
        results_title_row.addStretch()
        right_col.addLayout(results_title_row)

        self.casualties_row, self.casualties_text = self._make_simple_result_label(
            "fa5s.users", "Predicted Number of Casualties", "-"
        )
        self.crash_type_row, self.crash_type_text = self._make_simple_result_label(
            "fa5s.car-crash", "Predicted Crash Type", "-"
        )
        self.maintenance_row, self.maintenance_text = self._make_simple_result_label(
            "fa5s.wrench", "Predicted Maintenance Required", "-"
        )

        results_distribution_row = QHBoxLayout()
        results_distribution_row.setSpacing(30)

        results_left = QVBoxLayout()
        results_left.setSpacing(4)

        results_left.addWidget(self.casualties_row)
        results_left.addWidget(self.crash_type_row)
        results_left.addWidget(self.maintenance_row)

        distribution_right = QVBoxLayout()
        distribution_right.setSpacing(2)

        distribution_title = QLabel("RISK DISTRIBUTION")
        distribution_title.setStyleSheet("font-size: 17px; font-weight: 800; color: #111;")
        distribution_right.addWidget(distribution_title)

        self.low_distribution = QLabel("Low Risk: 0.00%")
        self.medium_distribution = QLabel("Medium Risk: 0.00%")
        self.high_distribution = QLabel("High Risk: 0.00%")

        self.low_distribution.setStyleSheet("font-size: 14px; color: #059A1C; font-weight: 600;")
        self.medium_distribution.setStyleSheet("font-size: 14px; color: #8D8D01; font-weight: 600;")
        self.high_distribution.setStyleSheet("font-size: 14px; color: #FF0000; font-weight: 600;")

        distribution_right.addWidget(self.low_distribution)
        distribution_right.addWidget(self.medium_distribution)
        distribution_right.addWidget(self.high_distribution)

        results_distribution_row.addLayout(results_left, 2)
        results_distribution_row.addLayout(distribution_right, 1)

        right_col.addLayout(results_distribution_row)


        reasons_title_row = QHBoxLayout()
        reasons_title_row.setSpacing(10)

        reasons_icon = QLabel()
        reasons_icon.setPixmap(qta.icon("fa5s.exclamation-circle", color=ORANGE).pixmap(28, 28))
        reasons_title = QLabel("REASONS")
        reasons_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #111;")

        reasons_title_row.addWidget(reasons_icon)
        reasons_title_row.addWidget(reasons_title)
        reasons_title_row.addStretch()
        right_col.addLayout(reasons_title_row)

        self.reasons_scroll = QScrollArea()
        self.reasons_scroll.setWidgetResizable(True)
        self.reasons_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.reasons_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.reasons_scroll.setFixedHeight(88)
        self.reasons_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #E6E6E6;
                width: 10px;
                border-radius: 5px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #B5B5B5;
                border-radius: 5px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9B9B9B;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.reasons_container = QWidget()
        self.reasons_box = QVBoxLayout(self.reasons_container)
        self.reasons_box.setSpacing(2)
        self.reasons_box.setContentsMargins(0, 0, 0, 0)
        self.reasons_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.reasons_scroll.setWidget(self.reasons_container)
        right_col.addWidget(self.reasons_scroll)
        right_col.addStretch()

        content_row.addLayout(right_col, 1)
        layout.addLayout(content_row, 0)

        # ---------------- BOTTOM AREA ----------------
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(24)

        left_buttons = QHBoxLayout()
        left_buttons.setSpacing(18)

        self.back_button = QPushButton(qta.icon("fa5s.arrow-left", color="white"), " Back")
        self.encrypt_button = QPushButton(qta.icon("fa5s.lock", color="white"), " Encrypt")
        self.decrypt_button = QPushButton(qta.icon("fa5s.unlock", color="white"), " Decrypt")

        self.back_button.clicked.connect(self.back_requested.emit)
        self.encrypt_button.clicked.connect(self.encrypt_requested.emit)
        self.decrypt_button.clicked.connect(self.decrypt_requested.emit)

        
        for btn in (self.back_button, self.encrypt_button, self.decrypt_button):
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(54)
            btn.setMinimumWidth(130)
            btn.setStyleSheet("""
                QPushButton {
                    background: #343438;
                    color: white;
                    border: none;
                    border-radius: 14px;
                    font-size: 15px;
                    font-weight: 500;
                    padding: 0 18px;
                }
                QPushButton:hover {
                    background: #4A4A50;
                }
            """)
            left_buttons.addWidget(btn)

        bottom_row.addLayout(left_buttons)
        bottom_row.addStretch()

        right_buttons = QHBoxLayout()
        right_buttons.setSpacing(20)

        self.advisory_button = QPushButton(qta.icon("fa5s.shield-alt", color="white"), " Check Advisory")
        self.advisory_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.advisory_button.setMinimumHeight(54)
        self.advisory_button.setMinimumWidth(220)
        self.advisory_button.setStyleSheet("""
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
        self.advisory_button.clicked.connect(self.advisory_requested.emit)

        self.new_eval_button = QPushButton(qta.icon("fa5s.file-medical", color="white"), " New Evaluation")
        self.new_eval_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_eval_button.setMinimumHeight(54)
        self.new_eval_button.setMinimumWidth(190)
        self.new_eval_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FCCC74,
                    stop:1 #F3BC23
                );
                color: white;
                font-size: 16px;
                font-weight: 500;
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
        self.new_eval_button.clicked.connect(self.back_requested.emit)

        right_buttons.addWidget(self.advisory_button)
        right_buttons.addWidget(self.new_eval_button)

        bottom_row.addLayout(right_buttons)
        layout.addLayout(bottom_row)

    def _make_field_row(self, icon_name: str, title: str) -> tuple[QWidget, QLabel]:
        row = QWidget()
        row.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(5)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color="#4F4F4F").pixmap(18, 18))

        title_lbl = QLabel(f"{title}:")
        title_lbl.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")
        title_lbl.setMinimumWidth(170)

        value_lbl = QLabel("-")
        value_lbl.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        row_layout.addWidget(icon)
        row_layout.addWidget(title_lbl)
        row_layout.addWidget(value_lbl)
        row_layout.addStretch()

        return row, value_lbl

    def _make_simple_result_label(self, icon_name: str, title: str, value: str) -> tuple[QWidget, QLabel]:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color="#4F4F4F").pixmap(22, 22))

        label = QLabel(f"{title}: {value}")
        label.setStyleSheet("font-size: 15px; color: #222; font-weight: 500;")

        row_layout.addWidget(icon)
        row_layout.addWidget(label)
        row_layout.addStretch()

        return row, label

    def _make_reason_row(self, reason: str) -> QWidget:
        row = QWidget()
        row.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)
        row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        icon = QLabel()
        icon.setPixmap(qta.icon("fa5s.exclamation-circle", color=ORANGE).pixmap(18, 18))

        label = QLabel(reason)
        label.setWordWrap(False)
        label.setStyleSheet("font-size: 14px; color: #444; font-weight: 500;")

        row_layout.addWidget(icon)
        row_layout.addWidget(label)
        row_layout.addStretch()

        return row

    def _risk_color(self, risk_level: str) -> str:
        if risk_level == "Low Risk":
            return LOW_COLOR
        if risk_level == "Medium Risk":
            return MEDIUM_COLOR
        if risk_level == "High Risk":
            return HIGH_COLOR
        return "#222"

    def set_result(
        self,
        report: str,
        risk_level: str,
        score: float,
        client_id: str = "-",
        inputs: dict | None = None,
        risk_distribution: dict | None = None,
        predicted_casualties: str = "-",
        predicted_crash_type: str = "-",
        predicted_maintenance: str = "-",
        reasons: list[str] | None = None,
    ):
        risk_distribution = risk_distribution or {"low": 0.0, "medium": 0.0, "high": 0.0}
        
        self.current_risk_level = risk_level
        self.current_client_id = client_id
        self.current_inputs = inputs or {}
        self.current_reasons = reasons or []

        self.risk_value.setText(risk_level)
        self.risk_value.setStyleSheet(
            f"font-size: 24px; font-weight: 500; color: {self._risk_color(risk_level)};"
        )

        self.client_label.setText(f"Client ID: {client_id}")
        self.score_label.setText(f"Evaluation Score: {score:.2f}")

        failure_text = "Yes" if float(self.current_inputs.get("failure_history", 0)) >= 0.5 else "No"

        value_map = {
            "driver_age": str(self.current_inputs.get("driver_age", "-")),
            "driver_experience": str(self.current_inputs.get("driver_experience", "-")),
            "driver_alcohol": str(self.current_inputs.get("driver_alcohol", "-")),
            "traffic_density": str(self.current_inputs.get("traffic_density", "-")),
            "vehicle_age": str(self.current_inputs.get("vehicle_age", "-")),
            "vehicle_type": str(self.current_inputs.get("vehicle_type", "-")),
            "failure_history": failure_text,
            "brake_condition": str(self.current_inputs.get("brake_condition", "-")),
            "weather": str(self.current_inputs.get("weather", "-")),
            "lighting": str(self.current_inputs.get("lighting", "-")),
            "road_condition": str(self.current_inputs.get("road_condition", "-")),
            "time_of_day": str(self.current_inputs.get("time_of_day", "-")),
            "road_type": str(self.current_inputs.get("road_type", "-")),
            "road_defect": str(self.current_inputs.get("road_defect", "-")),
            "intersection": str(self.current_inputs.get("intersection", "-")),
            "speed_limit": str(self.current_inputs.get("speed_limit", "-")),
        }

        for key, lbl in self.input_labels.items():
            lbl.setText(value_map.get(key, "-"))

        self.casualties_text.setText(f"Predicted Number of Casualties: {predicted_casualties}")
        self.crash_type_text.setText(f"Predicted Crash Type: {predicted_crash_type}")
        self.maintenance_text.setText(f"Predicted Maintenance Required: {predicted_maintenance}")
        self.low_distribution.setText(f"Low Risk: {risk_distribution['low']:.2f}%")
        self.medium_distribution.setText(f"Medium Risk: {risk_distribution['medium']:.2f}%")
        self.high_distribution.setText(f"High Risk: {risk_distribution['high']:.2f}%")
        
        while self.reasons_box.count():
            item = self.reasons_box.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for reason in self.current_reasons:
            self.reasons_box.addWidget(self._make_reason_row(reason))

        self.traffic_light.set_level(risk_level)

    def set_decrypted_report(self, report: str):
        pass

    def clear_result(self):
        self.current_risk_level = "-"
        self.current_client_id = "-"
        self.current_inputs = {}
        self.current_reasons = []

        self.risk_value.setText("-")
        self.risk_value.setStyleSheet("font-size: 24px; font-weight: 500; color: #222;")
        self.client_label.setText("Client ID: -")
        self.score_label.setText("Evaluation Score: -")

        for key, lbl in self.input_labels.items():
            lbl.setText("-")

        self.casualties_text.setText("Predicted Number of Casualties: -")
        self.crash_type_text.setText("Predicted Crash Type: -")
        self.maintenance_text.setText("Predicted Maintenance Required: -")
        
        self.low_distribution.setText("Low Risk: 0.00%")
        self.medium_distribution.setText("Medium Risk: 0.00%")
        self.high_distribution.setText("High Risk: 0.00%")
        
        while self.reasons_box.count():
            item = self.reasons_box.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.traffic_light.set_level("-")