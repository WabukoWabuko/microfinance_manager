from PyQt5.QtWidgets import QWidget


class AccessibilityManager:
    def __init__(self):
        try:
            print("AccessibilityManager initialized")
        except Exception as e:
            print(f"Error in AccessibilityManager.__init__: {e}")
            raise

    def setup_accessibility(self, ui_manager):
        try:
            # Set accessible names for login UI
            ui_manager.login_ui.email_input.setAccessibleName("Email input")
            ui_manager.login_ui.password_input.setAccessibleName(
                "Password input")
            ui_manager.login_ui.role_combo.setAccessibleName("Role selector")
            ui_manager.login_ui.login_button.setAccessibleName("Login button")
            if hasattr(ui_manager.login_ui, 'reset_password_button'):
                ui_manager.login_ui.reset_password_button.setAccessibleName(
                    "Reset password button")

            # Set accessible names for main UI
            ui_manager.main_ui.dashboard_button.setAccessibleName(
                "Dashboard button")
            ui_manager.main_ui.loan_button.setAccessibleName("Loan button")
            ui_manager.main_ui.transactions_button.setAccessibleName(
                "Transactions button")
            ui_manager.main_ui.analytics_button.setAccessibleName(
                "Analytics button")
            ui_manager.main_ui.repayment_button.setAccessibleName(
                "Repayment button")
            ui_manager.main_ui.profile_button.setAccessibleName(
                "Profile button")
            ui_manager.main_ui.sync_button.setAccessibleName("Sync button")
            ui_manager.main_ui.calculate_button.setAccessibleName(
                "Calculate button")
            ui_manager.main_ui.submit_loan_button.setAccessibleName(
                "Submit loan button")
            ui_manager.main_ui.back_button_loan.setAccessibleName(
                "Back button loan")
            ui_manager.main_ui.back_button_transactions.setAccessibleName(
                "Back button transactions")
            ui_manager.main_ui.back_button_analytics.setAccessibleName(
                "Back button analytics")
            ui_manager.main_ui.back_button_repayment.setAccessibleName(
                "Back button repayment")
            ui_manager.main_ui.back_button_profile.setAccessibleName(
                "Back button profile")
            ui_manager.main_ui.b2c_withdraw_button.setAccessibleName(
                "Withdraw button")
            ui_manager.main_ui.export_button.setAccessibleName("Export button")
            ui_manager.main_ui.notifications_button.setAccessibleName(
                "Notifications button")
            ui_manager.main_ui.profile_save_button.setAccessibleName(
                "Save profile button")
            ui_manager.main_ui.two_factor_button.setAccessibleName(
                "Two-factor setup button")
            print("Accessibility setup completed")
        except Exception as e:
            print(f"Error in setup_accessibility: {e}")
            raise

    def close(self):
        try:
            print("AccessibilityManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
