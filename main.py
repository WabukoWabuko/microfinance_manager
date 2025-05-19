import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from src.ui_manager import UIManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Roboto", 11))
    ui_manager = UIManager()
    ui_manager.stack.show()
    ui_manager.stack.setWindowOpacity(0)
    animation = QPropertyAnimation(ui_manager.stack, b"windowOpacity")
    animation.setDuration(500)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.InOutQuad)
    animation.start()
    sys.exit(app.exec_())
