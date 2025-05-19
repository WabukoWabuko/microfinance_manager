from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class ShortcutManager:
    def __init__(self):
        try:
            print("ShortcutManager initialized")
        except Exception as e:
            print(f"Error in ShortcutManager.__init__: {e}")
            raise

    def setup_shortcuts(self, widget):
        try:
            # Ctrl+D: Dashboard
            QShortcut(QKeySequence("Ctrl+D"), widget, lambda: widget.ui_manager.main_ui.content_stack.setCurrentIndex(0))
            # Ctrl+L: Loan
            QShortcut(QKeySequence("Ctrl+L"), widget, lambda: widget.ui_manager.main_ui.content_stack.setCurrentIndex(1))
            print("Shortcuts set up")
        except Exception as e:
            print(f"Error in setup_shortcuts: {e}")
            raise

    def close(self):
        try:
            print("ShortcutManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
