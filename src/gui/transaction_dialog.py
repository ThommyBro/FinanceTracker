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


class TransactionDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Transaction")

        layout = QFormLayout()
        self.setLayout(layout)

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
        self.category_input.addItems(
            [category.value for category in Category]
        )

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        layout.addRow("Description:", self.description_input)
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Type:", self.type_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Date:", self.date_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)


    def get_values(self):
        """
        Read Form values for 'Add Transaction'
        Returns dict with transaction attributes as keys.
        Used in transaction_tab
        """
        return {
            "description": self.description_input.text(),
            "amount": self.amount_input.value(),
            "transaction_type": TransactionType(self.type_input.currentText()),
            "category": Category(self.category_input.currentText()),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
        }