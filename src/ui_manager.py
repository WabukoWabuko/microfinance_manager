import logging
from PyQt5 import QtWidgets, QtCore
from src.login import Ui_LoginWindow
from src.main_window import Ui_MainWindow
import bcrypt

class UIManager:
    def __init__(self, database):
        logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='a',
                           format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("Initializing UIManager")
        self.database = database
        self.app = QtWidgets.QApplication([])
        logging.debug("QApplication created")
        self.login_window = None
        self.main_window = None
        self.current_user_role = None
        self.current_user_id = None
        logging.debug("Calling setup_login_ui")
        self.setup_login_ui()
        logging.debug("UIManager initialization complete")

    def setup_login_ui(self):
        logging.debug("Entering setup_login_ui")
        try:
            logging.debug("Creating login_window")
            self.login_window = QtWidgets.QWidget()
            logging.debug("Creating Ui_LoginWindow")
            login_ui = Ui_LoginWindow()
            logging.debug("Calling setupUi")
            login_ui.setupUi(self.login_window)
            logging.debug("Setting login UI margins")
            if hasattr(login_ui, 'verticalLayout'):
                login_ui.verticalLayout.setContentsMargins(20, 20, 20, 20)
                login_ui.verticalLayout.setSpacing(15)
            else:
                logging.warning("verticalLayout not found in login_ui")
            # Connect buttons
            logging.debug("Connecting button signals")
            login_ui.login_button.clicked.connect(self.handle_login)
            login_ui.reset_password_button.clicked.connect(self.handle_reset_password)
            self.login_ui = login_ui  # Store for access in handle_login
            logging.debug("Showing login_window")
            self.login_window.show()
            logging.debug("setup_login_ui complete")
        except Exception as e:
            logging.error(f"Error setting up login UI: {str(e)}")
            raise

    def handle_login(self):
        logging.debug("Login button clicked")
        try:
            email = self.login_ui.email_input.text().strip()
            password = self.login_ui.password_input.text().strip()
            role = self.login_ui.role_combo.currentText()
            logging.debug(f"Login attempt: email={email}, role={role}")
            if not email or not password or not role:
                QtWidgets.QMessageBox.warning(self.login_window, "Input Error",
                                             "Please fill in all fields")
                logging.debug("Login failed: Empty fields")
                return
            user = self.database.get_user_by_email(email)
            logging.debug(f"User query result: {user}")
            if user is None:
                QtWidgets.QMessageBox.critical(self.login_window, "Login Failed",
                                              "Invalid email, password, or role")
                logging.debug("Login failed: User not found")
                return
            if not isinstance(user['password'], (str, bytes)):
                logging.error(f"Invalid password type: {type(user['password'])}")
                QtWidgets.QMessageBox.critical(self.login_window, "Error",
                                              "Invalid password format in database")
                return
            password_bytes = password.encode('utf-8')
            stored_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
            if bcrypt.checkpw(password_bytes, stored_password) and user['role'] == role:
                self.current_user_id = user['user_id']
                self.set_user_role(role, self.current_user_id)
                self.show_main_window()
                logging.debug(f"Login successful for {email}, role: {role}")
            else:
                QtWidgets.QMessageBox.critical(self.login_window, "Login Failed",
                                              "Invalid email, password, or role")
                logging.debug("Login failed: Invalid credentials")
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            QtWidgets.QMessageBox.critical(self.login_window, "Error",
                                          f"Login error: {str(e)}")

    def handle_reset_password(self):
        logging.debug("Reset Password button clicked")
        try:
            QtWidgets.QMessageBox.information(self.login_window, "Reset Password",
                                             "Please contact the admin to reset your password")
            logging.debug("Reset password requested")
        except Exception as e:
            logging.error(f"Error during reset password: {str(e)}")

    def setup_main_ui(self):
        logging.debug("Entering setup_main_ui")
        try:
            self.main_window = QtWidgets.QMainWindow()
            main_ui = Ui_MainWindow()
            main_ui.setupUi(self.main_window)
            logging.debug("Setting main UI margins")
            if hasattr(main_ui, 'horizontalLayout'):
                main_ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
                main_ui.horizontalLayout.setSpacing(0)
            if hasattr(main_ui, 'verticalLayout'):
                main_ui.verticalLayout.setContentsMargins(10, 20, 10, 10)
                main_ui.verticalLayout.setSpacing(10)
            if hasattr(main_ui, 'content_stack'):
                for i in range(main_ui.content_stack.count()):
                    page = main_ui.content_stack.widget(i)
                    layout = page.layout()
                    if layout:
                        layout.setContentsMargins(20, 20, 20, 20)
                        layout.setSpacing(15)
            self.main_window.show()
            logging.debug("setup_main_ui complete")
        except Exception as e:
            logging.error(f"Error setting up main UI: {str(e)}")
            raise

    def show_main_window(self):
        logging.debug("Entering show_main_window")
        if self.login_window:
            self.login_window.hide()
        self.setup_main_ui()
        logging.debug("show_main_window complete")

    def apply_theme(self, theme="light"):
        logging.debug(f"Applying theme: {theme}")
        try:
            if theme == "light":
                style = """
                    QWidget { background: #F8F9FA; color: #333333; font-family: Roboto; }
                    QPushButton { background: #007BFF; color: #FFFFFF; border: none; border-radius: 8px; padding: 12px; }
                    QPushButton:hover { background: #0056B3; }
                    QLineEdit, QComboBox, QTextEdit { border: 1px solid #CED4DA; border-radius: 8px; padding: 10px; background: #FFFFFF; }
                    QTableWidget { border: none; background: #FFFFFF; gridline-color: #E9ECEF; }
                """
            else:
                style = """
                    QWidget { background: #2C2C2C; color: #E9ECEF; font-family: Roboto; }
                    QPushButton { background: #007BFF; color: #FFFFFF; border: none; border-radius: 8px; padding: 12px; }
                    QPushButton:hover { background: #0056B3; }
                    QLineEdit, QComboBox, QTextEdit { border: 1px solid #4A4A4A; border-radius: 8px; padding: 10px; background: #3C3C3C; }
                    QTableWidget { border: none; background: #3C3C3C; gridline-color: #4A4A4A; }
                """
            self.app.setStyleSheet(style)
            logging.debug("Theme applied")
        except Exception as e:
            logging.error(f"Error applying theme: {str(e)}")

    def set_user_role(self, role, user_id):
        logging.debug(f"Setting user role: {role}, user_id: {user_id}")
        self.current_user_role = role
        self.current_user_id = user_id
        try:
            if self.main_window:
                main_ui = self.main_window.findChild(Ui_MainWindow)
                if role == "Client":
                    main_ui.clients_button.hide()
                    main_ui.analytics_button.hide()
                else:
                    main_ui.clients_button.show()
                    main_ui.analytics_button.show()
            logging.debug("User role set completed")
        except Exception as e:
            logging.error(f"Error setting user role: {str(e)}")
