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

        self.setWindowTitle("Personal Finance Tracker")
        self.resize(1200, 741)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(layout)

        # ---------- Header ----------

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)

        # Left side
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title_label = QLabel("Personal Finance Tracker")
        title_label.setObjectName("appTitle")

        subtitle_label = QLabel("Track your income, expenses and financial progress.")
        subtitle_label.setObjectName("appSubtitle")

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        # Right side
        account_layout = QVBoxLayout()
        account_layout.setSpacing(5)

        account_label = QLabel("ACCOUNT")
        account_label.setObjectName("accountTitle")

        self.account_box = QComboBox()
        self.account_box.setMinimumWidth(180)

        for account_name in self.store.list_accounts():
            self.account_box.addItem(account_name)

        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_box)

        # Combine both sides
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(account_layout)

        layout.addLayout(header_layout)

   
        # KPI Cards
        kpi_layout = QHBoxLayout()
        self.balance_card = KpiCard("BALANCE")
        self.income_card = KpiCard("INCOME")
        self.expense_card = KpiCard("EXPENSE")

        kpi_layout.addWidget(self.balance_card)
        kpi_layout.addWidget(self.income_card)
        kpi_layout.addWidget(self.expense_card)


        layout.addLayout(kpi_layout)


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
   


    


