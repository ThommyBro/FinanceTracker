
import sys
from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow
from src.storage.memorystore import InMemoryStore
from src.pyFinance.transaction import Transaction
from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category




def main():
    app = QApplication(sys.argv)

    store = InMemoryStore()
    store.create_account("My Account")
    store.create_account("Savings")

    store.add_transaction(
    "My Account",
    Transaction(
        description="Salary",
        amount=3000.0,
        transaction_type=TransactionType.INCOME,
        category=Category.SALARY,
        date="2026-10-01",
        )
    )

    store.add_transaction(
        "My Account",
        Transaction(
            description="Groceries",
            amount=120.0,
            transaction_type=TransactionType.EXPENSE,
            category=Category.FOOD,
            date="2026-10-03",
        )
    )



# =============================================
#   Main Window
# =============================================
    window = MainWindow(store)
    window.show()

    app.exec()
 
if __name__ == "__main__":
    main()