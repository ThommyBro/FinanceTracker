
import pytest

from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category
from src.pyFinance.transaction import Transaction



def test_correct_transaction():
    """
    A simple and correct transaction
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


def test_expense_properties():
    ta = Transaction(
            "An Expense",
            120.5,
            TransactionType.EXPENSE,
            Category.FOOD,
            "2026-08-17"
        )
    assert ta.is_expense == True
    assert ta.signed_amount == -ta.amount
    assert ta.is_income == False


def test_income_properties():
    ta = Transaction(
            "An Income",
            500,
            TransactionType.INCOME,
            Category.HOUSING,
            "2026-08-17"
        )
    assert ta.is_expense == False
    assert ta.signed_amount == ta.amount
    assert ta.is_income == True


def test_empty_description_raises_value_error():
    with pytest.raises(ValueError, match="Description must not be empty"):
        Transaction(
            "",
            120.5,
            TransactionType.EXPENSE,
            Category.FOOD,
            "2026-08-17"
        )

def test_negative_amount_raises_value_error():
    with pytest.raises(ValueError):
        Transaction(
            "An Expense",
            -120.5,
            TransactionType.EXPENSE,
            Category.FOOD,
            "2026-08-17"
        )

def test_null_amount_raises_value_error():
    with pytest.raises(ValueError):
        Transaction(
            "An Expense",
            0,
            TransactionType.EXPENSE,
            Category.FOOD,
            "2026-08-17"
        )


def test_wrong_date_raises_value_error():
    with pytest.raises(ValueError):
        Transaction(
            "An Expense",
            120.5,
            TransactionType.EXPENSE,
            Category.FOOD,
            "20-08-1789"
        )

def test_tags():
    ta = Transaction(
        "Salary",
        12000,
        TransactionType.INCOME,
        Category.SALARY,
        "2026-08-17",
        {"Work", "Fun"}
    )
    assert ta.tags == {"Work", "Fun"}

def test_no_tags():
    ta = Transaction(
        "Salary",
        12000,
        TransactionType.INCOME,
        Category.SALARY,
        "2026-08-17",
    )
    assert ta.tags == set()

def test_default_tags_are_independent():
    ta1 = Transaction(
        "Salary",
        12000,
        TransactionType.INCOME,
        Category.SALARY,
        "2026-08-17",
    )

    ta2 = Transaction(
        "Rent refund",
        500,
        TransactionType.INCOME,
        Category.HOUSING,
        "2026-08-18",
    )

    ta1.tags.add("Work")

    assert ta1.tags == {"Work"}
    assert ta2.tags == set()