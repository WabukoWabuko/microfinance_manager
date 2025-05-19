class AccessibilityManager:
    def __init__(self):
        try:
            print("AccessibilityManager initialized")
        except Exception as e:
            print(f"Error in AccessibilityManager.__init__: {e}")
            raise

    def setup_accessibility(self, widget):
        try:
            widget.setAccessibleName("Main Window")
            widget.ui_manager.main_ui.label_welcome.setAccessibleName("Welcome Label")
            widget.ui_manager.main_ui.loan_table.setAccessibleName("Loan Table")
            print("Accessibility set up")
        except Exception as e:
            print(f"Error in setup_accessibility: {e}")
            raise

    def close(self):
        try:
            print("AccessibilityManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
