from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget, QMessageBox
from PyQt5.QtGui import QFont
from src.login import Ui_LoginWindow
from src.main_window import Ui_MainWindow
from src.database import Database
from src.auth import Auth
from src.loans import LoanManager
from src.transactions import TransactionManager
from src.sync import SyncManager

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

       # Add widgets to stack
       self.stack.addWidget(self.login_widget)
       self.stack.addWidget(self.main_widget)

       # Connect signals
       self.login_ui.login_button.clicked.connect(self.handle_login)
       self.main_ui.actionExit.triggered.connect(self.stack.close)
       self.main_ui.actionToggle_Theme.triggered.connect(self.toggle_theme)
       self.main_ui.submit_loan_button.clicked.connect(self.handle_loan_submission)
       self.main_ui.calculate_button.clicked.connect(self.handle_calculate_payment)
       self.main_ui.sync_button.clicked.connect(self.handle_sync)
       self.main_ui.back_button_loan.clicked.connect(self.back_to_dashboard)

       # Initialize UI
       self.apply_theme()
       self.update_dashboard()

   def handle_login(self):
       email = self.login_ui.email_input.text()
       password = self.login_ui.password_input.text()
       role = self.login_ui.role_combo.currentText().lower()
       success, result = self.auth.login(email, password)
       if success and result["role"] == role:
           self.current_user = result
           self.stack.setCurrentWidget(self.main_widget)
           self.main_ui.label_welcome.setText(f"Welcome, {result['name']}!")
           self.update_dashboard()
       else:
           QMessageBox.critical(self.login_widget, "Error", result)

   def handle_loan_submission(self):
       if not self.current_user:
           return
       amount = float(self.main_ui.amount_input.text() or 0)
       term = int(self.main_ui.term_input.text() or 0)
       purpose = "General"
       success, msg = self.loan_manager.apply_loan(self.current_user["id"], amount, 5.0, purpose)
       QMessageBox.information(self.main_widget, "Loan", msg)
       self.update_dashboard()

   def handle_calculate_payment(self):
       amount = float(self.main_ui.amount_input.text() or 0)
       term = int(self.main_ui.term_input.text() or 0)
       payment = self.loan_manager.calculate_monthly_payment(amount, 5.0, term)
       self.main_ui.payment_result.setText(f"Monthly Payment: {payment}")

   def handle_sync(self):
       success, msg = self.sync_manager.sync_transactions()
       QMessageBox.information(self.main_widget, "Sync", msg)
       self.update_dashboard()

   def back_to_dashboard(self):
       self.main_ui.tabWidget.setCurrentIndex(0)

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
       style = "background-color: #FFFFFF; color: #000000; font-family: Roboto;" if self.theme == "light" else "background-color: #343A40; color: #FFFFFF; font-family: Roboto;"
       self.login_widget.setStyleSheet(style)
       self.main_widget.setStyleSheet(style)
       self.db.execute("INSERT OR REPLACE INTO Settings (id, theme, last_sync_timestamp) VALUES (1, ?, NULL)", (self.theme,))

   def toggle_theme(self):
       self.theme = "dark" if self.theme == "light" else "light"
       self.apply_theme()

   def close(self):
       self.db.close()
       self.auth.close()
       self.loan_manager.close()
       self.transaction_manager.close()
       self.sync_manager.close()
