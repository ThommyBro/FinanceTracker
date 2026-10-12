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
    QPushButton,
    QMessageBox,
    QComboBox,
)
from PySide6.QtCore import Signal, Qt

from enum import IntEnum
from src.pyFinance.transaction import Transaction
from .transaction_dialog import TransactionDialog
from src.pyFinance.category import Category





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
    TAGS = 5




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


        # =====================
        #   Filter Layout
        # =====================
        filter_layout = QHBoxLayout()

        month_label = QLabel("Month:")
        self.month_filter = QComboBox()

        category_label = QLabel("Category:")
        self.category_filter = QComboBox()

        filter_layout.addWidget(month_label)
        filter_layout.addWidget(self.month_filter)

        filter_layout.addWidget(category_label)
        filter_layout.addWidget(self.category_filter)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)


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
        self.delete_button.clicked.connect(self.delete_selected_transaction)

        #layout.addStretch()


        # Table for transaction Details
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(len(TransactionColumn))    
        self.transaction_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # you can select complete rows
        self.transaction_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)    #
        self.transaction_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)        # only view, no editing
        self.transaction_table.setHorizontalHeaderLabels([
            "Date",
            "Description",
            "Type",
            "Category",
            "Amount",
            "Tags"
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
            TransactionColumn.TAGS
        ]:
            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.ResizeToContents
            )

        # sets Edit and Delete active when a row is selected -> see method: update_action_buttons
        self.transaction_table.itemSelectionChanged.connect(self.update_action_buttons)

        # edit transaction button clicked
        self.edit_button.clicked.connect(self.edit_selected_transaction)

        # ========= Filter =====================
        self.category_filter.addItem("All Categories")
        for category in Category:
            self.category_filter.addItem(category.value)

        self.month_filter.currentTextChanged.connect(self.apply_filters)

        self.category_filter.currentTextChanged.connect(self.apply_filters)


        

        
    # ===============================================
    #   End of init
    # ===============================================

    def set_account(self, account_name: str) -> None:
        self.current_account_name = account_name
        self.refresh()


    def update_transaction_table(self, account_name: str) -> None:
        """Updater for transaction table"""
        self.current_account_name = account_name

        transactions = self.store.get_transactions(account_name)       # 1. get all transactions
        transactions = self.filtered_transactions(transactions)        # 2. filter afterwards
        
        self.transaction_table.setRowCount(len(transactions))

        for row, ta in enumerate(transactions):
            # define dataItem for deletion
            date_item = QTableWidgetItem(ta.date)
            date_item.setData(Qt.ItemDataRole.UserRole,ta.id)

            self.transaction_table.setItem(row,TransactionColumn.DATE, date_item)   # sets invisible dataItem
            self.transaction_table.setItem(row, TransactionColumn.DESCRIPTION, QTableWidgetItem(ta.description) )
            self.transaction_table.setItem(row, TransactionColumn.TYPE, QTableWidgetItem(ta.transaction_type.value) )
            self.transaction_table.setItem(row, TransactionColumn.CATEGORY, QTableWidgetItem(ta.category.value) )
            self.transaction_table.setItem(row, TransactionColumn.AMOUNT, QTableWidgetItem(f"{ta.signed_amount:.2f} €") )
            self.transaction_table.setItem(row,TransactionColumn.TAGS, QTableWidgetItem(",".join(sorted(ta.tags))))


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
                date=values["date"],
                tags=values["tags"],

            )
            self.store.add_transaction(self.current_account_name, transaction)
            self.refresh()
            #self.update_transaction_table(self.current_account_name)

            # send signal to the world
            self.transactions_changed.emit(self.current_account_name)


    def update_action_buttons(self) -> None:
        """
        Set Edit und Delete active only when a row is selected.
        """
        has_selection = (self.transaction_table.currentRow() >= 0)
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)


    def delete_selected_transaction(self) -> None:
        if self.current_account_name is None:
            return

        row = self.transaction_table.currentRow()

        if row < 0: return

        item = self.transaction_table.item(row, TransactionColumn.DATE )
        transaction_id = item.data(Qt.ItemDataRole.UserRole )

        answer = QMessageBox.question(self, "Delete Transaction", "Do you really want to delete this transaction?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                      QMessageBox.StandardButton.No 
                                      )
        if answer != QMessageBox.StandardButton.Yes:
            return 

        self.store.delete_transaction(self.current_account_name, transaction_id)
        self.refresh()
        self.transactions_changed.emit(self.current_account_name)    


    def edit_selected_transaction(self) -> None:
        if self.current_account_name is None:
            return

        row = self.transaction_table.currentRow()

        if row < 0: return

        item = self.transaction_table.item(row, TransactionColumn.DATE)
        transaction_id = item.data(Qt.ItemDataRole.UserRole)
        transaction = self.store.get_transaction(self.current_account_name,transaction_id)

        dialog = TransactionDialog(self, transaction)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()

            self.store.update_transaction(
                self.current_account_name,
                transaction_id,
                description=values["description"],
                amount=values["amount"],
                transaction_type=values["transaction_type"],
                category=values["category"],
                date=values["date"],
                tags=values["tags"]
            )
            self.refresh()
            self.transactions_changed.emit(self.current_account_name)


    def update_month_filter(self, transactions: list[Transaction]) -> None:
        current_selection = self.month_filter.currentText()

        months = sorted({ta.date[:7] for ta in transactions})
        self.month_filter.blockSignals(True)

        self.month_filter.clear()
        self.month_filter.addItem("All Months")
        self.month_filter.addItems(months)

        if current_selection in months:
            self.month_filter.setCurrentText(current_selection)
        else:
            self.month_filter.setCurrentText("All Months")

        self.month_filter.blockSignals(True)


    def filtered_transactions(self, transactions: list[Transaction]) -> list[Transaction]:
        selected_month = self.month_filter.currentText()
        selected_category = self.category_filter.currentText()

        result = transactions

        if selected_month and selected_month != "All Months":
            result = [ta for ta in result if ta.date[:7] == selected_month]

        if selected_category and selected_category != "All Categories":
            result = [ta for ta in result if ta.category.value == selected_category]

        return result


    def update_filter_options(self) -> None:
        if self.current_account_name is None: return

        transactions = self.store.get_transactions(self.current_account_name)
        current_month = self.month_filter.currentText()

        months = sorted({ta.date[:7] for ta in transactions})

        self.month_filter.blockSignals(True)

        self.month_filter.clear()
        self.month_filter.addItem("All Months")
        self.month_filter.addItems(months)

        if current_month in months:
            self.month_filter.setCurrentText(current_month)
        else:
            self.month_filter.setCurrentText("All Months")

        self.month_filter.blockSignals(False)


    def refresh(self) -> None:
        if self.current_account_name is None: return
        self.update_filter_options()
        self.update_transaction_table(self.current_account_name)




    def apply_filters(self) -> None:
        if self.current_account_name is None: return
        self.update_transaction_table(self.current_account_name)