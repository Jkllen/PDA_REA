from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QScrollArea,
    QStackedWidget,
    QGridLayout,
)
from PyQt6.QtCore import pyqtSignal, Qt
import qtawesome as qta

from view.qt.ui_parts import BROWN


LOW_COLOR = "#059A1C"
MEDIUM_COLOR = "#8D8D01"
HIGH_COLOR = "#FF0000"

ORANGE = "#F28C13"
DARK_BUTTON = "#343438"
TAB_ACTIVE = "#23262F"
TAB_INACTIVE = "#F0C539"
TAB_TEXT_ACTIVE = "#FFE03A"
TAB_TEXT_INACTIVE = "#2F2F2F"


class FlatSection(QFrame):
    def __init__(self, title: str, icon_name: str = "", accent: str = ORANGE, highlight: bool = False, parent=None):
        super().__init__(parent)

        if highlight:
            bg = "rgba(255, 229, 227, 0.95)"   # soft red
        else:
            bg = "rgba(244, 235, 216, 0.95)"   # soft cream

        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: none;
                border-radius: 18px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        header = QHBoxLayout()
        header.setSpacing(10)

        if icon_name:
            icon = QLabel()
            icon.setPixmap(qta.icon(icon_name, color=accent).pixmap(20, 20))
            header.addWidget(icon)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            font-size: 17px;
            font-weight: 900;
            color: #111;
            background: transparent;
        """)
        header.addWidget(self.title_label)
        header.addStretch()

        self.subtitle_label = QLabel("")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 700;
            color: #6A5D49;
            text-transform: uppercase;
            background: transparent;
        """)

        self.body_label = QLabel("")
        self.body_label.setWordWrap(True)
        self.body_label.setStyleSheet("""
            font-size: 14px;
            color: #222;
            line-height: 1.6;
            background: transparent;
        """)

        layout.addLayout(header)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.body_label)

    def set_content(self, subtitle: str, lines: list[str]):
        self.subtitle_label.setText(subtitle)
        self.body_label.setText("\n".join(f"• {line}" for line in lines))

