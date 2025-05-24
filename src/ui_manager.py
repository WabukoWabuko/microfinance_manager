```python
import logging
from PyQt5 import QtWidgets, QtCore
from src.login import Ui_LoginWindow
from src.main_window import Ui_MainWindow

class UIManager:
    def __init__(self):
        logging.basicConfig(level=logging.ERROR, filename='debug.log', filemode='a',
                           format='%(asctime)s - %(levelname)s - %(message)s')
        self.app = QtWidgets.QApplication([])
        self.login_window = None
        self.main_window = None
        self.current_user_role = None
        self.current_user_id = None
        self.setup_login_ui()

    def setup_login_ui(self):
        try:
            self.login_window = QtWidgets.QWidget()
            login_ui = Ui_LoginWindow()
            login_ui.setupUi(self.login_window)
            # Fix margins: Use integers instead of QRect
            login_ui.verticalLayout.setContentsMargins(20, 20, 20, 20)
            login_ui.verticalLayout.setSpacing(15)
            self.login_window.show()
        except Exception as e:
            logging.error(f"Error setting up login UI: {str(e)}")

    def setup_main_ui(self):
        try:
            self.main_window = QtWidgets.QMainWindow()
            main_ui = Ui_MainWindow()
            main_ui.setupUi(self.main_window)
            # Fix margins: Use integers instead of QRect
            main_ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            main_ui.horizontalLayout.setSpacing(0)
            main_ui.verticalLayout.setContentsMargins(10, 20, 10, 10)
            main_ui.verticalLayout.setSpacing(10)
            # Fix content stack pages
            for i in range(main_ui.content_stack.count()):
                page = main_ui.content_stack.widget(i)
                layout = page.layout()
                if layout:
                    layout.setContentsMargins(20, 20, 20, 20)
                    layout.setSpacing(15)
            self.main_window.show()
        except Exception as e:
            logging.error(f"Error setting up main UI: {str(e)}")

    def show_main_window(self):
        if self.login_window:
            self.login_window.hide()
        self.setup_main_ui()

    def apply_theme(self, theme="light"):
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
        except Exception as e:
            logging.error(f"Error applying theme: {str(e)}")

    def set_user_role(self, role, user_id):
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
        except Exception as e:
            logging.error(f"Error setting user role: {str(e)}")
```
