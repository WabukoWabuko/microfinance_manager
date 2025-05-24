import sys
from src.ui_manager import UIManager

if __name__ == "__main__":
    try:
        ui_manager = UIManager()
        sys.exit(ui_manager.app.exec_())
    except Exception as e:
        print(f"Error in main.py: {e}")
