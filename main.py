import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from src.ui_manager import UIManager

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ui_manager = UIManager()
        ui_manager.login_widget.show()
        ui_manager.login_widget.setVisible(True)  # Force visibility
        # Hardcode position to ensure visibility
        ui_manager.login_widget.move(100, 100)
        # Log geometry and visibility
        print(f"Login window geometry: {ui_manager.login_widget.geometry()}")
        print(f"Login window isVisible: {ui_manager.login_widget.isVisible()}")
        # Temporarily disable animation to test visibility
        # ui_manager.animate_transition(ui_manager.login_widget)
        print("Application started, login window shown")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in main.py: {e}")
