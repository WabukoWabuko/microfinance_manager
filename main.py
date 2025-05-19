import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from src.ui_manager import UIManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Roboto", 11))
    try:
        ui_manager = UIManager()
        ui_manager.login_widget.setWindowTitle("Microfinance Manager - Login")
        ui_manager.login_widget.show()
        # Center the login window
        screen = QDesktopWidget().screenGeometry()
        size = ui_manager.login_widget.geometry()
        ui_manager.login_widget.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
        # Fade-in animation
        ui_manager.login_widget.setWindowOpacity(0)
        animation = QPropertyAnimation(ui_manager.login_widget, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in main.py: {e}")
        sys.exit(1)
