from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QFrame,
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
        self.current_inputs = {}
        self.current_reasons = []
        self.current_recommendations = []
        self._build_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top_margin = 170
        available_w = self.width() - 70
        available_h = self.height() - top_margin - 35

        card_w = max(1000, min(1180, available_w))
        card_h = max(520, min(700, available_h))

        x = (self.width() - card_w) // 2
        y = top_margin
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
        self.reasons_card = AdvisoryCard("KEY RISK FACTORS", "fa5s.list")
        self.recommendation_card = AdvisoryCard("RECOMMENDED ACTIONS", "fa5s.shield-alt")
        self.uncertainty_card = AdvisoryCard("IMPORTANT NOTICE", "fa5s.sync-alt")
        self.legal_card = AdvisoryCard("LEGAL AND SAFETY REMINDERS", "fa5s.gavel")

        self.scroll_layout.addWidget(self.risk_card)
        self.scroll_layout.addWidget(self.reasons_card)
        self.scroll_layout.addWidget(self.recommendation_card)
        self.scroll_layout.addWidget(self.uncertainty_card)
        self.scroll_layout.addWidget(self.legal_card)
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
        inputs: dict,
        reasons: list[str],
        recommendations: list[str],
    ):
        self.current_client_id = client_id
        self.current_risk_level = risk_level
        self.current_inputs = inputs or {}
        self.current_reasons = reasons or []
        self.current_recommendations = recommendations or []

        self.client_label.setText(f"Client ID: {client_id}")
        self.score_label.setText(f"Evaluation Score: {score:.2f}")
        self.risk_value.setText(risk_level)
        self.risk_value.setStyleSheet(
            f"font-size: 22px; font-weight: 600; color: {self._risk_color(risk_level)};"
        )

        if risk_level == "Low Risk":
            self.risk_card.set_content(
                "LOW RISK",
                [
                    "Current conditions appear generally manageable for travel.",
                    "The driver may proceed while maintaining normal caution and safe driving practice.",
                    "A quick final vehicle and route check is still recommended before departure.",
                ],
            )
        elif risk_level == "Medium Risk":
            self.risk_card.set_content(
                "MEDIUM RISK",
                [
                    "There are notable risk factors present before travel.",
                    "The driver should proceed only with extra caution and proper preparation.",
                    "Trip conditions should be reassessed before departure if possible.",
                ],
            )
        else:
            self.risk_card.set_content(
                "HIGH RISK",
                [
                    "Current conditions indicate a serious pre-driving safety concern.",
                    "Travel should be delayed or avoided until the major risk factors are addressed.",
                    "Alternative transportation or postponement is strongly advised.",
                ],
            )

        self.reasons_card.set_content(
            "FACTORS IDENTIFIED",
            self.current_reasons if self.current_reasons else ["No major risk factors were identified beyond safer baseline conditions."]
        )

        self.recommendation_card.set_content(
            "SAFETY GUIDANCE",
            self.current_recommendations if self.current_recommendations else ["Continue following normal road safety practices."]
        )

        self.uncertainty_card.set_content(
            "RISK LEVEL MAY CHANGE",
            [
                "This advisory is based only on the conditions provided during the pre-driving evaluation.",
                "Actual risk may still change because of unexpected events such as sudden weather shifts, traffic build-up, road obstructions, vehicle issues, or driver condition changes.",
                "The driver should continue reassessing conditions even after the evaluation result is shown.",
            ],
        )

        legal_lines = [
            "Drivers are expected to provide honest and accurate inputs during evaluation.",
            "This system is intended for non-professional licensed private drivers.",
            "Under Republic Act No. 4136, responsible and careful driving is expected at all times.",
            "Do not drive when impaired, unfit, fatigued, or when your vehicle is not roadworthy.",
        ]

        alcohol_text = str(self.current_inputs.get("alcohol_consumption", "")).lower()
        if alcohol_text not in {"", "none", "select"}:
            legal_lines.append("Driving after alcohol consumption may place you and others at serious risk.")

        mechanical_text = str(self.current_inputs.get("recent_mechanical_issues", "")).lower()
        if mechanical_text in {"major issues (affects safety)", "moderate issues (needs attention)"}:
            legal_lines.append("Vehicle safety-related mechanical issues should be resolved before driving.")

        brake_text = str(self.current_inputs.get("brake_condition", "")).lower()
        if brake_text in {"noticeable delay", "weak / unreliable", "not sure"}:
            legal_lines.append("Brake condition must be verified before travel if responsiveness is uncertain or reduced.")

        self.legal_card.set_content("RESPONSIBILITY REMINDERS", legal_lines)