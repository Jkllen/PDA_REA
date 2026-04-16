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
from PyQt6.QtCore import pyqtSignal, Qt
import qtawesome as qta

from view.qt.ui_parts import CardFrame, BROWN


LOW_COLOR = "#059A1C"
MEDIUM_COLOR = "#8D8D01"
HIGH_COLOR = "#FF0000"
ORANGE = "#F28C13"
DARK_BUTTON = "#343438"
YELLOW_START = "#FCCC74"
YELLOW_END = "#F3BC23"


class AdvisoryCard(QFrame):
    def __init__(self, title: str, icon_name: str, accent: str = ORANGE, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #D7D7D7;
                border-radius: 16px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color=accent).pixmap(22, 22))
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 17px; font-weight: 800; color: #111;")

        header.addWidget(icon)
        header.addWidget(self.title_label)
        header.addStretch()

        self.subtitle_label = QLabel("")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #444;")

        self.body_label = QLabel("")
        self.body_label.setWordWrap(True)
        self.body_label.setStyleSheet("font-size: 14px; color: #333; line-height: 1.4;")

        layout.addLayout(header)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.body_label)

    def set_content(self, subtitle: str, lines: list[str]):
        self.subtitle_label.setText(subtitle)
        self.body_label.setText("\n".join(f"• {line}" for line in lines))


