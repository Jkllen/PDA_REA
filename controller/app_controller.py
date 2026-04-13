from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from view.qt.main_window import MainWindow
from model.auth_model import login, signup
from model.fuzzy_model import evaluate_fuzzy
from model.crypto_model import encrypt_report, decrypt_report
from view.report_view import generate_report


class AppController:
    def __init__(self):
        self.window = MainWindow()
        self.current_client = None
        self.current_report = None
        self.current_encrypted_file = None

        self.window.login_screen.login_requested.connect(self.handle_login)
        self.window.login_screen.signup_link_clicked.connect(self.show_signup)

        self.window.signup_screen.signup_requested.connect(self.handle_signup)
        self.window.signup_screen.login_link_clicked.connect(self.show_login)

        self.window.risk_input_screen.back_to_login_requested.connect(self.logout)
        self.window.risk_input_screen.evaluate_requested.connect(self.handle_evaluate)

        self.window.result_screen.back_requested.connect(self.show_risk_input)
        self.window.result_screen.encrypt_requested.connect(self.handle_encrypt)
        self.window.result_screen.decrypt_requested.connect(self.handle_decrypt)

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
        self.current_encrypted_file = None
        self.window.risk_input_screen.clear_form()
        self.window.result_screen.clear_result()
        self.window.show_login()

    def handle_login(self, client_number: str, password: str):
        if not client_number or not password:
            self._show_message("Login Failed", "Please enter both client number and password.")
            return

        if login(client_number, password):
            self.current_client = client_number
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
            score, risk_level, triggered_reasons, recommendations = evaluate_fuzzy(user_inputs)

            report = generate_report(
                client=self.current_client,
                inputs=user_inputs,
                score=score,
                risk_level=risk_level,
                reasons=triggered_reasons,
                recommendations=recommendations,
            )

            self.current_report = report
            self.window.result_screen.set_result(report, risk_level, score)
            self.window.show_result()

        except Exception as error:
            self._show_message("Evaluation Error", f"Failed to evaluate risk.\n\n{error}")

    def handle_encrypt(self):
        if not self.current_report:
            self._show_message("No Report", "Please generate a report first.")
            return

        key, ok = QInputDialog.getText(self.window, "Encrypt Report", "Enter encryption key:")
        if not ok or not key.strip():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Save Encrypted Report",
            "report.enc",
            "Encrypted Files (*.enc)"
        )
        if not file_path:
            return

        try:
            saved_file = encrypt_report(self.current_report, key.strip(), file_path)
            self.current_encrypted_file = saved_file
            self._show_message("Encryption Success", f"Encrypted report saved to:\n{saved_file}")
        except Exception as error:
            self._show_message("Encryption Error", f"Failed to encrypt report.\n\n{error}")

    def handle_decrypt(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Open Encrypted Report",
            "",
            "Encrypted Files (*.enc)"
        )
        if not file_path:
            return

        key, ok = QInputDialog.getText(self.window, "Decrypt Report", "Enter decryption key:")
        if not ok or not key.strip():
            return

        try:
            decrypted = decrypt_report(key.strip(), file_path)
            if decrypted is None:
                self._show_message("Decryption Failed", "Invalid key or corrupted file.")
                return

            self.window.result_screen.set_decrypted_report(decrypted)

        except Exception as error:
            self._show_message("Decryption Error", f"Failed to decrypt report.\n\n{error}")

    def _show_message(self, title: str, text: str):
        QMessageBox.information(self.window, title, text)