from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from view.qt.main_window import MainWindow
from model.auth_model import login, signup
from model.fuzzy_model import evaluate_fuzzy
from reportGenerator.genReport import genReport

class AppController:
    def __init__(self):
        self.window = MainWindow()
        self.current_client = None
        self.last_client_id = None
        self.current_report = None

        self.last_inputs = {}
        self.last_score = 0.0
        self.last_risk_level = "-"
        self.last_risk_distribution = {"low": 0.0, "medium": 0.0, "high": 0.0}
        self.last_reasons = []
        self.last_recommendations = []

        self.window.login_screen.login_requested.connect(self.handle_login)
        self.window.login_screen.signup_link_clicked.connect(self.show_signup)

        self.window.signup_screen.signup_requested.connect(self.handle_signup)
        self.window.signup_screen.login_link_clicked.connect(self.show_login)

        self.window.risk_input_screen.back_to_login_requested.connect(self.logout)
        self.window.risk_input_screen.evaluate_requested.connect(self.handle_evaluate)

        self.window.result_screen.back_requested.connect(self.show_risk_input)
        self.window.result_screen.download_requested.connect(self.handle_download_report)
        self.window.result_screen.advisory_requested.connect(self.show_advisory)
        

        self.window.advisory_screen.back_to_result_requested.connect(self.show_result_screen)
        
        self.window.advisory_screen.new_evaluation_requested.connect(self.start_new_evaluation)
        self.window.result_screen.new_evaluation_requested.connect(self.start_new_evaluation)

    def show(self):
        self.window.show()

    def show_login(self):
        self.window.show_login()

    def show_signup(self):
        self.window.show_signup()

    def show_risk_input(self):
        self.window.show_risk_input()

    def logout(self):
        self.current_client = None
        self.current_report = None
        self.last_client_id = None
        self.last_inputs = {}
        self.last_score = 0.0
        self.last_risk_level = "-"
        self.last_risk_distribution = {"low": 0.0, "medium": 0.0, "high": 0.0}
        self.last_reasons = []
        self.last_recommendations = []

        if hasattr(self.window.risk_input_screen, "clear_form"):
            self.window.risk_input_screen.clear_form()
        if hasattr(self.window.result_screen, "clear_result"):
            self.window.result_screen.clear_result()

        self.window.show_login()

    def handle_login(self, client_number: str, password: str):
        if not client_number or not password:
            self._show_message("Login Failed", "Please enter both client number and password.")
            return

        if login(client_number, password):
            self.current_client = client_number
            
            if hasattr(self.window.risk_input_screen, "clear_form"):
                self.window.risk_input_screen.clear_form()

            self.window.show_risk_input()
            self._show_message("Login Success", "You have successfully logged in.")
        else:
            self._show_message("Login Failed", "Invalid client number or password.")

    def handle_signup(self, client_number: str, password: str, confirm_password: str):
        if not client_number or not password or not confirm_password:
            self._show_message("Sign Up Failed", "Please complete all fields.")
            return

        if password != confirm_password:
            self._show_message("Sign Up Failed", "Passwords do not match.")
            return

        ok, message = signup(client_number, password)
        self._show_message("Sign Up", message)

        if ok:
            self.window.show_login()
            self.window.login_screen.set_client_number(client_number)

    def handle_evaluate(self, user_inputs: dict):
        if not self.current_client:
            self._show_message("Session Error", "Please log in first.")
            return

        try:
            score, risk_level, risk_distribution, reasons, recommendations = evaluate_fuzzy(user_inputs)

            report = self._build_report_text(
                client_id=self.current_client,
                inputs=user_inputs,
                score=score,
                risk_level=risk_level,
                risk_distribution=risk_distribution,
                reasons=reasons,
                recommendations=recommendations,
            )

            self.current_report = report
            self.last_inputs = user_inputs
            self.last_score = score
            self.last_risk_level = risk_level
            self.last_risk_distribution = risk_distribution
            self.last_reasons = reasons
            self.last_recommendations = recommendations

            self.window.result_screen.set_result(
                report=report,
                risk_level=risk_level,
                score=score,
                client_id=self.current_client,
                inputs=user_inputs,
                risk_distribution=risk_distribution,
                reasons=reasons,
                recommendations=recommendations,
            )
            self.window.show_result()

        except Exception as error:
            self._show_message("Evaluation Error", f"Failed to evaluate risk.\n\n{error}")

    def start_new_evaluation(self):
        if hasattr(self.window.result_screen, "clear_result"):
            self.window.result_screen.clear_result()

        self.window.show_risk_input()

        QTimer.singleShot(0, self.window.risk_input_screen.start_new_evaluation)
        

    def handle_download_report(self):
        if not getattr(self.window.result_screen, "current_inputs", None):
            QMessageBox.warning(
                self.window,
                "No Report Available",
                "Please run an evaluation before downloading a report."
            )
            return

        filename, _ = QFileDialog.getSaveFileName(
            self.window,
            "Download Evaluation Report",
            "evaluation_report.pdf",
            "PDF Files (*.pdf)"
        )

        if not filename:
            return

        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        risk_level = self.window.result_screen.current_risk_level
        client_id = self.window.result_screen.current_client_id
        inputs = self.window.result_screen.current_inputs
        reasons = self.window.result_screen.current_reasons
        recommendations = self.window.result_screen.current_recommendations

        score_text = self.window.result_screen.score_label.text().replace("Evaluation Score:", "").strip()

        if risk_level == "Low Risk":
            eval_summary = "Current conditions appear manageable for travel."
            reco_action = "Proceed with normal caution."
        elif risk_level == "Medium Risk":
            eval_summary = "There are notable risk factors before travel."
            reco_action = "Proceed only with extra caution."
        else:
            eval_summary = "Current conditions present serious pre-driving risk."
            reco_action = "Delay or avoid travel until conditions improve."

        risk_distribution = [
            self.window.result_screen.low_distribution.text().replace("Low Risk:", "").strip(),
            self.window.result_screen.medium_distribution.text().replace("Medium Risk:", "").strip(),
            self.window.result_screen.high_distribution.text().replace("High Risk:", "").strip(),
        ]

        input_summary = [
            str(inputs.get("driver_age", "-")),
            str(inputs.get("alcohol_consumption", "-")),
            str(inputs.get("driving_experience", "-")),
            str(inputs.get("time_of_day", "-")),
            str(inputs.get("expected_trip_duration", "-")),
            str(inputs.get("vehicle_type", "-")),
            str(inputs.get("vehicle_age", "-")),
            str(inputs.get("recent_mechanical_issues", "-")),
            str(inputs.get("brake_condition", "-")),
            str(inputs.get("last_vehicle_maintenance", "-")),
            str(inputs.get("weather_condition", "-")),
            str(inputs.get("visible_road_issues", "-")),
            str(inputs.get("road_type", "-")),
            str(inputs.get("traffic_level", "-")),
            str(inputs.get("road_condition", "-")),
            str(inputs.get("intersections_busy_crossings", "-")),
        ]

        report = genReport(filename)
        report.setRiskLevel(risk_level)
        report.setClientId(client_id)
        report.setEvaluationScore(score_text)
        report.setInputSummary(input_summary)
        report.setEvalSummary(eval_summary)
        report.setRecommendedAction(reco_action)
        report.setRiskDistribution(risk_distribution)
        report.setReasonList(reasons)
        report.setPriorityActions(recommendations)
        report.generateReport()

        QMessageBox.information(
            self.window,
            "Report Downloaded",
            "The evaluation report was successfully saved as a PDF."
        )


    def show_result_screen(self):
        self.window.show_result()

    def _show_message(self, title: str, text: str):
        QMessageBox.information(self.window, title, text)

    def _build_report_text(
        self,
        client_id: str,
        inputs: dict,
        score: float,
        risk_level: str,
        risk_distribution: dict,
        reasons: list[str],
        recommendations: list[str],
    ) -> str:
        lines = [
            "PRE-DRIVING RISK EVALUATION REPORT",
            "=" * 42,
            f"Client ID: {client_id}",
            f"Evaluation Score: {score:.2f}",
            f"Risk Level: {risk_level}",
            "",
            "RISK DISTRIBUTION",
            f"  Low Risk: {risk_distribution.get('low', 0.0):.2f}%",
            f"  Medium Risk: {risk_distribution.get('medium', 0.0):.2f}%",
            f"  High Risk: {risk_distribution.get('high', 0.0):.2f}%",
            "",
            "INPUT SUMMARY",
        ]

        label_map = {
            "driver_age": "Driver Age",
            "alcohol_consumption": "Alcohol Consumption",
            "driving_experience": "Driving Experience",
            "time_of_day": "Time of Day",
            "expected_trip_duration": "Expected Trip Duration",
            "vehicle_type": "Vehicle Type",
            "vehicle_age": "Vehicle Age",
            "recent_mechanical_issues": "Recent Mechanical Issues",
            "brake_condition": "Brake Condition",
            "last_vehicle_maintenance": "Last Vehicle Maintenance",
            "weather_condition": "Weather Condition",
            "visible_road_issues": "Visible Road Issues",
            "road_type": "Road Type",
            "traffic_level": "Traffic Level",
            "road_condition": "Road Condition",
            "intersections_busy_crossings": "Intersections / Busy Crossings",
        }

        for key, value in inputs.items():
            label = label_map.get(key, key.replace("_", " ").title())
            lines.append(f"{label}: {value}")

        lines.extend([
            "",
            "REASONS",
        ])
        lines.extend([f"- {reason}" for reason in reasons])

        lines.extend([
            "",
            "RECOMMENDATIONS",
        ])
        lines.extend([f"  - {item}" for item in recommendations])

        return "\n".join(lines)