import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from src.ui_manager import UIManager

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ui_manager = UIManager()
        ui_manager.login_widget.show()
        ui_manager.animate_transition(ui_manager.login_widget)
        print("Application started")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in main.py: {e}")
