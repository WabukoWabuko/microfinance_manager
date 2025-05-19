from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget, QMessageBox, QButtonGroup
from PyQt5.QtGui import QFont, QGraphicsDropShadowEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from login import Ui_LoginWindow
from main_window import Ui_MainWindow
from database import Database
from auth import Auth
from loans import LoanManager
from transactions import TransactionManager
from sync import SyncManager

class UIManager:
   def __init__(self):
       self.db = Database()
       self.auth = Auth()
       self.loan_manager = LoanManager()
       self.transaction_manager = TransactionManager()
       self.sync_manager = SyncManager()
       self.current_user = None
       self.theme = "light"

       # Initialize stacked widget for navigation
       self.stack = QStackedWidget()
       self.login_widget = QWidget()
       self.main_widget = QMainWindow()

       # Set up UI
       self.login_ui = Ui_LoginWindow()
       self.login_ui.setupUi(self.login_widget)
       self.main_ui = Ui_MainWindow()
       self.main_ui.setupUi(self.main_widget)

       # Add shadow effect to login title
       shadow = QGraphicsDropShadowEffect()
       shadow.setBlurRadius(10)
       shadow.setXOffset(2)
       shadow.setYOffset(2)
       shadow.setColor(QtGui.QColor(0, 0, 0, 100))
       self.login_ui.label_title.setGraphicsEffect(shadow)

       # Button group for sidebar navigation
       self.nav_group = QButtonGroup(self.main_widget)
       self.nav_group.setExclusive(True)
       self.nav_group.addButton(self.main_ui.dashboard_button, 0)
       self.nav_group.addButton(self.main_ui.loan_button, 1)
       self.nav_group.addButton(self.main_ui.transactions_button, 2)

       # Connect signals
       self.login_ui.login_button.clicked.connect(self.handle_login)
       self.main_ui.actionExit.triggered.connect(self.stack.close)
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
       self.update_dashboard()
       self.main_ui.statusbar.showMessage("Ready")

   def handle_login(self):
       email = self.login_ui.email_input.text()
       password = self.login_ui.password_input.text()
       role = self.login_ui.role_combo.currentText().lower()
       success, result = self.auth.login(email, password)
       if success:
           if result["role"] == role:
               self.current_user = result
               self.stack.setCurrentWidget(self.main_widget)
               self.main_ui.label_welcome.setText(f"Welcome, {result['name']}!")
               self.update_dashboard()
               # Animate transition
               self.animate_transition(self.main_widget)
           else:
               self.show_message("Error", "Invalid role", QMessageBox.Critical)
       else:
           self.show_message("Error", result, QMessageBox.Critical)

   def handle_loan_submission(self):
       if not self.current_user:
           return
       amount = float(self.main_ui.amount_input.text() or 0)
       term = int(self.main_ui.term_input.text() or 0)
       purpose = "General"
       success, msg = self.loan_manager.apply_loan(self.current_user["id"], amount, 5.0, purpose)
       self.show_message("Loan", msg, QMessageBox.Information)
       self.update_dashboard()

   def handle_calculate_payment(self):
       amount = float(self.main_ui.amount_input.text() or 0)
       term = int(self.main_ui.term_input.text() or 0)
       payment = self.loan_manager.calculate_monthly_payment(amount, 5.0, term)
       self.main_ui.payment_result.setText(f"Monthly Payment: {payment}")

   def handle_sync(self):
       self.main_ui.statusbar.showMessage("Syncing transactions...")
       success, msg = self.sync_manager.sync_transactions()
       self.main_ui.statusbar.showMessage(msg, 5000)
       self.show_message("Sync", msg, QMessageBox.Information)
       self.update_dashboard()

   def back_to_dashboard(self):
       self.main_ui.content_stack.setCurrentIndex(0)
       self.main_ui.dashboard_button.setChecked(True)

   def update_dashboard(self):
       if not self.current_user:
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

   def apply_theme(self):
       style = "background: #F8F9FA; color: #000000; font-family: Roboto;" if self.theme == "light" else "background: #343A40; color: #FFFFFF; font-family: Roboto;"
       self.login_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #007BFF, stop:1 #0056B3); font-family: Roboto;")
       self.main_widget.setStyleSheet(style)
       self.main_ui.statusbar.setStyleSheet("background: #343A40; color: #FFFFFF;" if self.theme == "light" else "background: #212529; color: #FFFFFF;")
       self.main_ui.menubar.setStyleSheet("background: #343A40; color: #FFFFFF;" if self.theme == "light" else "background: #212529; color: #FFFFFF;")
       self.db.execute("INSERT OR REPLACE INTO Settings (id, theme, last_sync_timestamp) VALUES (1, ?, NULL)", (self.theme,))

   def toggle_theme(self):
       self.theme = "dark" if self.theme == "light" else "light"
       self.apply_theme()

   def show_message(self, title, message, icon):
       msg = QMessageBox(self.main_widget)
       msg.setWindowTitle(title)
       msg.setText(message)
       msg.setIcon(icon)
       msg.setStyleSheet("background: #F8F9FA; color: #000000; font-family: Roboto;" if self.theme == "light" else "background: #343A40; color: #FFFFFF; font-family: Roboto;")
       # Animate message box
       self.animate_message(msg)
       msg.exec_()

   def animate_transition(self, widget):
       animation = QPropertyAnimation(widget, b"windowOpacity")
       animation.setDuration(500)
       animation.setStartValue(0)
       animation.setEndValue(1)
       animation.setEasingCurve(QEasingCurve.InOutQuad)
       animation.start()

   def animate_message(self, msg):
       animation = QPropertyAnimation(msg, b"windowOpacity")
       animation.setDuration(300)
       animation.setStartValue(0)
       animation.setEndValue(1)
       animation.setEasingCurve(QEasingCurve.InOutQuad)
       animation.start()

   def close(self):
       self.db.close()
       self.auth.close()
       self.loan_manager.close()
       self.transaction_manager.close()
       self.sync_manager.close()