class AdvisoryScreen(QWidget):
    back_to_result_requested = pyqtSignal()
    new_evaluation_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_risk_level = "-"
        self.current_client_id = "-"
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_margin = 190
        available_w = self.width() - 70
        available_h = self.height() - top_margin - 35

        card_w = max(1000, min(1180, available_w))
        card_h = max(520, min(700, available_h))

        x = (self.width() - card_w) // 2
        y = max(top_margin, (self.height() - card_h) // 2)
        self.card.setGeometry(x, y, card_w, card_h)

    def _build_ui(self):
        self.card = CardFrame(self)

        outer = QVBoxLayout(self.card)
        outer.setContentsMargins(30, 20, 30, 18)
        outer.setSpacing(12)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        left = QVBoxLayout()
        left.setSpacing(8)

        title_row = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon("fa5s.shield-alt", color=ORANGE).pixmap(34, 34))

        self.title = QLabel("ADVISORY AND LEGAL GUIDANCE")
        self.title.setStyleSheet(f"color: {BROWN}; font-size: 28px; font-weight: 800;")

        title_row.addWidget(title_icon)
        title_row.addWidget(self.title)
        title_row.addStretch()

        risk_row = QHBoxLayout()
        self.risk_prefix = QLabel("Accident Risk Level:")
        self.risk_prefix.setStyleSheet("font-size: 22px; font-weight: 600; color: #111;")

        self.risk_value = QLabel("-")
        self.risk_value.setStyleSheet("font-size: 22px; font-weight: 600; color: #111;")

        risk_row.addWidget(self.risk_prefix)
        risk_row.addWidget(self.risk_value)
        risk_row.addStretch()

        left.addLayout(title_row)
        left.addLayout(risk_row)

        right = QVBoxLayout()
        right.setSpacing(8)
        right.setAlignment(Qt.AlignmentFlag.AlignRight)

        client_row = QHBoxLayout()
        client_row.setAlignment(Qt.AlignmentFlag.AlignRight)
        client_icon = QLabel()
        client_icon.setPixmap(qta.icon("fa5s.user", color="#808080").pixmap(22, 22))

        self.client_label = QLabel("Client ID: -")
        self.client_label.setStyleSheet("font-size: 17px; color: #0A2AD5; font-weight: 500;")

        client_row.addWidget(client_icon)
        client_row.addWidget(self.client_label)

        self.score_label = QLabel("Evaluation Score: -")
        self.score_label.setStyleSheet("font-size: 17px; color: #111; font-weight: 600;")

        right.addLayout(client_row)
        right.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignRight)

        top_row.addLayout(left, 1)
        top_row.addLayout(right)

        outer.addLayout(top_row)

        hline = QFrame()
        hline.setFrameShape(QFrame.Shape.HLine)
        hline.setStyleSheet("background: #5F5F5F; min-height: 2px; max-height: 2px; border: none;")
        outer.addWidget(hline)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(12)

        self.risk_card = AdvisoryCard("RISK LEVEL ADVISORY", "fa5s.exclamation-triangle")
        self.casualty_card = AdvisoryCard("CASUALTY ADVISORY", "fa5s.users")
        self.crash_card = AdvisoryCard("CRASH TYPE ADVISORY", "fa5s.car-crash")
        self.maintenance_card = AdvisoryCard("MAINTENANCE ADVISORY", "fa5s.wrench")
        self.general_card = AdvisoryCard("GENERAL RECOMMENDATIONS", "fa5s.info-circle")

        self.scroll_layout.addWidget(self.risk_card)
        self.scroll_layout.addWidget(self.casualty_card)
        self.scroll_layout.addWidget(self.crash_card)
        self.scroll_layout.addWidget(self.maintenance_card)
        self.scroll_layout.addWidget(self.general_card)
        self.scroll_layout.addStretch()

        self.scroll.setWidget(self.scroll_content)
        outer.addWidget(self.scroll, 1)

        bottom = QHBoxLayout()
        bottom.setSpacing(16)

        self.back_button = QPushButton(qta.icon("fa5s.arrow-left", color="white"), " Back to Result")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setMinimumHeight(54)
        self.back_button.setMinimumWidth(180)
        self.back_button.setStyleSheet(f"""
            QPushButton {{
                background: {DARK_BUTTON};
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 15px;
                font-weight: 500;
                padding: 0 18px;
            }}
            QPushButton:hover {{
                background: #4A4A50;
            }}
        """)
        self.back_button.clicked.connect(self.back_to_result_requested.emit)

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
        self.new_eval_button.clicked.connect(self.new_evaluation_requested.emit)

        bottom.addWidget(self.back_button)
        bottom.addStretch()
        bottom.addWidget(self.new_eval_button)

        outer.addLayout(bottom)

    def _risk_color(self, risk_level: str) -> str:
        if risk_level == "Low Risk":
            return LOW_COLOR
        if risk_level == "Medium Risk":
            return MEDIUM_COLOR
        if risk_level == "High Risk":
            return HIGH_COLOR
        return "#222"

    def set_advisory(
        self,
        client_id: str,
        risk_level: str,
        score: float,
        predicted_casualties: str,
        predicted_crash_type: str,
        predicted_maintenance: str,
        inputs: dict,
    ):
        self.current_client_id = client_id
        self.current_risk_level = risk_level

        self.client_label.setText(f"Client ID: {client_id}")
        self.score_label.setText(f"Evaluation Score: {score:.2f}")
        self.risk_value.setText(risk_level)
        self.risk_value.setStyleSheet(
            f"font-size: 22px; font-weight: 600; color: {self._risk_color(risk_level)};"
        )

        # Risk-level advisory
        if risk_level == "Low Risk":
            self.risk_card.set_content(
                "CLEAR",
                [
                    "Follow all traffic rules and speed limits.",
                    "Wear your seatbelt at all times.",
                    "Avoid using your phone while driving.",
                    "Stay alert even if roads look clear.",
                ],
            )
        elif risk_level == "Medium Risk":
            self.risk_card.set_content(
                "WARNING",
                [
                    "Slow down — conditions are riskier than normal.",
                    "Keep a safe distance from the vehicle ahead.",
                    "Avoid overtaking near corners and intersections.",
                    "Do not drive if you feel tired or distracted.",
                    "If unsure, pull over and wait for conditions to improve.",
                ],
            )
        else:
            self.risk_card.set_content(
                "CRITICAL — DO NOT DRIVE",
                [
                    "Stop driving immediately if possible.",
                    "Turn on all your lights.",
                    "Do not push through flooding, complete darkness, or very poor road conditions.",
                    "Let another driver take over, or delay your trip.",
                    "Call MMDA Hotline 136 or Emergency 911 if needed.",
                ],
            )

        # Casualty advisory
        if predicted_casualties == "Few":
            self.casualty_card.set_content(
                "ADVISORY",
                [
                    "Make sure all passengers are seated properly.",
                    "Do not overload your vehicle.",
                    "Keep seatbelts on.",
                    "Stay focused and drive carefully.",
                ],
            )
        elif predicted_casualties == "Moderate":
            self.casualty_card.set_content(
                "WARNING",
                [
                    "Reduce speed — more people are at risk here.",
                    "Do not overload your vehicle.",
                    "Take an alternate route if traffic is heavy.",
                    "Stop and rest if you feel fatigued before continuing.",
                ],
            )
        else:
            self.casualty_card.set_content(
                "CRITICAL — DO NOT DRIVE",
                [
                    "Do not drive if road conditions are dangerous.",
                    "Avoid this road and use an alternate route.",
                    "Large vehicles should park safely and wait.",
                    "Delay the trip or let a more experienced driver take over.",
                    "If an accident happens, call 911 immediately.",
                ],
            )

        # Crash-type advisory
        if predicted_crash_type == "No injury":
            self.crash_card.set_content(
                "CLEAR",
                [
                    "Drive normally but stay cautious.",
                    "Keep a safe distance from other vehicles.",
                    "Carry your license and vehicle documents at all times.",
                ],
            )
        elif predicted_crash_type == "Drive away":
            self.crash_card.set_content(
                "ADVISORY",
                [
                    "If a minor incident happens, stop and check all parties.",
                    "Exchange information and take photos of any damage.",
                    "Do not flee the scene.",
                ],
            )
        elif predicted_crash_type == "Injury":
            self.crash_card.set_content(
                "WARNING",
                [
                    "Slow down — there is a real risk of injury under current conditions.",
                    "If an accident happens, do not leave, call 911, and give first aid if you can.",
                    "Avoid this road if conditions are unsafe.",
                    "If tired or stressed, let another driver take over.",
                ],
            )
        else:
            self.crash_card.set_content(
                "CRITICAL — DO NOT DRIVE",
                [
                    "Risk of a severe crash that can make your vehicle undriveable.",
                    "Do not drive a damaged vehicle.",
                    "Call towing through MMDA 136 or use alternate transport.",
                    "Do not leave a damaged vehicle blocking traffic.",
                ],
            )

        # Maintenance advisory
        if predicted_maintenance == "No":
            self.maintenance_card.set_content(
                "CLEAR",
                [
                    "Vehicle is in good condition — keep it that way.",
                    "Check tires, brakes, and lights before every trip.",
                    "Schedule regular maintenance to stay roadworthy.",
                ],
            )
        else:
            self.maintenance_card.set_content(
                "CRITICAL — DO NOT DRIVE",
                [
                    "Your vehicle has a problem that needs fixing — do not drive it.",
                    "Call a mechanic for an on-site check or have it towed.",
                    "Use Grab, Angkas, or public transport in the meantime.",
                    "Driving this vehicle puts you and others in danger.",
                ],
            )

        # General recommendations
        general_lines = [
            "Always bring your driver's license, OR, and CR.",
            "Renew your license and registration before they expire.",
        ]

        if float(inputs.get("driver_alcohol", 0)) > 0:
            general_lines.extend([
                "You are not safe to drive while intoxicated.",
                "Call a sober friend or use Grab / Angkas.",
                "Stay parked in a safe place until you are sober.",
            ])

        if str(inputs.get("intersection", "")).lower() == "at intersection":
            general_lines.extend([
                "Slow down to a maximum of 20 kph.",
                "Yield to vehicles coming from the right.",
                "Do not overtake at intersections.",
            ])

        if str(inputs.get("vehicle_type", "")).lower() == "motorcycle":
            general_lines.extend([
                "Check that your headlight and taillight are working.",
                "Wear your helmet and protective gear.",
                "Do not overtake near corners or intersections.",
            ])

        if str(inputs.get("road_type", "")).lower() == "city road":
            general_lines.extend([
                "Observe the 30 kph limit on city streets.",
                "Reduce to 20 kph near intersections and crowded zones.",
                "Watch out for pedestrians at all times.",
            ])

        general_lines.extend([
            "If any accident occurs, stay at the scene.",
            "Show your license to the other party and to authorities.",
            "Help any injured person immediately.",
            "Call 911 for emergencies.",
        ])

        self.general_card.set_content("ADVISORY / LEGAL NOTICE", general_lines)

    def clear_advisory(self):
        self.client_label.setText("Client ID: -")
        self.score_label.setText("Evaluation Score: -")
        self.risk_value.setText("-")
        self.risk_value.setStyleSheet("font-size: 22px; font-weight: 600; color: #111;")

        for card in (
            self.risk_card,
            self.casualty_card,
            self.crash_card,
            self.maintenance_card,
            self.general_card,
        ):
            card.set_content("", [])