
import pytest

from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category
from src.pyFinance.transaction import Transaction
from src.pyFinance.account import Account



# 1 simple EXPENSE transaction
@pytest.fixture
def expense_transaction():
    return Transaction(
        "An Expense",
        100,
        TransactionType.EXPENSE,
        Category.FOOD,
        "2026-08-17"
    )

# 1 simple INCOME transaction
@pytest.fixture
def income_transaction():
    return Transaction(
        "An Income",
        1000,
        TransactionType.INCOME,
        Category.SALARY,
        "2026-09-17"
    )



def make_transaction(
    description: str = "Test Transaction",
    amount: float = 100.0,
    transaction_type: TransactionType = TransactionType.EXPENSE,
    category: Category = Category.FOOD,
    date: str = "2026-09-01",
    tags: set[str] | None = None,
) -> Transaction:
    """
    Factory for transactions
    """
    return Transaction(
        description=description,
        amount=amount,
        transaction_type=transaction_type,
        category=category,
        date=date,
        tags=tags or set(),
    )

# Use factory for lots of transactions
# 
transactions = [
    make_transaction("Rent", 900, date="2026-09-01", category=Category.HOUSING),        # 1
    make_transaction("Food", 120, date="2026-09-03"),                                   # 2
    make_transaction("Food", 300, date="2026-09-10"),                                   # 3
    make_transaction("Cinema", 35, date="2026-09-15", category=Category.ENTERTAINMENT), # 4
    make_transaction("Shoes", 140, date="2026-09-20", category=Category.CLOTHING),      # 5
    make_transaction("Doctor", 80, date="2026-10-01", category=Category.HEALTH),        # 6
    make_transaction("New Bike", 1300,date="2026-10-05", category=Category.OTHER)       # 7
]

salary = make_transaction(
    description="Salary",
    amount=3000,
    transaction_type=TransactionType.INCOME,
    category=Category.SALARY,
    date="2026-09-30",
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


def test_filter_by_month(income_transaction, expense_transaction):
    acc = Account(name="My Account")

    acc.add_transaction(income_transaction)
    acc.add_transaction(expense_transaction)

    assert income_transaction.date == "2026-09-17"
    assert expense_transaction.date == "2026-08-17"

    august = acc.filter_by_month("2026-08")
    september = acc.filter_by_month("2026-09")

    assert august == [expense_transaction]
    assert september == [income_transaction]
    

def test_top_n_expenses():
    acc = Account(name="My Account")
    for ta in transactions:
        acc.add_transaction(ta)
    result = acc.top_n_expenses(3)
    assert len(result) == 3
    assert [ta.amount for ta in result] == [1300, 900, 300] 



