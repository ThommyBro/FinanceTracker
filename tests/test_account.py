
import pytest

from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category
from src.pyFinance.transaction import Transaction
from src.pyFinance.account import Account



@pytest.fixture
def expense_transaction():
    return Transaction(
        "An Expense",
        100,
        TransactionType.EXPENSE,
        Category.FOOD,
        "2026-08-17"
    )


@pytest.fixture
def income_transaction():
    return Transaction(
        "An Income",
        1000,
        TransactionType.INCOME,
        Category.SALARY,
        "2026-08-17"
    )

def test_empty_account():
    acc = Account(name="My Account")
    assert acc.name == "My Account"
    assert acc.transactions == []


def test_add_transactions_to_account(income_transaction, expense_transaction,):
    acc = Account(name="My Account")
    acc.add_transaction(income_transaction)
    acc.add_transaction(expense_transaction)
    assert acc.expense_total == 100
    assert acc.income_total == 1000
    assert acc.balance == 900
    assert len(acc.transactions) == 2


def test_filter_by_category(income_transaction, expense_transaction):
    acc = Account(name="My Account")
    acc.add_transaction(income_transaction)
    acc.add_transaction(expense_transaction)

    result = acc.filter_by_category(Category.SALARY)
    assert result == [income_transaction]


def test_filter_by_category_with_non_match(income_transaction, expense_transaction):
    acc = Account(name="My Account")
    acc.add_transaction(income_transaction)
    acc.add_transaction(expense_transaction)

    result = acc.filter_by_category(Category.HEALTH)
    assert result == []


def test_search(income_transaction,expense_transaction):
    acc = Account(name="My Account")
    acc.add_transaction(income_transaction)
    acc.add_transaction(expense_transaction)

    assert acc.search("income") == [income_transaction]
    
  


