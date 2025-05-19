import sys
from PyQt5.QtWidgets import QApplication
from src.ui_manager import UIManager
from PyQt5.QtGui import QFont

if __name__ == "__main__":
   app = QApplication(sys.argv)
   app.setFont(QFont("Roboto", 10))
   ui_manager = UIManager()
   ui_manager.stack.show()
   sys.exit(app.exec_())
