from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from user_form import UserForm
from group_form import GroupForm
from contribution_form import ContributionForm
from loan_form import LoanForm
from payout_form import PayoutForm
from sync_window import SyncWindow

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Microfinance Manager")
        self.setFixedSize(400, 300)
        self.token = token

        # Layout and widgets
        widget = QWidget()
        layout = QVBoxLayout()

        btn_users = QPushButton("Manage Users")
        btn_users.clicked.connect(self.open_user_form)
        layout.addWidget(btn_users)

        btn_groups = QPushButton("Manage Groups")
        btn_groups.clicked.connect(self.open_group_form)
        layout.addWidget(btn_groups)

        btn_contributions = QPushButton("Add Contributions")
        btn_contributions.clicked.connect(self.open_contribution_form)
        layout.addWidget(btn_contributions)

        btn_loans = QPushButton("Manage Loans")
        btn_loans.clicked.connect(self.open_loan_form)
        layout.addWidget(btn_loans)

        btn_payouts = QPushButton("Manage Payouts")
        btn_payouts.clicked.connect(self.open_payout_form)
        layout.addWidget(btn_payouts)

        btn_sync = QPushButton("Sync Data")
        btn_sync.clicked.connect(self.open_sync_window)
        layout.addWidget(btn_sync)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_user_form(self):
        self.user_form = UserForm(self.token)
        self.user_form.show()

    def open_group_form(self):
        self.group_form = GroupForm(self.token)
        self.group_form.show()

    def open_contribution_form(self):
        self.contribution_form = ContributionForm(self.token)
        self.contribution_form.show()

    def open_loan_form(self):
        self.loan_form = LoanForm(self.token)
        self.loan_form.show()

    def open_payout_form(self):
        self.payout_form = PayoutForm(self.token)
        self.payout_form.show()

    def open_sync_window(self):
        self.sync_window = SyncWindow(self.token)
        self.sync_window.show()
