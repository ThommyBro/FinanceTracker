import sys
from PySide6.QtCore import Qt
from enum import IntEnum
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QTabWidget
)

from .transaction_tab import TransactionsTab
from .transaction_dialog import TransactionDialog



class MainWindow(QMainWindow):

    def __init__(self, store):
        super().__init__()
        self.store = store

        self.setWindowTitle("Finance Tracker")
        self.resize(1000, 618)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(layout)

        # Title in the main window
        title = QLabel("Personal Finance Tracker")
        layout.addWidget(title)

        account_label = QLabel("Account")
        layout.addWidget(account_label)


        # Account Choice
        self.account_box = QComboBox()
        self.account_box.addItems(self.store.list_accounts())
        layout.addWidget(self.account_box)
        self.account_box.currentTextChanged.connect(self.update_account_summary)


        
        


        # Summary labels
        self.balance_label = QLabel("Balance: 0.00 €")
        self.income_label = QLabel("Income: 0.00 €")
        self.expense_label = QLabel("Expense: 0.00 €")
        # Add labels to layout
        layout.addWidget(self.balance_label)
        layout.addWidget(self.income_label)
        layout.addWidget(self.expense_label)


        # Add Tabs
        self.tabs = QTabWidget()

        # Transaction Tab
        self.transactions_tab = TransactionsTab(self.store)
        self.transactions_tab.transactions_changed.connect(self.update_account_summary)
        self.tabs.addTab(self.transactions_tab,"Transactions")
        layout.addWidget(self.tabs)





        # Calls initial update if more than 1 account exists so that numbers in the main account will be loaded
        if self.account_box.count() > 0:
            account_name = self.account_box.currentText()
            self.update_account_summary(account_name)
            self.transactions_tab.update_transaction_table(account_name)

        layout.addStretch()


    def update_account_summary(self, account_name: str) -> None:
        """Updater for account Summaries"""
        account = self.store.get_account(account_name)
        self.balance_label.setText(f"Balance: {account.balance:.2f} €")
        self.income_label.setText(f"Income: {account.income_total:.2f} €")
        self.expense_label.setText(f"Expense: {account.expense_total:.2f} €")


    


