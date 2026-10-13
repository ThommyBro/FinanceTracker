from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
)

from src.pyFinance.category import Category
from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.transaction import Transaction


class TransactionDialog(QDialog):

    def __init__(self, parent=None, transaction: Transaction | None = None):
        super().__init__(parent)
        self.transaction = transaction

        

        # set layout
        layout = QFormLayout()
        self.setLayout(layout)


        # Form values for input
        self.description_input = QLineEdit()
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMinimum(0.01)
        self.amount_input.setMaximum(1_000_000)
        self.amount_input.setDecimals(2)

        self.type_input = QComboBox()
        self.type_input.addItems(
            [transaction_type.value for transaction_type in TransactionType]
        )

        self.category_input = QComboBox()
        self.category_input.setMinimumWidth(180)
        self.category_input.addItems(
            [category.value for category in Category]
        )

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("food, weekly, cinema")

        layout.addRow("Description:", self.description_input)
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Type:", self.type_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Tags:", self.tags_input)

        # set title for the window, depending on edit or add
        if transaction is None:
            self.setWindowTitle("Add Transaction")
        else:
            self.setWindowTitle("Edit Transaction")
            self.load_transaction(transaction)


        # buttons for save and cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)


        


# =============================================
#   End of init
# =============================================

    def get_values(self):
        """
        Read Form values for 'Add Transaction'
        Returns dict with transaction attributes as keys.
        Used in transaction_tab
        """
        tags = {tag.strip() for tag in self.tags_input.text().split(";") if tag.strip()}

        return {
            "description": self.description_input.text(),
            "amount": self.amount_input.value(),
            "transaction_type": TransactionType(self.type_input.currentText()),
            "category": Category(self.category_input.currentText()),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "tags": tags
        }

    def load_transaction(self, transaction: Transaction) -> None:
        """Method for editing transactions"""
        self.description_input.setText(transaction.description)
        self.amount_input.setValue(transaction.amount)
        self.type_input.setCurrentText(transaction.transaction_type.value)
        self.category_input.setCurrentText(transaction.category.value)
        self.date_input.setDate(QDate.fromString(transaction.date,"yyyy-MM-dd"))
        self.tags_input.setText("; ".join(sorted(transaction.tags)))