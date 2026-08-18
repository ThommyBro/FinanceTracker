
import pytest

from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category
from src.pyFinance.transaction import Transaction



def test_correct_transaction():
    """
    A simple an correct transaction
    """
    ta = Transaction(
        "An Expense",
        120.5,
        TransactionType.EXPENSE,
        Category.FOOD,
        "2026-08-17"
    )

    assert ta.description == "An Expense"
    assert ta.amount == 120.5
    assert ta.transaction_type == TransactionType.EXPENSE
    assert ta.category == Category.FOOD
    assert ta.date == "2026-08-17"