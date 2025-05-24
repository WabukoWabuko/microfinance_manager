from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QButtonGroup, QTableWidgetItem
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from src.login import Ui_LoginWindow
from src.main_window import Ui_MainWindow
from src.database import Database
from src.auth import Auth
from src.loans import LoanManager
from src.transactions import TransactionManager
from src.sync import SyncManager
from src.b2c import B2CManager
from src.analytics import AnalyticsManager
from src.notifications import NotificationManager
from src.export import ExportManager
from src.profile import ProfileManager
from src.two_factor import TwoFactorAuth
from src.offline import OfflineManager
from src.shortcuts import ShortcutManager
from src.accessibility import AccessibilityManager
from src.widgets import WidgetManager
from src.audit import AuditLogger
from src.repayment import RepaymentManager
from src.i18n import I18nManager
from src.animations import AnimationManager
from src.password_reset import PasswordResetManager
from src.clients import ClientManager

class UIManager:
    def __init__(self):
        try:
            self.db = Database()
            self.auth = Auth()
            self.loan_manager = LoanManager()
            self.transaction_manager = TransactionManager()
            self.sync_manager = SyncManager()
            self.b2c_manager = B2CManager()
            self.analytics_manager = AnalyticsManager()
            self.notification_manager = NotificationManager()
            self.export_manager = ExportManager()
            self.profile_manager = ProfileManager()
            self.two_factor = TwoFactorAuth()
            self.offline_manager = OfflineManager()
            self.shortcut_manager = ShortcutManager()
            self.accessibility_manager = AccessibilityManager()
            self.widget_manager = WidgetManager()
            self.audit_logger = AuditLogger()
            self.repayment_manager = RepaymentManager()
            self.i18n = I18nManager()
            self.animation_manager = AnimationManager()
            self.password_reset = PasswordResetManager()
            self.client_manager = ClientManager()
            self.current_user = None
            self.theme = "light"
            self.previous_page = 0

            self.login_widget = QWidget()
            self.login_ui = Ui_LoginWindow()
            self.login_ui.setupUi(self.login_widget)
            self.login_widget.setVisible(True)

            self.main_widget = QMainWindow()
            self.main_ui = Ui_MainWindow()
            self.main_ui.setupUi(self.main_widget)
            self.main_widget.setMinimumSize(1200, 800)

            self.nav_group = QButtonGroup(self.main_widget)
            self.nav_group.setExclusive(True)
            self.nav_group.addButton(self.main_ui.dashboard_button, 0)
            self.nav_group.addButton(self.main_ui.loan_button, 1)
            self.nav_group.addButton(self.main_ui.transactions_button, 2)
            self.nav_group.addButton(self.main_ui.analytics_button, 3)
            self.nav_group.addButton(self.main_ui.repayment_button, 4)
            self.nav_group.addButton(self.main_ui.profile_button, 5)
            self.nav_group.addButton(self.main_ui.clients_button, 6)

            self.login_ui.login_button.clicked.connect(self.handle_login)
            if hasattr(self.login_ui, 'reset_password_button'):
                self.login_ui.reset_password_button.clicked.connect(self.handle_password_reset)
            else:
                print("Warning: reset_password_button not found in login UI")
            self.main_ui.actionExit.triggered.connect(self.close)
            self.main_ui.actionToggle_Theme.triggered.connect(self.toggle_theme)
            self.main_ui.submit_loan_button.clicked.connect(self.handle_loan_submission)
            self.main_ui.calculate_button.clicked.connect(self.handle_calculate_payment)
            self.main_ui.sync_button.clicked.connect(self.handle_sync)
            self.main_ui.back_button_loan.clicked.connect(self.back_to_previous)
            self.main_ui.back_button_transactions.clicked.connect(self.back_to_previous)
            self.main_ui.back_button_analytics.clicked.connect(self.back_to_previous)
            self.main_ui.back_button_repayment.clicked.connect(self.back_to_previous)
            self.main_ui.back_button_profile.clicked.connect(self.back_to_previous)
            self.main_ui.back_button_clients.clicked.connect(self.back_to_previous)
            self.main_ui.b2c_withdraw_button.clicked.connect(self.handle_b2c_withdrawal)
            self.main_ui.export_button.clicked.connect(self.handle_export)
            self.main_ui.notifications_button.clicked.connect(self.handle_notifications)
            self.main_ui.profile_save_button.clicked.connect(self.handle_profile_save)
            self.main_ui.two_factor_button.clicked.connect(self.handle_two_factor_setup)
            self.main_ui.add_client_button.clicked.connect(self.handle_add_client)
            self.nav_group.buttonClicked[int].connect(self.handle_navigation)

            self.login_ui.email_input.setToolTip(self.i18n.translate("Enter your username"))
            self.login_ui.password_input.setToolTip(self.i18n.translate("Enter your password"))
            self.login_ui.role_combo.setToolTip(self.i18n.translate("Select your role"))
            self.login_ui.login_button.setToolTip(self.i18n.translate("Click to log in"))
            if hasattr(self.login_ui, 'reset_password_button'):
                self.login_ui.reset_password_button.setToolTip(self.i18n.translate("Reset your password"))
            self.main_ui.dashboard_button.setToolTip(self.i18n.translate("View your dashboard"))
            self.main_ui.loan_button.setToolTip(self.i18n.translate("Apply for a new loan"))
            self.main_ui.transactions_button.setToolTip(self.i18n.translate("View transaction history"))
            self.main_ui.analytics_button.setToolTip(self.i18n.translate("View loan analytics"))
            self.main_ui.repayment_button.setToolTip(self.i18n.translate("View repayment schedule"))
            self.main_ui.profile_button.setToolTip(self.i18n.translate("Edit your profile"))
            self.main_ui.clients_button.setToolTip(self.i18n.translate("Manage clients"))
            self.main_ui.sync_button.setToolTip(self.i18n.translate("Sync transactions with MPesa"))
            self.main_ui.calculate_button.setToolTip(self.i18n.translate("Calculate monthly payment"))
            self.main_ui.submit_loan_button.setToolTip(self.i18n.translate("Submit loan application"))
            self.main_ui.back_button_loan.setToolTip(self.i18n.translate("Return to previous page"))
            self.main_ui.back_button_transactions.setToolTip(self.i18n.translate("Return to previous page"))
            self.main_ui.back_button_analytics.setToolTip(self.i18n.translate("Return to previous page"))
            self.main_ui.back_button_repayment.setToolTip(self.i18n.translate("Return to previous page"))
            self.main_ui.back_button_profile.setToolTip(self.i18n.translate("Return to previous page"))
            self.main_ui.back_button_clients.setToolTip(self.i18n.translate("Return to previous page"))
            self.main_ui.b2c_withdraw_button.setToolTip(self.i18n.translate("Withdraw funds via MPesa"))
            self.main_ui.export_button.setToolTip(self.i18n.translate("Export data to CSV/PDF"))
            self.main_ui.export_format_combo.setToolTip(self.i18n.translate("Select export format"))
            self.main_ui.notifications_button.setToolTip(self.i18n.translate("View notifications"))
            self.main_ui.profile_save_button.setToolTip(self.i18n.translate("Save profile changes"))
            self.main_ui.two_factor_button.setToolTip(self.i18n.translate("Setup two-factor authentication"))
            self.main_ui.add_client_button.setToolTip(self.i18n.translate("Add a new client"))
            self.main_ui.client_name_input.setToolTip(self.i18n.translate("Enter client name"))
            self.main_ui.client_email_input.setToolTip(self.i18n.translate("Enter client username"))
            self.main_ui.client_phone_input.setToolTip(self.i18n.translate("Enter client phone number"))
            self.main_ui.client_role_combo.setToolTip(self.i18n.translate("Select client role"))

            self.apply_theme()
            self.shortcut_manager.setup_shortcuts(self.main_widget)
            self.accessibility_manager.setup_accessibility(self)
            self.widget_manager.setup_dashboard(self.main_ui)
            self.notification_manager.check_due_payments(self.current_user)
            self.main_ui.statusbar.showMessage(self.i18n.translate("Ready"))
        except Exception as e:
            print(f"Error in UIManager.__init__: {e}")
            raise

    def handle_login(self):
        try:
            username = self.login_ui.email_input.text()
            password = self.login_ui.password_input.text()
            role = self.login_ui.role_combo.currentText().lower()
            success, result = self.auth.login(username, password)
            if success:
                if result["role"] == role:
                    if self.two_factor.is_enabled(result["id"]):
                        success, msg = self.two_factor.verify(result["id"])
                        if not success:
                            self.show_message(self.i18n.translate("Error"), msg, QMessageBox.Critical)
                            return
                    self.current_user = result
                    self.login_widget.hide()
                    self.main_widget.setWindowTitle(self.i18n.translate("Microfinance Manager"))
                    self.main_widget.show()
                    self.main_ui.label_welcome.setText(self.i18n.translate("Welcome, {name}!").format(name=result["username"]))
                    self.update_dashboard()
                    self.animation_manager.animate_sidebar(self.main_ui.sidebar)
                    self.audit_logger.log_action(result["id"], "login", "User logged in")
                else:
                    self.show_message(self.i18n.translate("Error"), self.i18n.translate("Invalid role"), QMessageBox.Critical)
            else:
                self.show_message(self.i18n.translate("Error"), result, QMessageBox.Critical)
        except Exception as e:
            print(f"Error in handle_login: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Login failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_navigation(self, index):
        try:
            self.previous_page = self.main_ui.content_stack.currentIndex()
            self.main_ui.content_stack.setCurrentIndex(index)
            if index == 6 and self.current_user["role"] != "admin":
                self.show_message(self.i18n.translate("Error"), self.i18n.translate("Admin access required"), QMessageBox.Critical)
                self.main_ui.content_stack.setCurrentIndex(self.previous_page)
                return
            self.audit_logger.log_action(self.current_user["id"], "navigate", f"Navigated to page {index}")
        except Exception as e:
            print(f"Error in handle_navigation: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Navigation failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def back_to_previous(self):
        try:
            self.main_ui.content_stack.setCurrentIndex(self.previous_page)
            self.nav_group.button(self.previous_page).setChecked(True)
            self.audit_logger.log_action(self.current_user["id"], "navigate", f"Returned to page {self.previous_page}")
        except Exception as e:
            print(f"Error in back_to_previous: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Navigation failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_loan_submission(self):
        try:
            if not self.current_user:
                return
            amount = float(self.main_ui.amount_input.text() or 0)
            term = int(self.main_ui.term_input.text() or 0)
            purpose = "General"
            success, msg = self.loan_manager.apply_loan(self.current_user["id"], amount, 5.0, purpose)
            self.show_message(self.i18n.translate("Loan"), self.i18n.translate(msg), QMessageBox.Information)
            self.update_dashboard()
            self.audit_logger.log_action(self.current_user["id"], "loan_submission", f"Submitted loan: {amount}")
        except Exception as e:
            print(f"Error in handle_loan_submission: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Loan submission failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_calculate_payment(self):
        try:
            amount = float(self.main_ui.amount_input.text() or 0)
            term = int(self.main_ui.term_input.text() or 0)
            payment = self.loan_manager.calculate_monthly_payment(amount, 5.0, term)
            self.main_ui.payment_result.setText(self.i18n.translate("Monthly Payment: {payment}").format(payment=payment))
        except Exception as e:
            print(f"Error in handle_calculate_payment: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Calculation failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_sync(self):
        try:
            self.main_ui.statusbar.showMessage(self.i18n.translate("Syncing transactions..."))
            success, msg = self.offline_manager.sync_if_online(self.sync_manager.sync_transactions)
            self.main_ui.statusbar.showMessage(self.i18n.translate(msg), 5000)
            self.show_message(self.i18n.translate("Sync"), self.i18n.translate(msg), QMessageBox.Information)
            self.update_dashboard()
            self.audit_logger.log_action(self.current_user["id"], "sync", "Synced transactions")
        except Exception as e:
            print(f"Error in handle_sync: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Sync failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_b2c_withdrawal(self):
        try:
            amount = float(self.main_ui.b2c_amount_input.text() or 0)
            phone = self.main_ui.b2c_phone_input.text()
            success, msg = self.b2c_manager.withdraw(self.current_user["id"], amount, phone)
            self.show_message(self.i18n.translate("Withdrawal"), self.i18n.translate(msg), QMessageBox.Information)
            self.audit_logger.log_action(self.current_user["id"], "b2c_withdrawal", f"Withdrew {amount} to {phone}")
        except Exception as e:
            print(f"Error in handle_b2c_withdrawal: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Withdrawal failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_export(self):
        try:
            format_type = self.main_ui.export_format_combo.currentText()
            success, msg = self.export_manager.export_data(self.current_user["id"], format_type)
            self.show_message(self.i18n.translate("Export"), self.i18n.translate(msg), QMessageBox.Information)
            self.audit_logger.log_action(self.current_user["id"], "export", f"Exported data as {format_type}")
        except Exception as e:
            print(f"Error in handle_export: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Export failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_notifications(self):
        try:
            notifications = self.notification_manager.get_notifications(self.current_user["id"])
            self.main_ui.notifications_text.setPlainText("\n".join([self.i18n.translate(n["message"]) for n in notifications]))
            self.main_ui.content_stack.setCurrentIndex(7)
            self.audit_logger.log_action(self.current_user["id"], "view_notifications", "Viewed notifications")
        except Exception as e:
            print(f"Error in handle_notifications: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Notifications failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_profile_save(self):
        try:
            username = self.main_ui.profile_name_input.text()
            success, msg = self.profile_manager.update_profile(self.current_user["id"], username)
            self.show_message(self.i18n.translate("Profile"), self.i18n.translate(msg), QMessageBox.Information)
            self.audit_logger.log_action(self.current_user["id"], "update_profile", "Updated profile")
        except Exception as e:
            print(f"Error in handle_profile_save: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Profile update failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_two_factor_setup(self):
        try:
            success, msg = self.two_factor.setup(self.current_user["id"], self.main_ui.two_factor_code_input.text())
            self.show_message(self.i18n.translate("Two-Factor"), self.i18n.translate(msg), QMessageBox.Information)
            self.audit_logger.log_action(self.current_user["id"], "two_factor_setup", "Setup two-factor authentication")
        except Exception as e:
            print(f"Error in handle_two_factor_setup: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Two-factor setup failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_password_reset(self):
        try:
            username = self.login_ui.email_input.text()
            success, msg = self.password_reset.initiate_reset(username)
            self.show_message(self.i18n.translate("Password Reset"), self.i18n.translate(msg), QMessageBox.Information)
            self.audit_logger.log_action(0, "password_reset", f"Initiated password reset for {username}")
        except Exception as e:
            print(f"Error in handle_password_reset: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Password reset failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def handle_add_client(self):
        try:
            if self.current_user["role"] != "admin":
                self.show_message(self.i18n.translate("Error"), self.i18n.translate("Admin access required"), QMessageBox.Critical)
                return
            username = self.main_ui.client_name_input.text()
            email = self.main_ui.client_email_input.text()
            phone = self.main_ui.client_phone_input.text()
            role = self.main_ui.client_role_combo.currentText().lower()
            success, msg = self.client_manager.add_client(username, email, phone, role)
            self.show_message(self.i18n.translate("Client"), self.i18n.translate(msg), QMessageBox.Information if success else QMessageBox.Critical)
            self.audit_logger.log_action(self.current_user["id"], "add_client", f"Added client: {username}")
            if success:
                self.main_ui.client_name_input.clear()
                self.main_ui.client_email_input.clear()
                self.main_ui.client_phone_input.clear()
        except Exception as e:
            print(f"Error in handle_add_client: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Client addition failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def update_dashboard(self):
        try:
            if not self.current_user:
                return
            loans = self.db.execute_fetch_all(
                "SELECT id, amount, status, date_issued FROM loans WHERE user_id = ?",
                (str(self.current_user["id"]),)
            )
            self.main_ui.loan_table.setRowCount(len(loans))
            for row, loan in enumerate(loans):
                for col, value in enumerate(loan):
                    self.main_ui.loan_table.setItem(row, col, QTableWidgetItem(str(value)))
            if loans:
                transactions = self.db.execute_fetch_all(
                    "SELECT id, loan_id, amount, type FROM transactions WHERE loan_id = ?",
                    (str(loans[0][0]),)
                )
                self.main_ui.transaction_table.setRowCount(len(transactions))
                for row, transaction in enumerate(transactions):
                    for col, value in enumerate(transaction):
                        self.main_ui.transaction_table.setItem(row, col, QTableWidgetItem(str(value)))
            self.analytics_manager.update_analytics(self.main_ui, self.current_user["id"])
            self.repayment_manager.update_schedule(self.main_ui, self.current_user["id"])
            self.widget_manager.update_dashboard(self.main_ui, self.current_user["id"])
        except Exception as e:
            print(f"Error in update_dashboard: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Dashboard update failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def apply_theme(self):
        try:
            style = """
                QWidget { background: #F8F9FA; color: #000000; font-family: Roboto; }
                QLineEdit, QComboBox, QPushButton { border: 1px solid #CED4DA; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background: #0056B3; color: #FFFFFF; }
                QTableWidget { gridline-color: #CED4DA; color: #000000; }
                QLabel, QTextEdit { color: #000000; }
            """ if self.theme == "light" else """
                QWidget { background: #343A40; color: #FFFFFF; font-family: Roboto; }
                QLineEdit, QComboBox, QPushButton { border: 1px solid #6C757D; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background: #0056B3; color: #FFFFFF; }
                QTableWidget { gridline-color: #6C757D; color: #FFFFFF; }
                QLabel, QTextEdit { color: #FFFFFF; }
            """
            self.login_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #007BFF, stop:1 #0056B3); font-family: Roboto; color: #FFFFFF;")
            self.main_widget.setStyleSheet(style)
            self.main_ui.statusbar.setStyleSheet("background: #343A40; color: #FFFFFF;" if self.theme == "light" else "background: #212529; color: #FFFFFF;")
            self.main_ui.menubar.setStyleSheet("background: #343A40; color: #FFFFFF;" if self.theme == "light" else "background: #212529; color: #FFFFFF;")
            self.main_ui.loan_table.setStyleSheet("QTableWidget { color: #000000; }" if self.theme == "light" else "QTableWidget { color: #FFFFFF; }")
            self.main_ui.transaction_table.setStyleSheet("QTableWidget { color: #000000; }" if self.theme == "light" else "QTableWidget { color: #FFFFFF; }")
            self.main_ui.analytics_text.setStyleSheet("QTextEdit { color: #000000; }" if self.theme == "light" else "QTextEdit { color: #FFFFFF; }")
            self.main_ui.repayment_table.setStyleSheet("QTableWidget { color: #000000; }" if self.theme == "light" else "QTableWidget { color: #FFFFFF; }")
            self.main_ui.notifications_text.setStyleSheet("QTextEdit { color: #000000; }" if self.theme == "light" else "QTextEdit { color: #FFFFFF; }")
        except Exception as e:
            print(f"Error in apply_theme: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Theme application failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def toggle_theme(self):
        try:
            self.theme = "dark" if self.theme == "light" else "light"
            self.apply_theme()
            self.audit_logger.log_action(self.current_user["id"], "toggle_theme", f"Toggled to {self.theme} theme")
        except Exception as e:
            print(f"Error in toggle_theme: {e}")
            self.show_message(self.i18n.translate("Error"), self.i18n.translate("Theme toggle failed: {error}").format(error=str(e)), QMessageBox.Critical)

    def show_message(self, title, message, icon):
        try:
            msg = QMessageBox(self.main_widget)
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.setIcon(icon)
            msg.setStyleSheet("background: #808080; color: #FFFFFF; font-family: Roboto;")
            msg.addButton(self.i18n.translate("Close"), QMessageBox.AcceptRole)
            self.animate_message(msg)
            msg.show()
            QTimer.singleShot(5000, msg.close)
            print(f"Message shown: {title} - {message}")
        except Exception as e:
            print(f"Error in show_message: {e}")

    def animate_transition(self, widget):
        try:
            widget.setWindowOpacity(0)
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(500)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.finished.connect(lambda: widget.setWindowOpacity(1.0))
            animation.start()
        except Exception as e:
            print(f"Error in animate_transition: {e}")

    def animate_message(self, msg):
        try:
            msg.setWindowOpacity(0)
            animation = QPropertyAnimation(msg, b"windowOpacity")
            animation.setDuration(300)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.finished.connect(lambda: msg.setWindowOpacity(1.0))
            animation.start()
        except Exception as e:
            print(f"Error in animate_message: {e}")

    def close(self):
        try:
            self.db.close()
            self.auth.close()
            self.loan_manager.close()
            self.transaction_manager.close()
            self.sync_manager.close()
            self.b2c_manager.close()
            self.analytics_manager.close()
            self.notification_manager.close()
            self.export_manager.close()
            self.profile_manager.close()
            self.two_factor.close()
            self.offline_manager.close()
            self.shortcut_manager.close()
            self.accessibility_manager.close()
            self.widget_manager.close()
            self.audit_logger.close()
            self.repayment_manager.close()
            self.i18n.close()
            self.animation_manager.close()
            self.password_reset.close()
            self.client_manager.close()
            self.main_widget.close()
            self.login_widget.close()
        except Exception as e:
            print(f"Error in close: {e}")
