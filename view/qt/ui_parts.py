import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QPen, QPolygon
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPoint


DARK = "#353434"
DARKER = "#211F1F"
ORANGE = "#F1A146"
LIGHT_ORANGE = "#FFBF76"
BROWN = "#704F14"
BLUE = "#0F3362"
FIELD_BG = "#EFEFEF"
FIELD_BORDER = "#D1D1D1"
CARD_BORDER = "#DBD6D6"
BTN_START = "#FCCC74"
BTN_END = "#F3BC23"


class DecorativeBackground(QWidget):
    def __init__(self, background_path: str = ""):
        super().__init__()
        self.background_pixmap = QPixmap(background_path) if background_path else QPixmap()
        self.header_mode = "auth"

    def set_header_mode(self, mode: str):
        self.header_mode = mode
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        painter.fillRect(rect, QColor("#F8F8F8"))

        if not self.background_pixmap.isNull():
            scaled = self.background_pixmap.scaled(
                rect.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter.setOpacity(0.95)
            painter.drawPixmap(0, 0, scaled)
            painter.setOpacity(1.0)

        self._draw_top_bars(painter, rect)
        self._draw_corner_accents(painter, rect)
        self._draw_bottom_section(painter, rect)

    def _draw_top_bars(self, painter: QPainter, rect):
        painter.fillRect(0, 28, rect.width(), 72, QColor(DARK))
        painter.fillRect(0, 108, rect.width(), 72, QColor(DARK))

        pen = QPen(QColor("white"))
        pen.setWidth(6)
        painter.setPen(pen)
        painter.drawLine(0, 104, rect.width(), 104)

        width = rect.width()

        if self.header_mode == "evaluation":
            top_size = max(18, min(28, width // 42))
            bottom_size = max(18, min(28, width // 44))

            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Inter", top_size, QFont.Weight.Medium))
            painter.drawText(
                QRectF(100, 42, width - 200, 40),
                Qt.AlignmentFlag.AlignCenter,
                "PRE-DRIVING EVALUATION",
            )

            painter.setPen(QColor("#8AFF84"))
            painter.setFont(QFont("Inter", bottom_size, QFont.Weight.Medium))
            painter.drawText(
                QRectF(40, 122, width - 80, 40),
                Qt.AlignmentFlag.AlignCenter,
                "COMPLETE ALL FIELDS TO ASSESS COMPREHENSIVE DRIVING RISK",
            )

        else:
            title_size = max(22, min(40, width // 32))
            subtitle_size = max(20, min(34, width // 38))

            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Inter", title_size, QFont.Weight.Medium))
            painter.drawText(
                QRectF(120, 34, width - 240, 50),
                Qt.AlignmentFlag.AlignCenter,
                "PRE-DRIVING ACCIDENT RISK",
            )

            painter.setFont(QFont("Inter", subtitle_size, QFont.Weight.Medium))
            painter.drawText(
                QRectF(120, 116, width - 240, 46),
                Qt.AlignmentFlag.AlignCenter,
                "EVALUATION AND ADVISORY",
            )

    def _draw_corner_accents(self, painter: QPainter, rect):
        painter.save()
        painter.translate(-120, 80)
        painter.rotate(-45)
        painter.fillRect(-120, 0, 560, 120, QColor("#2A2116"))
        painter.fillRect(-82, 18, 560, 120, QColor("#2E2822"))
        painter.fillRect(-42, 38, 560, 120, QColor(LIGHT_ORANGE))
        painter.fillRect(-2, 58, 360, 120, QColor(ORANGE))

        pen = QPen(QColor(DARK), 6)
        painter.setPen(pen)
        for x in (20, 40, 60, 80):
            painter.drawLine(x, 58, x, 178)
        painter.restore()

        painter.save()
        painter.translate(rect.width() + 120, 80)
        painter.rotate(45)
        painter.fillRect(-440, 0, 560, 120, QColor("#2A2116"))
        painter.fillRect(-478, 18, 560, 120, QColor("#2E2822"))
        painter.fillRect(-518, 38, 560, 120, QColor(LIGHT_ORANGE))
        painter.fillRect(-358, 58, 360, 120, QColor(ORANGE))

        pen = QPen(QColor(DARK), 6)
        painter.setPen(pen)
        for x in (-80, -60, -40, -20):
            painter.drawLine(x, 58, x, 178)
        painter.restore()

    def _draw_bottom_section(self, painter: QPainter, rect):
        painter.fillRect(0, rect.height() - 130, rect.width(), 50, QColor(DARK))
        painter.fillRect(0, rect.height() - 80, rect.width(), 80, QColor(DARKER))

        center_x = rect.width() // 2
        traffic_y = rect.height() - 190

        painter.setBrush(QColor(DARKER))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(center_x - 170, traffic_y, 340, 126, 50, 50)

        colors = [QColor("#237D2C"), QColor("#8A8115"), QColor("#972414")]
        for i, color in enumerate(colors):
            painter.setBrush(color)
            painter.drawEllipse(center_x - 122 + i * 106, traffic_y + 16, 82, 82)

        painter.setBrush(QColor(ORANGE))
        left_poly = [
            (150, rect.height() - 180),
            (360, rect.height() - 180),
            (500, rect.height()),
            (250, rect.height()),
        ]
        right_poly = [
            (rect.width() - 150, rect.height() - 180),
            (rect.width() - 360, rect.height() - 180),
            (rect.width() - 500, rect.height()),
            (rect.width() - 250, rect.height()),
        ]

        painter.drawPolygon(QPolygon([QPoint(x, y) for x, y in left_poly]))
        painter.drawPolygon(QPolygon([QPoint(x, y) for x, y in right_poly]))

        pen = QPen(QColor(DARK), 7)
        painter.setPen(pen)
        for y in (rect.height() - 152, rect.height() - 115, rect.height() - 78):
            painter.drawLine(0, y, 300, y)
            painter.drawLine(rect.width() - 300, y, rect.width(), y)


class CardFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("cardFrame")
        self.setStyleSheet(
            f"""
            QFrame#cardFrame {{
                background: white;
                border: 2px solid {CARD_BORDER};
                border-radius: 32px;
            }}
            """
        )


class LinkLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"color: {BLUE}; font-size: 20px; font-weight: 500; background: transparent;")

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder: str, icon=None, password=False, parent=None):
        super().__init__(parent)

        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(60)

        self.is_password = password
        self.password_visible = False

        if password:
            self.setEchoMode(QLineEdit.EchoMode.Password)

        self.setStyleSheet("""
            QLineEdit {
                background: #EFEFEF;
                border: 1px solid #D1D1D1;
                border-radius: 20px;
                padding-left: 42px;
                padding-right: 42px;
                font-size: 18px;
                color: #4A4A4A;
            }
        """)

        # LEFT ICON (FontAwesome)
        if icon:
            self.icon_label = QPushButton(self)
            self.icon_label.setIcon(qta.icon(icon, color="#8C8C8C"))
            self.icon_label.setStyleSheet("border: none; background: transparent;")
            self.icon_label.setEnabled(False)
        else:
            self.icon_label = None

        # RIGHT ICON (eye toggle)
        if password:
            self.eye_button = QPushButton(self)
            self.eye_button.setIcon(qta.icon("fa5s.eye-slash", color="#8C8C8C"))
            self.eye_button.setStyleSheet("border: none; background: transparent;")
            self.eye_button.clicked.connect(self.toggle_password)
        else:
            self.eye_button = None

    def resizeEvent(self, event):
        super().resizeEvent(event)

        h = self.height()

        if self.icon_label:
            self.icon_label.setGeometry(10, (h - 24)//2, 24, 24)

        if self.eye_button:
            self.eye_button.setGeometry(self.width() - 34, (h - 24)//2, 24, 24)

    def toggle_password(self):
        if self.password_visible:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_button.setIcon(qta.icon("fa5s.eye-slash", color="#8C8C8C"))
        else:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_button.setIcon(qta.icon("fa5s.eye", color="#8C8C8C"))

        self.password_visible = not self.password_visible

class PrimaryButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            f"""
            QPushButton {{
                color: white;
                font-size: 24px;
                font-weight: 500;
                letter-spacing: 4px;
                border: none;
                border-radius: 20px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {BTN_START},
                    stop:1 {BTN_END}
                );
            }}
            """
        )