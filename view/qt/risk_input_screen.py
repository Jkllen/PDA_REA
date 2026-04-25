from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal

from view.qt.ui_parts import CardFrame
from view.qt.onboarding_screen import OnboardingScreen
from view.qt.driver_trip_screen import DriverTripScreen
from view.qt.environment_screen import EnvironmentScreen
from view.qt.vehicle_screen import VehicleScreen


class RiskInputScreen(QWidget):
    evaluate_requested = pyqtSignal(dict)
    back_to_login_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.show_intro()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        top_y = 205
        card_w = min(1240, self.width() - 60)
        card_h = min(680, self.height() - top_y - 34)
        card_w = max(860, card_w)
        card_h = max(440, card_h)
        x = (self.width() - card_w) // 2
        self.card.setGeometry(x, top_y, card_w, card_h)

    def _build_ui(self):
        self.card = CardFrame(self)
        outer = QVBoxLayout(self.card)
        outer.setContentsMargins(28, 28, 28, 24)
        outer.setSpacing(0)

        self.stack = QStackedWidget()
        outer.addWidget(self.stack)

        self.onboarding_screen = OnboardingScreen(self)
        self.driver_trip_screen = DriverTripScreen(self)
        self.environment_screen = EnvironmentScreen(self)
        self.vehicle_screen = VehicleScreen(self)

        self.stack.addWidget(self.onboarding_screen)
        self.stack.addWidget(self.driver_trip_screen)
        self.stack.addWidget(self.environment_screen)
        self.stack.addWidget(self.vehicle_screen)

        self.onboarding_screen.proceed_requested.connect(self.show_driver_trip)
        self.onboarding_screen.logout_requested.connect(self.back_to_login_requested.emit)
        
        self.driver_trip_screen.next_requested.connect(self._go_to_vehicle_if_valid)
        self.driver_trip_screen.logout_requested.connect(self.back_to_login_requested.emit)

        self.environment_screen.back_requested.connect(self.show_vehicle)
        self.environment_screen.next_requested.connect(self._emit_data)
        self.environment_screen.logout_requested.connect(self.back_to_login_requested.emit)

        self.vehicle_screen.back_requested.connect(self.show_driver_trip)
        self.vehicle_screen.evaluate_requested.connect(self._go_to_environment_if_valid)
        self.vehicle_screen.logout_requested.connect(self.back_to_login_requested.emit)

    def _set_header(self, title: str, subtitle: str):
        bg = self.parent()
        if hasattr(bg, "set_evaluation_header"):
            bg.set_evaluation_header(title, subtitle)

    def show_intro(self):
        self.stack.setCurrentWidget(self.onboarding_screen)
        self._set_header("BEFORE ASSESSING YOUR RISK,", "ARE YOU PREPARED TO DRIVE?")

    def show_driver_trip(self):
        self.stack.setCurrentWidget(self.driver_trip_screen)
        self._set_header("PRE-DRIVING EVALUATION", "COMPLETE ALL FIELDS TO ASSESS COMPREHENSIVE DRIVING RISK")

    def show_vehicle(self):
        self.stack.setCurrentWidget(self.vehicle_screen)
        self._set_header("PRE-DRIVING EVALUATION", "COMPLETE ALL FIELDS TO ASSESS COMPREHENSIVE DRIVING RISK")

    def show_environment(self):
        self.stack.setCurrentWidget(self.environment_screen)
        self._set_header("PRE-DRIVING EVALUATION", "COMPLETE ALL FIELDS TO ASSESS COMPREHENSIVE DRIVING RISK")


    def start_new_evaluation(self):
        self.driver_trip_screen.reset()
        self.environment_screen.reset()
        self.vehicle_screen.reset()
        self.stack.setCurrentWidget(self.driver_trip_screen)
        self.update()
        self.repaint()

    def _warn(self, message: str):
        QMessageBox.warning(self, "Incomplete Input", message)

    def _go_to_vehicle_if_valid(self):
        birthdate = self.driver_trip_screen.birthdate_input.date()
        driver_age = self.driver_trip_screen.calculate_age(birthdate)

        if driver_age < 18 or driver_age > 70:
            self._warn("Driver age must be between 18 and 70.")
            return

        if self.driver_trip_screen.driver_alcohol.currentIndex() == 0:
            self._warn("Please select your alcohol consumption before proceeding.")
            return

        if self.driver_trip_screen.driver_experience.currentIndex() == 0:
            self._warn("Please select your driving experience before proceeding.")
            return

        if self.driver_trip_screen.time_of_day.currentIndex() == 0:
            self._warn("Please select your time of day before proceeding.")
            return

        if self.driver_trip_screen.trip_duration.currentIndex() == 0:
            self._warn("Please select your expected trip duration before proceeding.")
            return

        self.show_vehicle()


    def _go_to_environment_if_valid(self):
        if self.vehicle_screen.vehicle_type.currentIndex() == 0:
            self._warn("Please select the vehicle type before proceeding.")
            return

        if self.vehicle_screen.failure_history.currentIndex() == 0:
            self._warn("Please select recent mechanical issues before proceeding.")
            return

        if self.vehicle_screen.vehicle_age.currentIndex() == 0:
            self._warn("Please select the vehicle age before proceeding.")
            return

        if self.vehicle_screen.brake_condition.currentIndex() == 0:
            self._warn("Please select the brake condition before proceeding.")
            return

        if self.vehicle_screen.maintenance_recency.currentIndex() == 0:
            self._warn("Please select the last vehicle maintenance before proceeding.")
            return

        self.show_environment()

    def _emit_data(self):
        birthdate = self.driver_trip_screen.birthdate_input.date()
        driver_age = self.driver_trip_screen.calculate_age(birthdate)

        if driver_age < 18 or driver_age > 70:
            self._warn("Driver age must be between 18 and 70 before running the assessment.")
            return

        # vehicle validation
        if self.vehicle_screen.vehicle_type.currentIndex() == 0:
            self._warn("Please select the vehicle type before running the assessment.")
            return

        if self.vehicle_screen.failure_history.currentIndex() == 0:
            self._warn("Please select recent mechanical issues before running the assessment.")
            return

        if self.vehicle_screen.vehicle_age.currentIndex() == 0:
            self._warn("Please select the vehicle age before running the assessment.")
            return

        if self.vehicle_screen.brake_condition.currentIndex() == 0:
            self._warn("Please select the brake condition before running the assessment.")
            return

        if self.vehicle_screen.maintenance_recency.currentIndex() == 0:
            self._warn("Please select the last vehicle maintenance before running the assessment.")
            return

        # environment validation
        if self.environment_screen.weather.currentIndex() == 0:
            self._warn("Please select the current weather condition before running the assessment.")
            return

        if self.environment_screen.road_type.currentIndex() == 0:
            self._warn("Please select the road type before running the assessment.")
            return

        if self.environment_screen.road_condition.currentIndex() == 0:
            self._warn("Please select the road condition before running the assessment.")
            return

        if self.environment_screen.road_defect.currentIndex() == 0:
            self._warn("Please select the visible road issues before running the assessment.")
            return

        if self.environment_screen.traffic_density.currentIndex() == 0:
            self._warn("Please select the traffic level before running the assessment.")
            return

        if self.environment_screen.intersection_related.currentIndex() == 0:
            self._warn("Please select the intersections / busy crossings field before running the assessment.")
            return

        payload = {
            "driver_age": driver_age,
            "alcohol_consumption": self.driver_trip_screen.driver_alcohol.currentText().strip().lower(),
            "driving_experience": self.driver_trip_screen.driver_experience.currentText().strip().lower(),
            "time_of_day": self.driver_trip_screen.time_of_day.currentText().strip().lower(),
            "expected_trip_duration": self.driver_trip_screen.trip_duration.currentText().strip().lower(),

            "weather_condition": self.environment_screen.weather.currentText().strip().lower(),
            "visible_road_issues": self.environment_screen.road_defect.currentText().strip().lower(),
            "road_type": self.environment_screen.road_type.currentText().strip().lower(),
            "traffic_level": self.environment_screen.traffic_density.currentText().strip().lower(),
            "road_condition": self.environment_screen.road_condition.currentText().strip().lower(),
            "intersections_busy_crossings": self.environment_screen.intersection_related.currentText().strip().lower(),

            "vehicle_type": self.vehicle_screen.vehicle_type.currentText().strip().lower(),
            "recent_mechanical_issues": self.vehicle_screen.failure_history.currentText().strip().lower(),
            "vehicle_age": self.vehicle_screen.vehicle_age.currentText().strip().lower(),
            "brake_condition": self.vehicle_screen.brake_condition.currentText().strip().lower(),
            "last_vehicle_maintenance": self.vehicle_screen.maintenance_recency.currentText().strip().lower(),
        }

        self.evaluate_requested.emit(payload)

    def clear_form(self):
        for checkbox in getattr(self.onboarding_screen, "awareness_checks", []):
            checkbox.setChecked(False)

        self.driver_trip_screen.reset()
        self.environment_screen.reset()
        self.vehicle_screen.reset()
        self.show_intro()