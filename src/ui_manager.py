from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QButtonGroup, QTableWidgetItem, QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from src.login import Ui_LoginWindow
from src.main_window import Ui_MainWindow
from src.database import Database
from src.auth import Auth
from src.loans import LoanManager
from src.transactions import TransactionManager
from src.sync import SyncManager

class UIManager:
    def __init__(self):
        try:
            self.db = Database()
            self.auth = Auth()
            self.loan_manager = LoanManager()
            self.transaction_manager = TransactionManager()
            self.sync_manager = SyncManager()
            self.current_user = None
            self.theme = "light"

            # Initialize login widget
            self.login_widget = QWidget()
            self.login_ui = Ui_LoginWindow()
            self.login_ui.setupUi(self.login_widget)
            print("Login widget initialized")

            # Initialize main window
            self.main_widget = QMainWindow()
            self.main_ui = Ui_MainWindow()
            self.main_ui.setupUi(self.main_widget)
            self.main_widget.setMinimumSize(1200, 800)
            print("Main window initialized")

            # Button group for sidebar navigation
            self.nav_group = QButtonGroup(self.main_widget)
            self.nav_group.setExclusive(True)
            self.nav_group.addButton(self.main_ui.dashboard_button, 0)
            self.nav_group.addButton(self.main_ui.loan_button, 1)
            self.nav_group.addButton(self.main_ui.transactions_button, 2)

            # Connect signals
            self.login_ui.login_button.clicked.connect(self.handle_login)
            self.main_ui.actionExit.triggered.connect(self.close)
            self.main_ui.actionToggle_Theme.triggered.connect(self.toggle_theme)
            self.main_ui.submit_loan_button.clicked.connect(self.handle_loan_submission)
            self.main_ui.calculate_button.clicked.connect(self.handle_calculate_payment)
            self.main_ui.sync_button.clicked.connect(self.handle_sync)
            self.main_ui.back_button_loan.clicked.connect(self.back_to_dashboard)
            self.nav_group.buttonClicked[int].connect(self.main_ui.content_stack.setCurrentIndex)

            # Add tooltips
            self.login_ui.email_input.setToolTip("Enter your registered email")
            self.login_ui.password_input.setToolTip("Enter your password")
            self.login_ui.role_combo.setToolTip("Select your role")
            self.login_ui.login_button.setToolTip("Click to log in")
            self.main_ui.dashboard_button.setToolTip("View your dashboard")
            self.main_ui.loan_button.setToolTip("Apply for a new loan")
            self.main_ui.transactions_button.setToolTip("View transaction history")
            self.main_ui.sync_button.setToolTip("Sync transactions with MPesa")
            self.main_ui.calculate_button.setToolTip("Calculate monthly payment")
            self.main_ui.submit_loan_button.setToolTip("Submit loan application")
            self.main_ui.back_button_loan.setToolTip("Return to dashboard")

            # Initialize UI
            self.apply_theme()
            self.main_ui.statusbar.showMessage("Ready")
            print("UI initialized")
        except Exception as e:
            print(f"Error in UIManager.__init__: {e}")
            raise

    def handle_login(self):
        try:
            email = self.login_ui.email_input.text()
            password = self.login_ui.password_input.text()
            role = self.login_ui.role_combo.currentText().lower()
            success, result = self.auth.login(email, password)
            if success:
                if result["role"] == role:
                    self.current_user = result
                    self.login_widget.hide()
                    # Ensure main window is visible and centered
                    self.main_widget.setWindowTitle("Microfinance Manager")
                    self.main_widget.show()
                    screen = QDesktopWidget().screenGeometry()
                    size = self.main_widget.geometry()
                    self.main_widget.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
                    self.main_ui.label_welcome.setText(f"Welcome, {result['name']}!")
                    self.update_dashboard()
                    # Animate transition
                    self.animate_transition(self.main_widget)
                    print("Main window shown after login")
                else:
                    self.show_message("Error", "Invalid role", QMessageBox.Critical)
            else:
                self.show_message("Error", result, QMessageBox.Critical)
        except Exception as e:
            print(f"Error in handle_login: {e}")
            self.show_message("Error", f"Login failed: {e}", QMessageBox.Critical)

    def handle_loan_submission(self):
        try:
            if not self.current_user:
                return
            amount = float(self.main_ui.amount_input.text() or 0)
            term = int(self.main_ui.term_input.text() or 0)
            purpose = "General"
            success, msg = self.loan_manager.apply_loan(self.current_user["id"], amount, 5.0, purpose)
            self.show_message("Loan", msg, QMessageBox.Information)
            self.update_dashboard()
        except Exception as e:
            print(f"Error in handle_loan_submission: {e}")
            self.show_message("Error", f"Loan submission failed: {e}", QMessageBox.Critical)

    def handle_calculate_payment(self):
        try:
            amount = float(self.main_ui.amount_input.text() or 0)
            term = int(self.main_ui.term_input.text() or 0)
            payment = self.loan_manager.calculate_monthly_payment(amount, 5.0, term)
            self.main_ui.payment_result.setText(f"Monthly Payment: {payment}")
        except Exception as e:
            print(f"Error in handle_calculate_payment: {e}")
            self.show_message("Error", f"Calculation failed: {e}", QMessageBox.Critical)

    def handle_sync(self):
        try:
            self.main_ui.statusbar.showMessage("Syncing transactions...")
            success, msg = self.sync_manager.sync_transactions()
            self.main_ui.statusbar.showMessage(msg, 5000)
            self.show_message("Sync", msg, QMessageBox.Information)
            self.update_dashboard()
        except Exception as e:
            print(f"Error in handle_sync: {e}")
            self.show_message("Error", f"Sync failed: {e}", QMessageBox.Critical)

    def back_to_dashboard(self):
        try:
            self.main_ui.content_stack.setCurrentIndex(0)
            self.main_ui.dashboard_button.setChecked(True)
        except Exception as e:
            print(f"Error in back_to_dashboard: {e}")
            self.show_message("Error", f"Navigation failed: {e}", QMessageBox.Critical)

    def update_dashboard(self):
        try:
            if not self.current_user:
                print("No current user, skipping dashboard update")
                return
            # Update loan table
            loans = self.loan_manager.get_loans(self.current_user["id"])
            self.main_ui.loan_table.setRowCount(len(loans))
            for row, loan in enumerate(loans):
                for col, value in enumerate(loan[:4]):
                    self.main_ui.loan_table.setItem(row, col, QTableWidgetItem(str(value)))
            # Update transaction table
            if loans:
                transactions = self.transaction_manager.get_transactions(loans[0][0])
                self.main_ui.transaction_table.setRowCount(len(transactions))
                for row, transaction in enumerate(transactions):
                    for col, value in enumerate(transaction[:4]):
                        self.main_ui.transaction_table.setItem(row, col, QTableWidgetItem(str(value)))
            print("Dashboard updated")
        except Exception as e:
            print(f"Error in update_dashboard: {e}")
            self.show_message("Error", f"Dashboard update failed: {e}", QMessageBox.Critical)

    def apply_theme(self):
        try:
            style = "background: #F8F9FA; color: #000000; font-family: Roboto;" if self.theme == "light" else "background: #343A40; color: #FFFFFF; font-family: Roboto;"
            self.login_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #007BFF, stop:1 #0056B3); font-family: Roboto;")
            self.main_widget.setStyleSheet(style)
            self.main_ui.statusbar.setStyleSheet("background: #343A40; color: #FFFFFF;" if self.theme == "light" else "background: #212529; color: #FFFFFF;")
            self.main_ui.menubar.setStyleSheet("background: #343A40; color: #FFFFFF;" if self.theme == "light" else "background: #212529; color: #FFFFFF;")
            self.db.execute("INSERT OR REPLACE INTO Settings (id, theme, last_sync_timestamp) VALUES (1, ?, NULL)", (self.theme,))
            print("Theme applied")
        except Exception as e:
            print(f"Error in apply_theme: {e}")
            self.show_message("Error", f"Theme application failed: {e}", QMessageBox.Critical)

    def toggle_theme(self):
        try:
            self.theme = "dark" if self.theme == "light" else "light"
            self.apply_theme()
            print("Theme toggled")
        except Exception as e:
            print(f"Error in toggle_theme: {e}")
            self.show_message("Error", f"Theme toggle failed: {e}", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        try:
            msg = QMessageBox(self.main_widget)
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.setIcon(icon)
            msg.setStyleSheet("background: #F8F9FA; color: #000000; font-family: Roboto;" if self.theme == "light" else "background: #343A40; color: #FFFFFF; font-family: Roboto;")
            # Animate message box
            self.animate_message(msg)
            msg.exec_()
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
            animation.start()
            print(f"Transition animation started for {widget}")
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
            self.main_widget.close()
            self.login_widget.close()
            print("Application closed")
        except Exception as e:
            print(f"Error in close: {e}")
