from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QDialog,
    QPushButton
)
from PySide6.QtCore import Signal

from enum import IntEnum
from src.pyFinance.transaction import Transaction
from .transaction_dialog import TransactionDialog





class TransactionColumn(IntEnum):
    """
    Helper Class
    A numbersystem for the transaction table for easier reading and adaptability
    """
    DATE = 0
    DESCRIPTION = 1
    TYPE = 2
    CATEGORY = 3
    AMOUNT = 4




class TransactionsTab(QWidget):
    """
    Home of all transaction functionality.
    Table, Filters, relevant Buttons ...
    """

    # my signal for new transactions
    transactions_changed = Signal(str)


    def __init__(self, store):
        super().__init__()
        self.store = store
        self.current_account_name: str | None = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # label = QLabel("Transactions")
        # layout.addWidget(label)


        # Buttons for the main window
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Transaction")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.edit_button.setEnabled(False)      # disabeled 
        self.delete_button.setEnabled(False)    # disabeled 
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        # Add Buttons to layout
        layout.addLayout(button_layout)

        # Button Click events
        self.add_button.clicked.connect(self.open_add_transaction_dialog)

        #layout.addStretch()


        # Table for transaction Details
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(5)
        self.transaction_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # you can select complete rows
        self.transaction_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)    #
        self.transaction_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)        # only view, no editing
        self.transaction_table.setHorizontalHeaderLabels([
            "Date",
            "Description",
            "Type",
            "Category",
            "Amount"
        ])
        layout.addWidget(self.transaction_table)


        # Set width for table headers
        header = self.transaction_table.horizontalHeader()
        header.setSectionResizeMode(
            TransactionColumn.DESCRIPTION,
            QHeaderView.ResizeMode.Interactive
        )
    
        for column in [
            TransactionColumn.DATE,
            TransactionColumn.TYPE,
            TransactionColumn.CATEGORY,
            TransactionColumn.AMOUNT,
        ]:
            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.ResizeToContents
            )


        

        


    def update_transaction_table(self, account_name: str) -> None:
        """Updater for transaction table"""
        self.current_account_name = account_name
        transactions = self.store.get_transactions(account_name)
        self.transaction_table.setRowCount(len(transactions))

        for row, ta in enumerate(transactions):
            self.transaction_table.setItem(row, TransactionColumn.DATE, QTableWidgetItem(ta.date) )
            self.transaction_table.setItem(row, TransactionColumn.DESCRIPTION, QTableWidgetItem(ta.description) )
            self.transaction_table.setItem(row, TransactionColumn.TYPE, QTableWidgetItem(ta.transaction_type.value) )
            self.transaction_table.setItem(row, TransactionColumn.CATEGORY, QTableWidgetItem(ta.category.value) )
            self.transaction_table.setItem(row, TransactionColumn.AMOUNT, QTableWidgetItem(f"{ta.signed_amount:.2f} €") )


    def open_add_transaction_dialog(self) -> None:
        dialog = TransactionDialog(self)

        # check if account is not none
        if self.current_account_name is None:
            return
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()

            transaction = Transaction(
                description=values["description"],
                amount=values["amount"],
                transaction_type=values["transaction_type"],
                category=values["category"],
                date=values["date"]
            )
            self.store.add_transaction(self.current_account_name, transaction)
            self.update_transaction_table(self.current_account_name)

            # send signal to the world
            self.transactions_changed.emit(self.current_account_name)
    