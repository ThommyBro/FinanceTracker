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
    QTabWidget,
    QFrame,
)

from .transaction_tab import TransactionsTab
from .transaction_dialog import TransactionDialog
from .overview_tab import OverviewTab
from .import_export_tab import ImportExportTab
from .kpi_card import KpiCard



class MainWindow(QMainWindow):

    def __init__(self, store):
        super().__init__()
        self.store = store

        self.setWindowTitle("Finance Tracker")
        self.resize(1200, 741)

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

   
        # KPI Cards
        kpi_layout = QHBoxLayout()
        self.balance_card = KpiCard("BALANCE")
        self.income_card = KpiCard("INCOME")
        self.expense_card = KpiCard("EXPENSE")

        kpi_layout.addWidget(self.balance_card)
        kpi_layout.addWidget(self.income_card)
        kpi_layout.addWidget(self.expense_card)


        layout.addLayout(kpi_layout)


        # self.balance_label = QLabel("Balance: 0.00 €")
        # self.income_label = QLabel("Income: 0.00 €")
        # self.expense_label = QLabel("Expense: 0.00 €")
        # # Add labels to layout
        # layout.addWidget(self.balance_label)
        # layout.addWidget(self.income_label)
        # layout.addWidget(self.expense_label)


        # ======================================
        #   Add Tabs
        # ======================================
        self.tabs = QTabWidget()

        # Overview Tab
        self.overview_tab = OverviewTab(self.store)
        self.tabs.addTab(self.overview_tab, "Overview")

        # Transaction Tab
        self.transactions_tab = TransactionsTab(self.store)
        self.tabs.addTab(self.transactions_tab,"Transactions")

        # Import Export Tab
        self.import_export_tab = ImportExportTab(self.store)
        self.tabs.addTab(self.import_export_tab, "Import / Export")


        layout.addWidget(self.tabs)

        # Signals

        # Account changed
        self.account_box.currentTextChanged.connect(self.update_account_summary)
        self.account_box.currentTextChanged.connect(self.overview_tab.set_account)
        self.account_box.currentTextChanged.connect(self.transactions_tab.set_account)
        self.account_box.currentTextChanged.connect(self.import_export_tab.set_account)

        # Transactions imported
        self.import_export_tab.transactions_imported.connect(self.update_account_summary)
        self.import_export_tab.transactions_imported.connect(self.overview_tab.refresh)
        self.import_export_tab.transactions_imported.connect(lambda _: self.transactions_tab.refresh())

        # Transaction Changed
        self.transactions_tab.transactions_changed.connect(self.update_account_summary)
        self.transactions_tab.transactions_changed.connect(self.overview_tab.refresh)

        

        # Calls initial update if more than 1 account exists so that numbers in the main account will be loaded
        if self.account_box.count() > 0:
            account_name = self.account_box.currentText()
            self.update_account_summary(account_name)
            self.overview_tab.set_account(account_name)
            self.transactions_tab.set_account(account_name)
            self.import_export_tab.set_account(account_name)
            

        layout.addStretch()


    def update_account_summary(self, account_name: str) -> None:
        """Updater for account Summaries"""
        account = self.store.get_account(account_name)
        self.balance_card.set_value(f"{account.balance:,.2f} €")
        self.income_card.set_value(f"{account.income_total:,.2f} €")
        self.expense_card.set_value(f"{account.expense_total:,.2f} €")
   


    