class SideCard(QFrame):
    def __init__(self, title: str, lines: list[str], icon_name: str = "", bg: str = "#F3EFE6", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: none;
                border-radius: 18px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        title_row = QHBoxLayout()
        title_row.setSpacing(8)

        if icon_name:
            icon = QLabel()
            icon.setPixmap(qta.icon(icon_name, color="#111").pixmap(18, 18))
            title_row.addWidget(icon)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("""
            font-size: 16px;
            font-weight: 800;
            color: #111;
            background: transparent;
        """)
        title_row.addWidget(title_lbl)
        title_row.addStretch()

        body_lbl = QLabel("\n".join(f"• {line}" for line in lines))
        body_lbl.setWordWrap(True)
        body_lbl.setStyleSheet("""
            font-size: 14px;
            color: #222;
            line-height: 1.45;
            background: transparent;
        """)

        layout.addLayout(title_row)
        layout.addWidget(body_lbl)
        
    def __init__(self, title: str, lines: list[str], icon_name: str = "", bg: str = "rgba(255,255,255,0.88)", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: none;
                border-radius: 18px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        title_row = QHBoxLayout()
        title_row.setSpacing(8)

        if icon_name:
            icon = QLabel()
            icon.setPixmap(qta.icon(icon_name, color="#111").pixmap(18, 18))
            title_row.addWidget(icon)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #111;")
        title_row.addWidget(title_lbl)
        title_row.addStretch()

        body_lbl = QLabel("\n".join(f"• {line}" for line in lines))
        body_lbl.setWordWrap(True)
        body_lbl.setStyleSheet("font-size: 14px; color: #222; line-height: 1.45;")

        layout.addLayout(title_row)
        layout.addWidget(body_lbl)


class ReminderTile(QFrame):
    def __init__(self, text: str, icon_name: str = "", bg: str = "#F6C400", fg: str = "#111", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: none;
                border-radius: 16px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        if icon_name:
            icon = QLabel()
            icon.setPixmap(qta.icon(icon_name, color=fg).pixmap(18, 18))
            layout.addWidget(icon)

        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {fg};")
        layout.addWidget(label, 1)


class TabButton(QPushButton):
    def __init__(self, text: str, icon_name: str, parent=None):
        super().__init__(parent)
        self._text = text
        self._icon_name = icon_name
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(64)
        self.setMinimumWidth(260)
        self.set_active(False)

    def set_active(self, active: bool):
        if active:
            self.setIcon(qta.icon(self._icon_name, color=TAB_TEXT_ACTIVE))
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {TAB_ACTIVE};
                    color: {TAB_TEXT_ACTIVE};
                    border: none;
                    border-radius: 18px;
                    font-size: 16px;
                    font-weight: 800;
                    padding: 0 20px;
                    text-align: center;
                }}
            """)
        else:
            self.setIcon(qta.icon(self._icon_name, color="#4F4F5C"))
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {TAB_INACTIVE};
                    color: {TAB_TEXT_INACTIVE};
                    border: none;
                    border-radius: 18px;
                    font-size: 16px;
                    font-weight: 700;
                    padding: 0 20px;
                    text-align: center;
                }}
            """)

        self.setText(self._text)
        self.setIconSize(qta.icon(self._icon_name).pixmap(18, 18).size())
    def __init__(self, text: str, icon_name: str, parent=None):
        super().__init__(parent)
        self._text = text
        self._icon_name = icon_name
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(64)
        self.setStyleSheet("border-radius: 18px;")
        self.set_active(False)

    def set_active(self, active: bool):
        if active:
            self.setIcon(qta.icon(self._icon_name, color=TAB_TEXT_ACTIVE))
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {TAB_ACTIVE};
                    color: {TAB_TEXT_ACTIVE};
                    border: none;
                    border-radius: 18px;
                    font-size: 16px;
                    font-weight: 800;
                    padding: 0 18px;
                    text-align: center;
                }}
            """)
        else:
            self.setIcon(qta.icon(self._icon_name, color="#4F4F5C"))
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {TAB_INACTIVE};
                    color: {TAB_TEXT_INACTIVE};
                    border: none;
                    border-radius: 18px;
                    font-size: 16px;
                    font-weight: 700;
                    padding: 0 18px;
                    text-align: center;
                }}
            """)
        self.setText(self._text)


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

        top_margin = 190
        side_margin = 70
        bottom_margin = 28

        content_w = self.width() - (side_margin * 2)
        content_h = self.height() - top_margin - bottom_margin

        content_w = max(1180, min(1320, content_w))
        content_h = max(620, min(780, content_h))

        x = (self.width() - content_w) // 2
        y = top_margin
        self.container.setGeometry(x, y, content_w, content_h)

    def _build_ui(self):
        self.container = QWidget(self)
        self.container.setStyleSheet("background: transparent;")

        outer = QVBoxLayout(self.container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(16)

        # top info row
        top_row = QHBoxLayout()
        top_row.setSpacing(18)

        left_info = QVBoxLayout()
        left_info.setSpacing(8)

        advisory_title_row = QHBoxLayout()
        advisory_title_row.setSpacing(15)

        title_icon = QLabel()
        title_icon.setPixmap(qta.icon("fa5s.shield-alt", color=ORANGE).pixmap(30, 30))

        self.title = QLabel("ADVISORY AND LEGAL GUIDANCE")
        self.title.setStyleSheet(f"font-size: 26px; font-weight: 900; color: {BROWN};")

        advisory_title_row.addWidget(title_icon)
        advisory_title_row.addWidget(self.title)
        advisory_title_row.addStretch()

        risk_row = QHBoxLayout()
        risk_row.setSpacing(8)

        self.risk_prefix = QLabel("Accident Risk Level:")
        self.risk_prefix.setStyleSheet("font-size: 19px; font-weight: 500; color: #111;")

        self.risk_value = QLabel("-")
        self.risk_value.setStyleSheet("font-size: 19px; font-weight: 800; color: #111;")

        risk_row.addWidget(self.risk_prefix)
        risk_row.addWidget(self.risk_value)
        risk_row.addStretch()

        left_info.addLayout(advisory_title_row)
        left_info.addLayout(risk_row)

        right_info = QVBoxLayout()
        right_info.setSpacing(8)
        right_info.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.client_label = QLabel("Client ID: -")
        self.client_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.client_label.setStyleSheet("font-size: 18px; color: #2854FF; font-weight: bold;")

        self.score_label = QLabel("Evaluation Score: -")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.score_label.setStyleSheet("font-size: 18px; color: #111; font-weight: bold;")

        right_info.addWidget(self.client_label)
        right_info.addWidget(self.score_label)

        top_row.addLayout(left_info, 1)
        top_row.addLayout(right_info)

        outer.addLayout(top_row)

        # tabs
        tabs_row = QHBoxLayout()
        tabs_row.setSpacing(12)

        self.tab_advisory = TabButton("Advisory Assessment", "fa5s.book-open")
        self.tab_safety = TabButton("Safety Discipline", "fa5s.shield-alt")
        self.tab_laws = TabButton("Laws Regulations", "fa5s.balance-scale")

        self.tab_advisory.clicked.connect(lambda: self._switch_tab("advisory"))
        self.tab_safety.clicked.connect(lambda: self._switch_tab("safety"))
        self.tab_laws.clicked.connect(lambda: self._switch_tab("laws"))

        tabs_row.addWidget(self.tab_advisory, 1)
        tabs_row.addWidget(self.tab_safety, 1)
        tabs_row.addWidget(self.tab_laws, 1)

        outer.addLayout(tabs_row)

        # content stack
        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self._build_advisory_tab())
        self.content_stack.addWidget(self._build_safety_tab())
        self.content_stack.addWidget(self._build_laws_tab())
        outer.addWidget(self.content_stack, 1)

        # bottom actions
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(16)

        self.back_button = QPushButton(qta.icon("fa5s.arrow-left", color="white"), " Back to Result")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setMinimumHeight(54)
        self.back_button.setMinimumWidth(190)
        self.back_button.setStyleSheet(f"""
            QPushButton {{
                background: {DARK_BUTTON};
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 15px;
                font-weight: 600;
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
        self.new_eval_button.setMinimumWidth(220)
        self.new_eval_button.setStyleSheet("""
            QPushButton {
                background: #F1C54B;
                color: white;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 20px;
                padding: 0 24px;
            }
            QPushButton:hover {
                background: #F5CF68;
            }
        """)
        self.new_eval_button.clicked.connect(self.new_evaluation_requested.emit)

        bottom_row.addWidget(self.back_button)
        bottom_row.addStretch()
        bottom_row.addWidget(self.new_eval_button)

        outer.addLayout(bottom_row)

        self._switch_tab("advisory")

    # ---------- advisory tab ----------
    def _build_advisory_tab(self):
        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # LEFT SIDE
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        scroll_left = QScrollArea()
        scroll_left.setWidgetResizable(True)
        scroll_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_left.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #ECECEC;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0;
                border-radius: 5px;
                min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        left_content = QWidget()
        left_content_layout = QVBoxLayout(left_content)
        left_content_layout.setContentsMargins(0, 0, 0, 0)
        left_content_layout.setSpacing(12)

        self.critical_section = FlatSection("CRITICAL SAFETY ADVISORY", "fa5s.exclamation-triangle", "#FF3B30", True)
        self.explanation_section = FlatSection("ASSESSMENT EXPLANATION", "fa5s.clipboard-check", ORANGE)
        self.risk_factors_section = FlatSection("SPECIFIC RISK FACTORS", "fa5s.list", ORANGE)

        left_content_layout.addWidget(self.critical_section)
        left_content_layout.addWidget(self.explanation_section)
        left_content_layout.addWidget(self.risk_factors_section)
        left_content_layout.addStretch()

        scroll_left.setWidget(left_content)
        left_layout.addWidget(scroll_left)

        # RIGHT SIDE
        right_panel = QWidget()
        right_panel.setFixedWidth(360)

        right_outer_layout = QVBoxLayout(right_panel)
        right_outer_layout.setContentsMargins(0, 0, 0, 0)
        right_outer_layout.setSpacing(0)

        scroll_right = QScrollArea()
        scroll_right.setWidgetResizable(True)
        scroll_right.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_right.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #ECECEC;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0;
                border-radius: 5px;
                min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        right_scroll_content = QWidget()
        right_layout = QVBoxLayout(right_scroll_content)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.side_priority_card = SideCard(
            "Priority Actions",
            [
                "Correct the most serious risk factor first.",
                "Do not drive if you are impaired, fatigued, or unfit.",
                "Check vehicle roadworthiness before travel.",
            ],
            "fa5s.tasks",
            "#F3EFE6",
        )

        self.side_vehicle_check_card = SideCard(
            "Quick Vehicle Check",
            [
                "Inspect brakes, lights, tires, and mirrors.",
                "Check for leaks, visible damage, or warning signs.",
                "If unsure about safety, do not drive yet.",
            ],
            "fa5s.car-side",
            "#F3EFE6",
        )

        self.side_reminder_card = SideCard(
            "Safety Reminder",
            [
                "Your safety is in your hands.",
                "Learn to say no when you are not fit to drive.",
                "Driver must follow the rules and drive responsibly.",
            ],
            "fa5s.shield-alt",
            "#F3EFE6",
        )

        right_layout.addWidget(self.side_priority_card)
        right_layout.addWidget(self.side_vehicle_check_card)
        right_layout.addWidget(self.side_reminder_card)
        right_layout.addStretch()

        scroll_right.setWidget(right_scroll_content)
        right_outer_layout.addWidget(scroll_right)

        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 0)

        return wrapper
    
    # ---------- safety tab ----------
    def _build_safety_tab(self):
        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(22)

        # LEFT SIDE SCROLL
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        scroll_left = QScrollArea()
        scroll_left.setWidgetResizable(True)
        scroll_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_left.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #ECECEC;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0;
                border-radius: 5px;
                min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        left_content = QWidget()
        left_content_layout = QVBoxLayout(left_content)
        left_content_layout.setContentsMargins(0, 0, 0, 0)
        left_content_layout.setSpacing(14)

        top_grid = QGridLayout()
        top_grid.setHorizontalSpacing(12)
        top_grid.setVerticalSpacing(12)

        prayer_tile = SideCard(
            '"Pray Before Driving"',
            [
                "Take a moment to center yourself spiritually and mentally.",
                "Ask for safe travels and protection for yourself and others on the road.",
            ],
            "fa5s.praying-hands",
            "rgba(215,229,255,0.92)",
        )

        top_grid.addWidget(prayer_tile, 0, 0, 2, 2)
        top_grid.addWidget(ReminderTile('"Your Safety is in Your Hands"'), 0, 2)
        top_grid.addWidget(ReminderTile('"Learn to Say NO"'), 0, 3)
        top_grid.addWidget(ReminderTile('"Drivers MUST Follow Rules"'), 1, 2)
        top_grid.addWidget(ReminderTile('"Better Late Than Never"'), 1, 3)

        left_content_layout.addLayout(top_grid)

        health_title = QLabel("Pre-Drive Health Checklist")
        health_title.setStyleSheet("font-size: 19px; font-weight: 800; color: #111;")
        left_content_layout.addWidget(health_title)

        health_grid = QGridLayout()
        health_grid.setHorizontalSpacing(12)
        health_grid.setVerticalSpacing(12)

        health_grid.addWidget(SideCard(
            "✓ Get Adequate Sleep",
            [
                "Ensure proper sleep before driving.",
                "Aim for 7–8 hours of quality rest.",
                "Never drive when sleepy, fatigued, or unable to focus properly.",
            ],
            "",
            "rgba(255,248,224,0.95)",
        ), 0, 0)

        health_grid.addWidget(SideCard(
            "✓ Eat Proper Meals",
            [
                "Eat before long drives.",
                "Avoid driving on an empty stomach for long trips.",
                "Low energy may reduce concentration and reaction time.",
            ],
            "",
            "rgba(255,248,224,0.95)",
        ), 0, 1)

        health_grid.addWidget(SideCard(
            "✓ Stay Hydrated",
            [
                "Drink water regularly.",
                "Dehydration may cause headache, fatigue, and reduced alertness.",
            ],
            "",
            "rgba(255,248,224,0.95)",
        ), 0, 2)

        health_grid.addWidget(SideCard(
            "✓ Check Medical Fitness",
            [
                "Do not drive if you feel dizzy, ill, emotionally unstable, or affected by drowsy medication.",
                "Impaired means your ability to operate a vehicle safely is reduced.",
            ],
            "",
            "rgba(255,248,224,0.95)",
        ), 0, 3)

        left_content_layout.addLayout(health_grid)

        self.discipline_section = FlatSection("DRIVING DISCIPLINE AND DRIVER BEHAVIOR", "fa5s.user-shield", ORANGE)
        self.discipline_section.set_content(
            "SAFE DRIVING PRACTICES",
            [
                "Maintain focus and avoid distractions such as mobile phones while driving.",
                "Keep proper steering control and avoid sudden, aggressive maneuvers.",
                "Maintain safe following distance and observe other road users carefully.",
                "Driver should follow the rules, use signals properly, and respect road markings and signs.",
                "Learn to say no to driving when tired, emotionally unstable, pressured, or unfit.",
            ],
        )
        left_content_layout.addWidget(self.discipline_section)

        self.knowledge_section = FlatSection("DRIVING KNOWLEDGE AND SAFE PRACTICE", "fa5s.book-reader", ORANGE)
        self.knowledge_section.set_content(
            "IMPORTANT REMINDERS",
            [
                "Impaired driving means reduced ability to drive safely due to alcohol, fatigue, illness, stress, or medication.",
                "Safe driving includes staying alert, controlling speed, using signals properly, and protecting passengers and pedestrians.",
                "For longer travel, avoid driving continuously beyond 6 hours. Rest earlier whenever possible.",
            ],
        )
        left_content_layout.addWidget(self.knowledge_section)

        left_content_layout.addStretch()
        scroll_left.setWidget(left_content)
        left_layout.addWidget(scroll_left)

        # RIGHT SIDE SCROLL
        right_panel = QWidget()
        right_panel.setFixedWidth(360)

        right_outer_layout = QVBoxLayout(right_panel)
        right_outer_layout.setContentsMargins(0, 0, 0, 0)
        right_outer_layout.setSpacing(0)

        scroll_right = QScrollArea()
        scroll_right.setWidgetResizable(True)
        scroll_right.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_right.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #ECECEC;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0;
                border-radius: 5px;
                min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        right_layout.addWidget(SideCard(
            "Discipline Checklist",
            [
                "No distracted driving",
                "No aggressive driving",
                "No driving under influence",
                "Follow traffic signals and road signs",
                "Yield properly and respect pedestrians",
            ],
            "fa5s.clipboard-list",
            "#F3EFE6",
        ))

        right_layout.addWidget(SideCard(
            "Proper Vehicle Checking",
            [
                "Walk around the vehicle before every trip.",
                "Check tires, lights, brakes, mirrors, and visible damage.",
                "Confirm the vehicle is roadworthy before departure.",
            ],
            "fa5s.tools",
            "#F3EFE6",
        ))

        right_layout.addWidget(SideCard(
            "Maximum Continuous Driving",
            [
                "Avoid driving continuously beyond 6 hours.",
                "Take breaks every 2–3 hours whenever possible.",
                "Stop earlier if you feel sleepy, tired, dizzy, or unfocused.",
            ],
            "fa5s.clock",
            "#F3EFE6",
        ))

        right_layout.addStretch()
        scroll_right.setWidget(right_content)
        right_outer_layout.addWidget(scroll_right)

        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 0)

        return wrapper
    
    # ---------- laws tab ----------
    def _build_laws_tab(self):
        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(22)

        # LEFT SIDE SCROLL
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        scroll_left = QScrollArea()
        scroll_left.setWidgetResizable(True)
        scroll_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_left.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #ECECEC;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0;
                border-radius: 5px;
                min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        left_content = QWidget()
        left_content_layout = QVBoxLayout(left_content)
        left_content_layout.setContentsMargins(0, 0, 0, 0)
        left_content_layout.setSpacing(14)

        legal_banner = QFrame()
        legal_banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF2D55,
                    stop:1 #FF7A00
                );
                border-radius: 18px;
            }
            QLabel {
                background: transparent;
            }
        """)
        banner_layout = QHBoxLayout(legal_banner)
        banner_layout.setContentsMargins(22, 18, 22, 18)
        banner_layout.setSpacing(24)

        banner_layout.addWidget(self._banner_block(
            "Legal Liability",
            "Drivers may be criminally and civilly liable for accidents caused by negligence or reckless driving."
        ))
        banner_layout.addWidget(self._banner_block(
            "Insurance Required",
            "Required vehicle documents and insurance must be in order before travel."
        ))
        banner_layout.addWidget(self._banner_block(
            "High-Risk Penalties",
            "Repeated violations may result in larger fines, suspension, or other serious legal consequences."
        ))

        left_content_layout.addWidget(legal_banner)

        laws_grid = QGridLayout()
        laws_grid.setHorizontalSpacing(12)
        laws_grid.setVerticalSpacing(12)

        laws_grid.addWidget(SideCard(
            "RA 4136",
            [
                "Land Transportation and Traffic Code",
                "Vehicle registration and licensing rules",
                "Traffic violations and penalties",
                "Roadworthiness standards",
            ],
            "fa5s.balance-scale",
            "#F3EFE6",
        ), 0, 0)

        laws_grid.addWidget(SideCard(
            "RA 10913",
            [
                "Anti-Distracted Driving Act",
                "No mobile phone use while driving",
                "Hands-free use has limited exceptions",
                "Violations may result in fines",
            ],
            "fa5s.balance-scale",
            "#F3EFE6",
        ), 0, 1)

        laws_grid.addWidget(SideCard(
            "RA 8750",
            [
                "Seat Belt Use Act",
                "Mandatory for driver and passengers where applicable",
                "Promotes occupant safety compliance",
                "Violations may result in fines",
            ],
            "fa5s.balance-scale",
            "#F3EFE6",
        ), 0, 2)

        laws_grid.addWidget(SideCard(
            "LTO Compliance",
            [
                "Valid driver’s license",
                "Updated vehicle registration",
                "Required insurance",
                "Medical fitness to drive",
            ],
            "fa5s.file-alt",
            "#F3EFE6",
        ), 1, 0)

        laws_grid.addWidget(SideCard(
            "Violation Penalties",
            [
                "Reckless driving may lead to fines and legal liability.",
                "Driving under the influence may lead to severe penalties and suspension.",
                "No valid license or unsafe vehicle condition may also lead to penalties.",
            ],
            "fa5s.exclamation-triangle",
            "#F3EFE6",
        ), 1, 1, 1, 2)

        left_content_layout.addLayout(laws_grid)
        left_content_layout.addStretch()

        scroll_left.setWidget(left_content)
        left_layout.addWidget(scroll_left)

        # RIGHT SIDE SCROLL
        right_panel = QWidget()
        right_panel.setFixedWidth(360)

        right_outer_layout = QVBoxLayout(right_panel)
        right_outer_layout.setContentsMargins(0, 0, 0, 0)
        right_outer_layout.setSpacing(0)

        scroll_right = QScrollArea()
        scroll_right.setWidgetResizable(True)
        scroll_right.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_right.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #ECECEC;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0;
                border-radius: 5px;
                min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        right_layout.addWidget(SideCard(
            "Mandatory Before Driving",
            [
                "Valid driver’s license",
                "Updated registration",
                "Required insurance",
                "Fit driver condition",
            ],
            "fa5s.exclamation-circle",
            "#F3EFE6",
        ))

        right_layout.addWidget(SideCard(
            "Rule Reminder",
            [
                "Driver must follow the rules at all times.",
                "Better late than never.",
                "Your safety is in your hands.",
            ],
            "fa5s.gavel",
            "#F3EFE6",
        ))

        right_layout.addWidget(SideCard(
            "Legal Responsibility",
            [
                "Driving requires discipline and accountability.",
                "Reckless or negligent behavior may lead to legal consequences.",
                "Always make safe and lawful driving decisions.",
            ],
            "fa5s.user-shield",
            "#F3EFE6",
        ))

        right_layout.addStretch()
        scroll_right.setWidget(right_content)
        right_outer_layout.addWidget(scroll_right)

        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 0)

        return wrapper
    
    def _banner_block(self, title: str, text: str):
        block = QWidget()
        layout = QVBoxLayout(block)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: white;")

        body_lbl = QLabel(text)
        body_lbl.setWordWrap(True)
        body_lbl.setStyleSheet("font-size: 14px; color: white; line-height: 1.4;")

        layout.addWidget(title_lbl)
        layout.addWidget(body_lbl)
        return block

    def _switch_tab(self, tab_name: str):
        self.tab_advisory.set_active(tab_name == "advisory")
        self.tab_safety.set_active(tab_name == "safety")
        self.tab_laws.set_active(tab_name == "laws")

        if tab_name == "advisory":
            self.content_stack.setCurrentIndex(0)
        elif tab_name == "safety":
            self.content_stack.setCurrentIndex(1)
        else:
            self.content_stack.setCurrentIndex(2)

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
        self.score_label.setText(f"Severity Score: {score * 100:.2f}%")
        self.risk_value.setText(risk_level)
        self.risk_value.setStyleSheet(
            f"font-size: 19px; font-weight: 800; color: {self._risk_color(risk_level)};"
        )

        if risk_level == "Low Risk":
            critical_lines = [
                "Your current inputs indicate a lower level of pre-driving risk.",
                "You may proceed, but safe driving discipline and vehicle checking are still necessary.",
                "Continue reassessing your condition, your vehicle, and your surroundings before departure.",
            ]
            explanation_lines = [
                "Low Risk does not mean zero risk.",
                "Unexpected traffic, weather changes, fatigue, or vehicle issues may still affect safety.",
                "Stay alert and continue following all traffic rules and responsible driving practices.",
            ]
        elif risk_level == "Medium Risk":
            critical_lines = [
                "Your current inputs indicate a moderate level of pre-driving risk.",
                "Driving may still be possible, but only with extra caution and proper preparation.",
                "You should correct controllable issues first before proceeding.",
            ]
            explanation_lines = [
                "Medium Risk means there are notable conditions that may reduce driving safety.",
                "Examples may include fatigue, unsafe weather, route hazards, or vehicle concerns.",
                "Reduce exposure by delaying travel, using a safer route, or correcting driver or vehicle issues first.",
            ]
        else:
            critical_lines = [
                "Your current inputs indicate a high level of pre-driving risk.",
                "Driving is not recommended unless major risk factors are addressed first.",
                "Failure to correct these issues may increase the chance of accidents, injury, or legal consequences.",
            ]
            explanation_lines = [
                "High Risk means one or more serious conditions are affecting safe driving ability.",
                "Examples may include alcohol use, unsafe weather, major mechanical issues, poor brake condition, or unfit driver condition.",
                "The safest decision may be to delay the trip, refuse to drive, or use another transport option.",
            ]

        self.critical_section.set_content("Risk Status", critical_lines)
        self.explanation_section.set_content("What This Means", explanation_lines)
        self.risk_factors_section.set_content(
            "Factors Identified",
            self.current_reasons if self.current_reasons else ["No major risk factors were identified beyond safer baseline conditions."]
        )

        joined = " ".join(self.current_recommendations).lower()

        priority_lines = list(self.current_recommendations) if self.current_recommendations else [
            "Review your driver condition, vehicle condition, and route before departure."
        ]

        if "alcohol" in joined:
            priority_lines.insert(0, "Do not drive after consuming alcohol.")
        if "brake" in joined or "mechanical" in joined:
            priority_lines.insert(0, "Resolve safety-related vehicle issues before travel.")

        self.side_priority_card = self._replace_side_card(
            self.side_priority_card,
            "Priority Actions",
            priority_lines[:5],
            "fa5s.tasks",
        )

        self.side_vehicle_check_card = self._replace_side_card(
            self.side_vehicle_check_card,
            "Quick Vehicle Check",
            [
                "Inspect brakes, tires, lights, and mirrors.",
                "Confirm no major warning signs or obvious damage.",
                "If unsure about roadworthiness, do not drive yet.",
            ],
            "fa5s.car-side",
        )

        reminder_lines = [
            "Your safety is in your hands.",
            "Learn to say no when you are not fit to drive.",
            "Driver must follow the rules and drive responsibly.",
        ]
        self.side_reminder_card = self._replace_side_card(
            self.side_reminder_card,
            "Safety Reminder",
            reminder_lines,
            "fa5s.shield-alt",
        )

    def _replace_side_card(self, old_widget, title, lines, icon_name):
        parent_layout = old_widget.parentWidget().layout()
        index = parent_layout.indexOf(old_widget)
        parent_layout.removeWidget(old_widget)
        old_widget.deleteLater()

        new_card = SideCard(title, lines, icon_name, "rgba(255,255,255,0.88)")
        parent_layout.insertWidget(index, new_card)
        return new_card